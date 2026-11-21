"""Forever Field Notes clip maker v2.

usage: python3 tools/make_clip.py specs/NAME.json NAME.mp4

Spec fields:
  title    ["LINE 1", "LINE 2"]                 required
  cards    [["Title", "Subtitle"], ...]          up to 3
  footer   ["Small line", "Call to action"]
  dur      seconds (default 12)
  style    dusk | parchment | frost | fel | ember | arcane   (default: picked from the file name)
  layout   cards | list | big                    (default cards)
  footage  "footage/file.mp4"  optional background video (own or permitted footage only)
  footage_credit "@creator"    shown on screen when footage is used
  footage_start  seconds into the footage to start (default 0)
  footage_audio  true to mix the footage's own sound under the music (default false)

Everything you hear is synthesised here (original music and sound effects), so there is
no licensed audio in any clip.
"""
import sys, os, math, random, json, subprocess, tempfile, wave, zlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SR = 1080, 1920, 30, 44100
HERE = os.path.dirname(os.path.abspath(__file__))
AS = os.path.join(HERE, 'assets')
FONTS = {
    'poppins_b': os.path.join(AS, 'Poppins-Bold.ttf'),
    'poppins_m': os.path.join(AS, 'Poppins-Medium.ttf'),
    'lora': os.path.join(AS, 'Lora-Variable.ttf'),
    'inter_black': os.path.join(AS, 'InterDisplay-Black.otf'),
    'inter_m': os.path.join(AS, 'Inter-Medium.otf'),
}
LOGO = os.path.join(AS, 'logo.png')

_font_cache = {}
_SHADOW = [True]
def F(key, size):
    k = (key, size)
    if k not in _font_cache:
        f = ImageFont.truetype(FONTS[key], size)
        if key == 'lora':
            try: f.set_variation_by_name('Bold')
            except Exception: pass
        _font_cache[k] = f
    return _font_cache[k]

def fit(text, key, size, maxw):
    d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    while size > 28 and d.textlength(text, font=F(key, size)) > maxw:
        size -= 4
    return F(key, size)

# ---------------------------------------------------------------- themes
# music: root Hz, scale (semitones), chord degrees, bpm, timbre, drums
THEMES = {
    'dusk': dict(top=(16, 20, 50), bot=(150, 78, 64), scenery='mountains', particles='twinkle',
                 title='poppins_b', body='poppins_m', c1=(250, 240, 220), c2=(232, 185, 92),
                 card='round', card_fill=(14, 18, 40, 215), card_line=(232, 185, 92), anim='up', shade=95,
                 music=dict(root=110.0, scale=[0, 2, 3, 5, 7, 8, 10], prog=[0, 5, 2, 6], bpm=84, timbre='warm', drums='soft')),
    'parchment': dict(top=(214, 190, 146), bot=(176, 140, 92), scenery='paper', particles='dust',
                      title='lora', body='lora', c1=(58, 34, 18), c2=(142, 32, 24),
                      card='paper', card_fill=(236, 218, 180, 235), card_line=(92, 58, 30), anim='fade', shade=0, shadow=False,
                      music=dict(root=146.83, scale=[0, 2, 4, 5, 7, 9, 11], prog=[0, 3, 4, 0], bpm=76, timbre='pluck', drums='none')),
    'frost': dict(top=(10, 24, 54), bot=(40, 120, 150), scenery='peaks', particles='snow',
                  title='inter_black', body='inter_m', c1=(240, 250, 255), c2=(120, 220, 255),
                  card='glass', card_fill=(255, 255, 255, 40), card_line=(170, 230, 255), anim='sides', shade=60,
                  music=dict(root=130.81, scale=[0, 2, 3, 5, 7, 8, 10], prog=[0, 5, 3, 4], bpm=92, timbre='bell', drums='soft')),
    'fel': dict(top=(6, 12, 8), bot=(20, 50, 22), scenery='glow', particles='motes',
                title='inter_black', body='inter_m', c1=(225, 255, 225), c2=(120, 255, 90),
                card='bar', card_fill=(8, 20, 10, 220), card_line=(120, 255, 90), anim='pop', shade=30,
                music=dict(root=98.0, scale=[0, 1, 3, 5, 7, 8, 10], prog=[0, 1, 5, 0], bpm=104, timbre='dark', drums='pulse')),
    'ember': dict(top=(18, 6, 4), bot=(120, 30, 10), scenery='glow', particles='embers',
                  title='poppins_b', body='poppins_m', c1=(255, 240, 225), c2=(255, 150, 50),
                  card='bar', card_fill=(30, 10, 6, 220), card_line=(255, 140, 40), anim='right', shade=40,
                  music=dict(root=87.31, scale=[0, 2, 3, 5, 7, 8, 10], prog=[0, 6, 5, 4], bpm=110, timbre='dark', drums='pulse')),
    'arcane': dict(top=(22, 8, 48), bot=(70, 30, 120), scenery='rings', particles='sparkle',
                   title='lora', body='poppins_m', c1=(248, 240, 255), c2=(200, 160, 255),
                   card='pill', card_fill=(30, 14, 60, 210), card_line=(200, 160, 255), anim='up', shade=40,
                   music=dict(root=123.47, scale=[0, 2, 4, 6, 7, 9, 11], prog=[0, 4, 5, 3], bpm=88, timbre='bell', drums='soft')),
}
STYLE_ORDER = ['dusk', 'parchment', 'frost', 'fel', 'ember', 'arcane']

