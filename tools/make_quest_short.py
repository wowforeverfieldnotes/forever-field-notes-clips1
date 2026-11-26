"""Quest-window style Shorts: an original RPG quest dialog drawn in code (dark frame, gold title bar,
round portrait with the channel logo, parchment page, lines revealed one by one, two red buttons).
Pages come from the same spec data as make_guide_shorts (title1, title2, label, rows).
Music: reuses the audio track of the existing card-style render of the same Short when there is one.

usage (from a spec):  render(name, pages, out_path, audio_from=None)
"""
import os, subprocess, random, sys, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_clip as M
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, PAGE = 1080, 1920, 30, 12.0
HERE = os.path.dirname(os.path.abspath(__file__))
GF = '/usr/share/fonts/truetype/google-fonts/ofl'
F = {
    'title': os.path.join(GF, 'crimsontext/CrimsonText-SemiBold.ttf'),
    'head': os.path.join(GF, 'cardo/Cardo-Bold.ttf'),
    'item': os.path.join(GF, 'crimsontext/CrimsonText-Bold.ttf'),
    'sub': os.path.join(GF, 'crimsontext/CrimsonText-Regular.ttf'),
    'btn': os.path.join(GF, 'crimsontext/CrimsonText-SemiBold.ttf'),
}
LOGO = os.path.join(HERE, 'assets', 'logo.png')
GOLD, GOLD_D = (240, 196, 82), (150, 108, 40)
INK, INK_S, HEAD = (38, 24, 10), (74, 52, 26), (92, 30, 8)

def font(k, s): return ImageFont.truetype(F[k], s)

def fit(text, k, size, maxw):
    while size > 20:
        f = font(k, size)
        if f.getlength(text) <= maxw: return f
        size -= 2
    return font(k, size)

# window geometry
WX0, WX1, WY0, WY1 = 56, 1024, 250, 1790
TB = 96                                   # title bar height
PX0, PX1, PY0, PY1 = WX0 + 30, WX1 - 74, WY0 + TB + 20, WY1 - 120   # parchment (right strip = scrollbar)

def _bg():
    im = Image.new('RGB', (W, H), (14, 10, 8)); d = ImageDraw.Draw(im)
    for y in range(H):                     # warm dusk gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(40 - 22 * t), int(26 - 14 * t), int(20 - 10 * t)))
    rnd = random.Random(3)
    for _ in range(140):
        x, y = rnd.randrange(W), rnd.randrange(int(H * 0.55)); r = rnd.choice((1, 1, 2))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 104, 84))
    return im