def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

# ---------------------------------------------------------------- backgrounds
def grad(w, h, top, bot):
    a = np.linspace(0, 1, h)[:, None]
    arr = (np.array(top)[None, None, :] * (1 - a[..., None]) + np.array(bot)[None, None, :] * a[..., None])
    arr = np.repeat(arr, w, axis=1).astype(np.uint8)
    return Image.fromarray(arr, 'RGB')

def ridge(d, w, h, base, amp, col, seed, n=(7, 11)):
    rnd = random.Random(seed); pts = [(0, h)]; x = 0
    while x <= w + 60:
        pts.append((x, base - rnd.random() * amp)); x += w / rnd.randint(*n)
    pts += [(w, h)]; d.polygon(pts, fill=col)

def base_background(th, seed):
    bw, bh = int(W * 1.12), int(H * 1.12)
    im = grad(bw, bh, th['top'], th['bot']).convert('RGBA'); d = ImageDraw.Draw(im)
    rnd = random.Random(seed); sc = th['scenery']
    if sc == 'mountains':
        mx, my, mr = bw * .78, bh * .16, 95
        g = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([mx - mr * 2.4, my - mr * 2.4, mx + mr * 2.4, my + mr * 2.4], fill=(255, 210, 150, 70))
        im = Image.alpha_composite(im, g.filter(ImageFilter.GaussianBlur(90))); d = ImageDraw.Draw(im)
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(250, 226, 190))
        ridge(d, bw, bh, bh * .74, bh * .12, (58, 40, 62), seed + 1)
        ridge(d, bw, bh, bh * .84, bh * .10, (32, 26, 46), seed + 2)
        ridge(d, bw, bh, bh * .94, bh * .07, (14, 20, 38), seed + 3)
    elif sc == 'peaks':
        ridge(d, bw, bh, bh * .72, bh * .25, (30, 70, 110), seed + 1, (5, 8))
        ridge(d, bw, bh, bh * .86, bh * .18, (16, 44, 80), seed + 2, (6, 9))
        ridge(d, bw, bh, bh * .97, bh * .08, (8, 24, 50), seed + 3)
    elif sc == 'paper':
        arr = np.array(im).astype(np.int16)
        noise = np.random.default_rng(seed).normal(0, 9, (bh, bw, 1)).astype(np.int16)
        arr[..., :3] = np.clip(arr[..., :3] + noise, 0, 255)
        im = Image.fromarray(arr.astype(np.uint8), 'RGBA'); d = ImageDraw.Draw(im)
        for _ in range(14):  # faint map lines
            x0, y0 = rnd.randrange(bw), rnd.randrange(bh)
            pts = [(x0, y0)]
            for _ in range(8):
                x0 += rnd.randint(-120, 120); y0 += rnd.randint(-120, 120); pts.append((x0, y0))
            d.line(pts, fill=(120, 86, 50, 60), width=3)
        vign = Image.new('L', (bw, bh), 0); ImageDraw.Draw(vign).ellipse([-bw * .2, -bh * .1, bw * 1.2, bh * 1.1], fill=255)
        dark = Image.new('RGBA', (bw, bh), (70, 40, 15, 150)); dark.putalpha(Image.eval(vign.filter(ImageFilter.GaussianBlur(160)), lambda v: 150 - v * 150 // 255))
        im = Image.alpha_composite(im, dark)
    elif sc == 'glow':
        g = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); c = th['c2']
        ImageDraw.Draw(g).ellipse([bw * .1, bh * .55, bw * .9, bh * 1.2], fill=c + (90,))
        im = Image.alpha_composite(im, g.filter(ImageFilter.GaussianBlur(200)))
        d = ImageDraw.Draw(im); ridge(d, bw, bh, bh * .93, bh * .06, (0, 0, 0, 255), seed + 4, (10, 16))
    elif sc == 'rings':
        g = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        cx, cy = bw / 2, bh * .42
        for r in range(220, 1100, 140):
            gd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=th['c2'] + (40,), width=3)
        im = Image.alpha_composite(im, g.filter(ImageFilter.GaussianBlur(2)))
    if th['shade']:
        im = Image.alpha_composite(im, Image.new('RGBA', (bw, bh), (8, 10, 24, th['shade'])))
    return im

class Particles:
    def __init__(self, kind, seed, n=None):
        self.kind = kind; rnd = random.Random(seed)
        n = n or {'twinkle': 260, 'dust': 70, 'snow': 160, 'motes': 90, 'embers': 110, 'sparkle': 120}.get(kind, 0)
        self.p = [(rnd.random() * W, rnd.random() * H, rnd.uniform(1.5, 4.5), rnd.uniform(0.3, 1.0), rnd.random() * 6.28) for _ in range(n)]
    def draw(self, fr, s, th):
        if not self.p: return
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for x, y, r, sp, ph in self.p:
            k = self.kind
            if k == 'twinkle':
                if y > H * .62: continue
                a = int(140 + 115 * math.sin(s * 2.2 * sp + ph)); col = (255, 255, 255, max(0, a)); yy = y
                r = r * .6
            elif k == 'snow':
                yy = (y + s * 120 * sp) % H; x = (x + 30 * math.sin(s * sp + ph)) % W; col = (255, 255, 255, int(200 * sp))
            elif k == 'dust':
                yy = (y - s * 12 * sp) % H; x = (x + 8 * math.sin(s * .5 + ph)) % W; col = (90, 60, 30, int(70 * sp))
            elif k == 'motes':
                yy = (y - s * 70 * sp) % H; x = (x + 20 * math.sin(s * 1.3 * sp + ph)) % W; col = th['c2'] + (int(170 * sp),)
            elif k == 'embers':
                yy = (y - s * 150 * sp) % H; x = (x + 25 * math.sin(s * 2 * sp + ph)) % W
                col = (255, int(120 + 100 * sp), 40, int(220 * sp)); r = r * .8
            elif k == 'sparkle':
                a = max(0, math.sin(s * 3 * sp + ph)); yy = y; col = (230, 210, 255, int(255 * a))
                if a > .6:
                    d.line([(x - r * 3, yy), (x + r * 3, yy)], fill=col, width=2); d.line([(x, yy - r * 3), (x, yy + r * 3)], fill=col, width=2)
            else:
                continue
            d.ellipse([x - r, yy - r, x + r, yy + r], fill=col)
        if self.kind in ('motes', 'embers', 'sparkle'):
            L = Image.alpha_composite(L.filter(ImageFilter.GaussianBlur(3)), L)
        fr.alpha_composite(L)