def _parchment(w, h):
    rnd = random.Random(7)
    base = Image.new('RGB', (w, h), (226, 204, 156))
    noise = Image.effect_noise((w // 4, h // 4), 40).resize((w, h), Image.BICUBIC)
    tint = Image.merge('RGB', [noise.point(lambda v: 196 + (v - 128) * 0.25)] * 1 +
                       [noise.point(lambda v: 172 + (v - 128) * 0.22)] + [noise.point(lambda v: 122 + (v - 128) * 0.2)])
    base = Image.blend(base, tint, 0.55)
    # darker burnt edges
    edge = Image.new('L', (w, h), 0); ed = ImageDraw.Draw(edge)
    ed.rectangle([0, 0, w - 1, h - 1], outline=255, width=46)
    edge = edge.filter(ImageFilter.GaussianBlur(34))
    dark = Image.new('RGB', (w, h), (150, 112, 62))
    base = Image.composite(dark, base, edge)
    d = ImageDraw.Draw(base)
    for _ in range(18):                     # faint stains
        x, y, r = rnd.randrange(w), rnd.randrange(h), rnd.randrange(30, 120)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(200, 172, 120), width=2)
    return base.filter(ImageFilter.GaussianBlur(0.6))

def _button(d, x0, y0, x1, y1, text):
    d.rounded_rectangle([x0, y0, x1, y1], 8, fill=(108, 14, 10), outline=(40, 6, 4), width=4)
    d.rounded_rectangle([x0 + 6, y0 + 6, x1 - 6, y0 + (y1 - y0) // 2], 6, fill=(150, 26, 18))
    f = font('btn', 44)
    tw = f.getlength(text)
    d.text(((x0 + x1 - tw) / 2 + 2, y0 + 8 + 2), text, font=f, fill=(20, 4, 2))
    d.text(((x0 + x1 - tw) / 2, y0 + 8), text, font=f, fill=GOLD)

def base_frame(page_name):
    im = _bg().convert('RGBA'); d = ImageDraw.Draw(im)
    # shadow
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle(
        [WX0 + 10, WY0 + 18, WX1 + 10, WY1 + 18], 22, fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    # window frame
    d.rounded_rectangle([WX0, WY0, WX1, WY1], 20, fill=(24, 18, 14), outline=(92, 78, 62), width=6)
    d.rounded_rectangle([WX0 + 9, WY0 + 9, WX1 - 9, WY1 - 9], 14, outline=(46, 38, 30), width=3)
    # title bar
    d.rounded_rectangle([WX0 + 14, WY0 + 14, WX1 - 14, WY0 + TB], 10, fill=(34, 28, 24), outline=(70, 60, 48), width=2)
    f = fit(page_name, 'title', 58, (WX1 - WX0) - 360)
    tw = f.getlength(page_name); tx = (WX0 + WX1) / 2 - tw / 2 + 60
    d.text((tx + 2, WY0 + 20 + 2), page_name, font=f, fill=(0, 0, 0))
    d.text((tx, WY0 + 20), page_name, font=f, fill=GOLD)
    # close box
    cx0, cy0 = WX1 - 84, WY0 + 24
    d.rounded_rectangle([cx0, cy0, cx0 + 58, cy0 + 58], 8, fill=(118, 16, 10), outline=(196, 152, 70), width=3)
    d.line([cx0 + 16, cy0 + 16, cx0 + 42, cy0 + 42], fill=GOLD, width=6); d.line([cx0 + 42, cy0 + 16, cx0 + 16, cy0 + 42], fill=GOLD, width=6)
    # parchment + border
    im.alpha_composite(_parchment(PX1 - PX0, PY1 - PY0).convert('RGBA'), (PX0, PY0))
    d.rectangle([PX0 - 4, PY0 - 4, PX1 + 4, PY1 + 4], outline=(60, 44, 26), width=5)
    # scrollbar strip
    sx0, sx1 = PX1 + 14, WX1 - 18
    d.rectangle([sx0, PY0, sx1, PY1], fill=(16, 12, 10), outline=(70, 60, 48), width=2)
    for yy, up in ((PY0 + 6, True), (PY1 - 46, False)):
        d.rounded_rectangle([sx0 + 4, yy, sx1 - 4, yy + 40], 6, fill=(60, 50, 40), outline=(120, 100, 70), width=2)
        mx = (sx0 + sx1) / 2
        pts = [(mx, yy + 10), (mx - 10, yy + 30), (mx + 10, yy + 30)] if up else [(mx, yy + 30), (mx - 10, yy + 10), (mx + 10, yy + 10)]
        d.polygon(pts, fill=GOLD)
    d.rounded_rectangle([sx0 + 6, PY0 + 56, sx1 - 6, PY0 + 140], 6, fill=(96, 84, 66))
    # buttons
    _button(d, PX0, WY1 - 98, PX0 + 270, WY1 - 26, 'Accept')
    _button(d, PX1 - 214, WY1 - 98, PX1 + 56, WY1 - 26, 'Decline')
    # portrait (overlaps top-left corner)
    R, cx, cy = 128, WX0 + 96, WY0 + 30
    d.ellipse([cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10], fill=(20, 16, 12), outline=(110, 92, 64), width=6)
    logo = Image.open(LOGO).convert('RGBA').resize((2 * R, 2 * R), Image.LANCZOS)
    m = Image.new('L', (2 * R, 2 * R), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
    disc = Image.new('RGBA', (2 * R, 2 * R), (40, 30, 22, 255)); disc.alpha_composite(logo)
    im.paste(disc, (cx - R, cy - R), m)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(196, 152, 70), width=5)
    return im

def page_layers(label, rows, objective=None):
    """Return list of (rgba_image, (x, y)) to reveal one by one, in order. Rows are spread to fill the page."""
    x0, maxw = PX0 + 48, (PX1 - PX0) - 96
    htxt = label.upper(); hf = fit(htxt, 'head', 78, maxw)
    head = _text_layer(htxt, hf, HEAD)
    n = len(rows); isz, ssz = (68, 52) if n <= 4 else (60, 46)
    blocks = []
    for left, right, sub in rows:
        lay = Image.new('RGBA', (maxw, isz + (ssz + 14 if sub else 0) + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        rw = 0
        if right:
            rf = font('head', isz - 4); rw = rf.getlength(right) + 30
            d.text((maxw - rf.getlength(right), 4), right, font=rf, fill=HEAD)
        d.text((0, 0), left, font=fit(left, 'item', isz, maxw - rw), fill=INK)
        if sub:
            d.text((0, isz + 10), sub, font=fit(sub, 'sub', ssz, maxw), fill=INK_S)
        blocks.append(lay)
    obj = []
    if objective:
        of, sf = font('head', 60), font('sub', 48)
        obj = [_text_layer('Quest Objectives', of, HEAD)] + [_text_layer(l, sf, INK) for l in _wrap(objective, sf, maxw)]
    top, bottom = PY0 + 56, PY1 - 56
    used = head.height + 30 + sum(b.height for b in blocks) + (sum(o.height for o in obj) + 40 if obj else 0)
    gap = max(14, min(70 if n > 3 else 120, (bottom - top - used) / max(1, n)))
    out = [(head, (x0, top))]; y = top + head.height + 30
    for b in blocks:
        out.append((b, (x0, int(y)))); y += b.height + gap
    if obj:
        y += 10
        for o in obj:
            out.append((o, (x0, int(y)))); y += o.height
    return out

def page_layers_dense(label, rows, objective=None):
    """Full explanations, sized to fill the page: rows are (title, pill or None, detail text wrapped).
    Tries the largest text that fits, so pages with less text get bigger, easier-to-read lines."""
    x0, maxw = PX0 + 44, (PX1 - PX0) - 88
    top, bottom = PY0 + 40, PY1 - 36
    avail = bottom - top
    for k in [x / 100 for x in range(150, 79, -5)]:
        hs, ts, ds = int(66 * min(k, 1.2)), int(46 * k), int(36 * k)
        lh = int(ds * 1.18)
        head = _text_layer(label.upper(), fit(label.upper(), 'head', hs, maxw), HEAD)
        df = font('sub', ds)
        blocks = []
        for title, pill, detail in rows:
            lines = _wrap(detail, df, maxw) if detail else []
            h = int(ts * 1.15) + len(lines) * lh + 6
            lay = Image.new('RGBA', (maxw, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            rw = 0
            if pill:
                pf = font('head', int(ts * 0.87)); rw = pf.getlength(pill) + 24
                d.text((maxw - pf.getlength(pill), 4), pill, font=pf, fill=HEAD)
            d.text((0, 0), title, font=fit(title, 'item', ts, maxw - rw), fill=INK)
            for i, ln in enumerate(lines):
                d.text((0, int(ts * 1.17) + i * lh), ln, font=df, fill=INK_S)
            blocks.append(lay)
        obj = []
        if objective:
            of, sf = font('head', int(50 * min(k, 1.2))), font('sub', int(40 * min(k, 1.2)))
            obj = [_text_layer('Quest Objectives', of, HEAD)] + [_text_layer(l, sf, INK) for l in _wrap(objective, sf, maxw)]
        used = head.height + 20 + sum(b.height for b in blocks) + (sum(o.height for o in obj) + 24 if obj else 0)
        if used + 26 * len(blocks) <= avail:
            break
    if used > avail:
        raise ValueError(f'page "{label}" overflows by {used - avail} px')
    gap = max(12, min(96, (avail - used) / max(1, len(blocks))))
    out = [(head, (x0, top))]; y = top + head.height + 20
    for b in blocks:
        out.append((b, (x0, int(y)))); y += b.height + gap
    if obj:
        y += 4
        for o in obj:
            out.append((o, (x0, int(y)))); y += o.height
    return out

def page_seconds(rows, objective=None):
    """Reading time: about 3.3 words a second plus a beat, between 10 and 22 seconds."""
    words = sum(len((' '.join(x for x in r if x)).split()) for r in rows) + (len(objective.split()) if objective else 0)
    return float(min(22, max(10, round(3 + words / 3.3))))

def _wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if f.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def _text_layer(text, f, fill):
    w = int(f.getlength(text)) + 8; h = int(f.size * 1.35)
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((0, 0), text, font=f, fill=fill)
    return lay

def _fade(lay, a):
    if a >= 1: return lay
    r, g, b, al = lay.split(); al = al.point(lambda v: int(v * a))
    return Image.merge('RGBA', (r, g, b, al))

START, STEP, FADE = 0.5, 0.75, 0.35

def render(name, pages, out_path, style='dusk', objective='Follow Forever Field Notes for more WoW: Forever guides.', dense=False):
    """pages: list of (page_name, label, rows). dense=True: smaller text, wrapped explanations, page length set by reading time.
    Music + a whoosh on every line, timed to the reveals."""
    built = []
    for pi, (pname, label, rows) in enumerate(pages):
        obj = objective if pi == len(pages) - 1 else None
        if dense:
            L = page_layers_dense(label, rows, obj); dur = page_seconds(rows, obj)
            step = min(STEP, max(0.45, dur * 0.22 / max(1, len(L))))
        else:
            L = page_layers(label, rows, obj); dur = PAGE; step = STEP
        built.append((base_frame(pname), L, dur, step))
    total = sum(b[2] for b in built); tmp = out_path[:-4] + '.tmp.mp4'
    starts, t0 = [], 0.0
    for b in built: starts.append(t0); t0 += b[2]
    reveals = [starts[pi] + START + li * b[3] for pi, b in enumerate(built) for li in range(len(b[1]))]
    wav = M.make_audio(M.THEMES[style], total, reveals, zlib.crc32(name.encode()))
    cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', wav, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '160k',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-t', str(total), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    black = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    for pi, (base, layers, dur, step) in enumerate(built):
        for fi in range(int(round(dur * FPS))):
            t = fi / FPS
            fr = base.copy()
            for li, (lay, pos) in enumerate(layers):
                a = (t - (START + li * step)) / FADE
                if a <= 0: break
                a = min(a, 1.0)
                fr.alpha_composite(_fade(lay, a), (pos[0], int(pos[1] + (1 - a) * 14)))
            if t > dur - 0.4 and pi < len(built) - 1:
                fr = Image.blend(fr, black, (t - (dur - 0.4)) / 0.4 * 0.6)
            if t < 0.3 and pi > 0:
                fr = Image.blend(fr, black, (1 - t / 0.3) * 0.6)
            p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait(); os.remove(wav)
    if p.returncode == 0: os.replace(tmp, out_path)
    return out_path