class Footage:
    """Streams a video file as 1080x1920 cover-cropped RGB frames (loops if short)."""
    def __init__(self, path, start, dur):
        self.path, self.start, self.dur = path, start, dur
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
        self.proc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-stream_loop', '-1', '-ss', str(start), '-i', path,
                                      '-t', str(dur + 1), '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        self.last = None
    def frame(self):
        b = self.proc.stdout.read(W * H * 3)
        if len(b) == W * H * 3:
            self.last = Image.frombytes('RGB', (W, H), b)
        return (self.last or Image.new('RGB', (W, H))).convert('RGBA')
    def close(self):
        try: self.proc.kill()
        except Exception: pass

# ---------------------------------------------------------------- text and cards
def text_img(t, font, color, shadow=True):
    shadow = shadow and _SHADOW[0]
    d = ImageDraw.Draw(Image.new('RGB', (1, 1))); bb = d.textbbox((0, 0), t, font=font, anchor='lt')
    w, h = bb[2] - bb[0] + 28, bb[3] - bb[1] + 28
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((14 - bb[0], 17 - bb[1]), t, font=font, fill=(0, 0, 0, 210), anchor='lt')
        L = Image.alpha_composite(L, sh.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(L).text((14 - bb[0], 14 - bb[1]), t, font=font, fill=color, anchor='lt')
    return L

def card_img(th, title, sub, num=None, w=920, h=196):
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    fill, line, shape = th['card_fill'], th['card_line'], th['card']
    if shape == 'round':
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=36, fill=fill, outline=line, width=4)
    elif shape == 'glass':
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=28, fill=fill, outline=line + (200,), width=2)
    elif shape == 'pill':
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=fill, outline=line, width=3)
    elif shape == 'bar':
        d.rectangle([0, 0, w - 1, h - 1], fill=fill); d.rectangle([0, 0, 14, h - 1], fill=line)
    elif shape == 'paper':
        d.rectangle([0, 0, w - 1, h - 1], fill=fill, outline=line, width=4); d.rectangle([10, 10, w - 11, h - 11], outline=line + (120,), width=2)
    tf = 'lora' if th['title'] == 'lora' else ('inter_black' if th['title'] == 'inter_black' else 'poppins_b')
    if num is not None:
        cx = 98; d.ellipse([cx - 56, h // 2 - 56, cx + 56, h // 2 + 56], fill=line)
        d.text((cx, h // 2), str(num), font=F(tf, 64), fill=th['card_fill'][:3] if shape != 'glass' else (10, 24, 54), anchor='mm')
        x0, anc, maxw = 190, 'lm', w - 220
        d.text((x0, 74), title, font=fit(title, tf, 60, maxw), fill=th['c1'], anchor=anc)
        d.text((x0, 142), sub, font=fit(sub, th['body'], 40, maxw), fill=th['c2'], anchor=anc)
    else:
        x0 = w // 2 + (8 if shape == 'bar' else 0)
        d.text((x0, 74), title, font=fit(title, tf, 64, w - 80), fill=th['c1'], anchor='mm')
        d.text((x0, 142), sub, font=fit(sub, th['body'], 40, w - 80), fill=th['c2'], anchor='mm')
    return L

def layout(spec, th):
    """Returns list of (img, x, y, start, idx) and list of reveal times for sound."""
    t = spec['title']; cards = spec.get('cards', [])[:3]; foot = spec.get('footer', ['', ''])
    dur = spec.get('dur', 12); lay = spec.get('layout', 'cards'); tf = th['title']
    out = []
    def add(img, y, st, idx=0):
        out.append((img, (W - img.width) // 2, int(y - img.height / 2), st, idx))
    if lay == 'big':
        add(text_img(t[0], fit(t[0], tf, 230, 1000), th['c2']), 640, 0.15)
        add(text_img(t[1], fit(t[1], tf, 110, 1000), th['c1']), 820, 0.55)
        y = 1010; step = max(0.9, (dur - 6) / max(1, len(cards)))
        for k, (a, b) in enumerate(cards):
            line = f"{a}  ·  {b}"
            add(text_img(line, fit(line, th['body'], 52, 980), th['c1']), y + 110 * k, 1.5 + step * k * .8, k + 1)
        y = y + 110 * len(cards) + 40
    else:
        add(text_img(t[0], fit(t[0], tf, 104, 980), th['c1']), 610, 0.15)
        add(text_img(t[1], fit(t[1], tf, 124, 980), th['c2']), 742, 0.55)
        step = max(1.0, (dur - 6) / max(1, len(cards)))
        for k, (a, b) in enumerate(cards):
            img = card_img(th, a, b, num=(k + 1) if lay == 'list' else None)
            add(img, 985 + 232 * k, 1.5 + step * k * .8, k + 1)
        y = 985 + 232 * len(cards) - 30
    last = 1.5 + step * len(cards) * .8 if cards else 1.4
    if foot and foot[0]:
        add(text_img(foot[0], fit(foot[0], th['body'], 46, 980), th['c1']), y + 40, last)
    if foot and len(foot) > 1 and foot[1]:
        add(text_img(foot[1], fit(foot[1], tf if tf != 'lora' else 'lora', 54, 980), th['c2']), y + 132, last + .8)
    return out

def place(fr, img, x, y, st, idx, s, anim):
    a = ease((s - st) / 0.45)
    if a <= 0: return
    l = img
    dx = dy = 0
    if anim == 'up': dy = int((1 - a) * 70)
    elif anim == 'sides': dx = int((1 - a) * (-160 if idx % 2 else 160))
    elif anim == 'right': dx = int((1 - a) * 200)
    elif anim == 'pop' and a < 1:
        sc = 0.8 + 0.2 * a + 0.06 * math.sin(a * math.pi)
        nw, nh = max(1, int(img.width * sc)), max(1, int(img.height * sc))
        l = img.resize((nw, nh), Image.BILINEAR); x += (img.width - nw) // 2; y += (img.height - nh) // 2
    if a < 1:
        l = l.copy(); l.putalpha(l.getchannel('A').point(lambda v: int(v * a)))
    fr.alpha_composite(l, (x + dx, y + dy))

# ---------------------------------------------------------------- audio (all original, synthesised)
def lowpass(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4); return np.fft.irfft(X, len(x))

def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (1 / (1 + (lo / np.maximum(f, 1)) ** 4)) * (1 / (1 + (f / hi) ** 4)); return np.fft.irfft(X, len(x))

def tone(freq, n, timbre, rng):
    t = np.arange(n) / SR
    if timbre == 'warm':
        v = sum(np.sin(2 * np.pi * freq * k * t * (1 + d)) / k for k in (1, 2, 3, 4) for d in (-0.002, 0.002))
    elif timbre == 'bell':
        v = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2.01 * t) + 0.25 * np.sin(2 * np.pi * freq * 3.0 * t)
    elif timbre == 'pluck':
        v = sum(np.sin(2 * np.pi * freq * k * t) * np.exp(-t * (2 + k)) / k for k in (1, 2, 3, 4, 5))
    else:  # dark
        v = sum(np.sin(2 * np.pi * freq * k * t * (1 + d)) / (k * k) for k in (1, 2, 3, 5) for d in (-0.003, 0, 0.003))
    return v

def make_audio(th, dur, reveals, seed):
    m = th['music']; n = int(dur * SR); rng = np.random.default_rng(seed)
    out = np.zeros(n); beat = 60 / m['bpm']; bar = beat * 4
    scale = m['scale']
    def note(deg, octave=0):
        semis = scale[deg % 7] + 12 * (deg // 7 + octave); return m['root'] * 2 ** (semis / 12)
    # pad / chord progression (one chord per bar)
    nbars = int(math.ceil(dur / bar)) + 1
    for b in range(nbars):
        deg = m['prog'][b % len(m['prog'])]
        s0 = int(b * bar * SR); L = int(bar * SR * (1.0 if m['timbre'] != 'pluck' else 1.0))
        if s0 >= n: break
        L = min(L, n - s0); env = np.minimum(1, np.arange(L) / (0.25 * SR)) * np.minimum(1, (L - np.arange(L)) / (0.2 * SR))
        if m['timbre'] == 'pluck':
            for k in range(8):  # arpeggio
                st = s0 + int(k * beat / 2 * SR)
                if st >= n: break
                ln = min(int(0.9 * SR), n - st); f = note(deg + [0, 2, 4, 7][k % 4])
                out[st:st + ln] += 0.18 * tone(f, ln, 'pluck', rng)
            out[s0:s0 + L] += 0.10 * env * tone(note(deg, -1), L, 'warm', rng)
        else:
            for iv in (0, 2, 4):
                out[s0:s0 + L] += 0.07 * env * tone(note(deg + iv), L, m['timbre'], rng)
            out[s0:s0 + L] += 0.09 * env * tone(note(deg, -1), L, 'warm', rng)
            if m['timbre'] == 'bell':  # gentle bell melody
                for k in range(4):
                    st = s0 + int(k * beat * SR)
                    if st >= n: break
                    ln = min(int(1.2 * SR), n - st); t = np.arange(ln) / SR
                    f = note(deg + [4, 2, 7, 4][(b + k) % 4], 1)
                    out[st:st + ln] += 0.05 * np.sin(2 * np.pi * f * t) * np.exp(-t * 3)
    out = lowpass(out, 2600 if m['timbre'] != 'bell' else 5000)
    # drums
    t_k = np.arange(int(0.35 * SR)) / SR
    kick = np.sin(2 * np.pi * (45 * t_k + 60 * (1 - np.exp(-t_k * 30)) / 30 * 1)) * np.exp(-t_k * 9)
    hat = bandpass(rng.normal(0, 1, int(0.06 * SR)), 6000, 14000) * np.exp(-np.arange(int(0.06 * SR)) / SR * 70)
    if m['drums'] != 'none':
        k_gain = 0.45 if m['drums'] == 'pulse' else 0.28
        tt = beat * (2 if m['drums'] == 'soft' else 1)
        x = 1.5  # drums enter after the title
        while x < dur - 0.6:
            st = int(x * SR); ln = min(len(kick), n - st); out[st:st + ln] += k_gain * kick[:ln]; x += tt
        if m['drums'] == 'pulse':
            x = 1.5 + beat / 2
            while x < dur - 0.6:
                st = int(x * SR); ln = min(len(hat), n - st); out[st:st + ln] += 0.10 * hat[:ln]; x += beat
    # sound effects: riser into title, impact on title, whoosh on each reveal
    rl = int(0.7 * SR); riser = bandpass(rng.normal(0, 1, rl), 800, 9000) * np.linspace(0, 1, rl) ** 2 * 0.12
    out[:min(rl, n)] += riser[:min(rl, n)]
    t_i = np.arange(int(1.2 * SR)) / SR
    impact = (np.sin(2 * np.pi * 50 * t_i) * 0.6 + lowpass(rng.normal(0, 1, len(t_i)), 300) * 0.4) * np.exp(-t_i * 4) * 0.55
    st = int(0.15 * SR); ln = min(len(impact), n - st); out[st:st + ln] += impact[:ln]
    wl = int(0.4 * SR)
    for r in reveals:
        w = bandpass(rng.normal(0, 1, wl), 500, 6000) * np.sin(np.linspace(0, np.pi, wl)) ** 2 * 0.16
        st = int(max(0, r - 0.12) * SR); ln = min(wl, n - st)
        if ln > 0: out[st:st + ln] += w[:ln]
    # fades + normalise
    fi, fo = int(0.05 * SR), int(0.8 * SR)
    out[:fi] *= np.linspace(0, 1, fi); out[-fo:] *= np.linspace(1, 0, fo)
    out = np.tanh(out * 1.2); out /= (np.max(np.abs(out)) + 1e-9); out *= 0.84
    st = np.stack([out, np.roll(out, 220) * 0.96], axis=1)  # slight stereo width
    pcm = (st * 32767).astype(np.int16)
    path = tempfile.mktemp(suffix='.wav')
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
    return path

# ---------------------------------------------------------------- render
def build(spec, out, name_hint=''):
    style = spec.get('style') or STYLE_ORDER[zlib.crc32(name_hint.encode()) % len(STYLE_ORDER)]
    th = THEMES[style]; _SHADOW[0] = th.get('shadow', True) or bool(spec.get('footage')); dur = float(spec.get('dur', 12)); seed = zlib.crc32((name_hint + style).encode())
    layers = layout(spec, th)
    reveals = [st for (_, _, _, st, _) in layers]
    footage = None; fpath = spec.get('footage')
    if fpath:
        p = fpath if os.path.isabs(fpath) else os.path.join(os.path.dirname(HERE), fpath)
        if os.path.exists(p):
            footage = Footage(p, float(spec.get('footage_start', 0)), dur); fpath = p
        else:
            print('footage not found, using generated background:', p); fpath = None
    bg = None if footage else base_background(th, seed)
    parts = Particles(th['particles'] if not footage else 'none', seed)
    # legibility overlay for footage: theme-coloured gradient, darker behind text
    over = None
    if footage:
        a = np.concatenate([np.linspace(170, 120, 500), np.linspace(120, 215, H - 500)])
        over = Image.new('RGBA', (W, H), th['top'] + (0,)); over.putalpha(Image.fromarray(np.repeat(a[:, None], W, 1).astype(np.uint8), 'L'))
    logo = Image.open(LOGO).convert('RGBA').resize((190, 190), Image.LANCZOS)
    wm = text_img('Forever Field Notes', F('poppins_b', 40), th['c1'] if style != 'parchment' else th['c1'])
    credit = None
    if footage and spec.get('footage_credit'):
        credit = text_img('Footage: ' + spec['footage_credit'], F('poppins_m', 36), (255, 255, 255))
    music = make_audio(th, dur, reveals, seed)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', music]
    if footage and spec.get('footage_audio'):
        cmd += ['-ss', str(spec.get('footage_start', 0)), '-i', fpath, '-filter_complex',
                '[2:a]volume=0.45[fa];[1:a][fa]amix=inputs=2:duration=first:normalize=0[a]', '-map', '0:v', '-map', '[a]']
    else:
        cmd += ['-map', '0:v', '-map', '1:a']
    cmd += ['-t', str(dur), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(dur * FPS)
    for i in range(n):
        s = i / FPS
        if footage:
            fr = footage.frame(); fr.alpha_composite(over)
        else:
            z = 1 + 0.06 * s / dur; bw, bh = bg.size; cw, ch = int(bw / z), int(bh / z)
            fr = bg.crop(((bw - cw) // 2, (bh - ch) // 2, (bw - cw) // 2 + cw, (bh - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
            parts.draw(fr, s, th)
        fr.alpha_composite(logo, ((W - 190) // 2, 150)); fr.alpha_composite(wm, ((W - wm.width) // 2, 352))
        for img, x, y, st, idx in layers:
            place(fr, img, x, y, st, idx, s, th['anim'])
        if credit: fr.alpha_composite(credit, ((W - credit.width) // 2, H - 150))
        if s > dur - 0.4:
            k = (dur - s) / 0.4; fr = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), fr, k)
        p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    if footage: footage.close()
    os.remove(music)
    print(out, 'style=' + style, 'layout=' + spec.get('layout', 'cards'), 'footage=' + (os.path.basename(fpath) if fpath else 'none'))

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    build(spec, sys.argv[2], os.path.splitext(os.path.basename(sys.argv[2]))[0])
