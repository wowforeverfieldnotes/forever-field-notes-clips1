"""Vertical Shorts cut from the leveling guides: one per level range per faction, one per class.
usage: python3 tools/make_guide_shorts.py CONTENT_DIR OUT_DIR [only_name]
CONTENT_DIR holds content.py (the guide script data)."""
import sys, os, math, json, subprocess, zlib
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_clip as M

W, H, FPS = M.W, M.H, M.FPS

def row_card(th, left, right, sub=None, w=940, h=128, tag=None, fsize=52):
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    shape = th['card']
    if shape == 'bar':
        d.rectangle([0, 0, w - 1, h - 1], fill=th['card_fill']); d.rectangle([0, 0, 12, h - 1], fill=th['card_line'])
    elif shape == 'paper':
        d.rectangle([0, 0, w - 1, h - 1], fill=th['card_fill'], outline=th['card_line'], width=4)
    elif shape == 'glass':
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=th['card_fill'], outline=th['card_line'] + (200,), width=2)
    else:
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2 if shape == 'pill' else 30, fill=th['card_fill'], outline=th['card_line'], width=3)
    tf = th['title'] if th['title'] != 'poppins_m' else 'poppins_b'
    x0 = 42
    if right:
        rf = M.F('poppins_b', 40); rw = int(ImageDraw.Draw(L).textlength(right, font=rf)) + 40
        d.rounded_rectangle([w - rw - 28, h // 2 - 34, w - 28, h // 2 + 34], radius=34, fill=th['card_line'])
        d.text((w - 28 - rw // 2, h // 2), right, font=rf, fill=th['card_fill'][:3] if shape != 'glass' else (10, 24, 54), anchor='mm')
        maxw = w - rw - 110
    else:
        maxw = w - 80
    if tag:
        tf2 = M.F('poppins_b', 26); tw = int(d.textlength(tag, font=tf2)) + 26
        d.rounded_rectangle([x0, 14, x0 + tw, 52], radius=19, fill=th['c2']); d.text((x0 + tw // 2, 33), tag, font=tf2, fill=(20, 20, 20), anchor='mm')
    if sub:
        d.text((x0, h // 2 - 20 + (8 if tag else 0)), left, font=M.fit(left, tf, 50, maxw), fill=th['c1'], anchor='lm')
        d.text((x0, h // 2 + 30), sub, font=M.fit(sub, th['body'], 34, maxw), fill=th['c2'], anchor='lm')
    else:
        d.text((x0, h // 2 + (14 if tag else 0)), left, font=M.fit(left, tf, fsize, maxw), fill=th['c1'], anchor='lm')
    return L

def usize(th, texts, start, maxw=860):
    tf = th['title'] if th['title'] != 'poppins_m' else 'poppins_b'
    return min(M.fit(t, tf, start, maxw).size for t in texts)

def page(th, title2, rows, t0, t1, label=None, footer=None):
    """Return layers visible from t0 to t1. rows: list of card images."""
    out = []
    c = lambda img, y, st: out.append((img, (W - img.width) // 2, int(y), st, t1))
    tf = th['title']
    a = M.text_img(title2[0], M.fit(title2[0], tf, 92, 980), th['c1']); c(a, 520, t0 + 0.1)
    b = M.text_img(title2[1], M.fit(title2[1], tf, 104, 980), th['c2']); c(b, 625, t0 + 0.4)
    y = 790
    if label:
        lb = M.text_img(label, M.F('poppins_b', 40), th['c2']); c(lb, y, t0 + 0.8); y += 80
    gap = 18
    for i, r in enumerate(rows):
        c(r, y, t0 + 1.0 + i * 0.45); y += r.height + gap
    if footer:
        f = M.text_img(footer, M.fit(footer, th['body'], 40, 980), th['c1']); c(f, min(y + 20, H - 230), t0 + 1.2 + len(rows) * 0.45)
    return out

def render(name, spec_pages, style, out_dir, dur):
    th = M.THEMES[style]; M._SHADOW[0] = th.get('shadow', True); seed = zlib.crc32(name.encode())
    layers = []
    for pg in spec_pages: layers += pg
    reveals = sorted(set(l[3] for l in layers))
    bg = M.base_background(th, seed); parts = M.Particles(th['particles'], seed)
    logo = Image.open(M.LOGO).convert('RGBA').resize((170, 170), Image.LANCZOS)
    wm = M.text_img('Forever Field Notes', M.F('poppins_b', 38), th['c1'])
    music = M.make_audio(th, dur, reveals, seed)
    out = os.path.join(out_dir, name + '.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', music, '-map', '0:v', '-map', '1:a', '-t', str(dur), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                          '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        s = i / FPS; z = 1 + 0.06 * s / dur; bw, bh = bg.size; cw, ch = int(bw / z), int(bh / z)
        fr = bg.crop(((bw - cw) // 2, (bh - ch) // 2, (bw - cw) // 2 + cw, (bh - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
        parts.draw(fr, s, th)
        fr.alpha_composite(logo, ((W - 170) // 2, 130)); fr.alpha_composite(wm, ((W - wm.width) // 2, 312))
        for img, x, y, st, end in layers:
            if s >= end: continue
            fade = min(1.0, (end - s) / 0.35) if end < dur else 1.0
            if fade < 1:
                im2 = img.copy(); im2.putalpha(im2.getchannel('A').point(lambda v, f=fade: int(v * f)))
                M.place(fr, im2, x, y, st, 0, s, th['anim'])
            else:
                M.place(fr, img, x, y, st, 0, s, th['anim'])
        if s > dur - 0.4: fr = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), fr, (dur - s) / 0.4)
        p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait(); os.remove(music); print(out, style, dur)
    return out

def zone_short(C, fac, z, style):
    rng, title, zones, dungeons, tip = z
    rows1 = [row_card(M.THEMES[style], n, r, sub=(note or None)) for n, r, note in zones][:6]
    t_split = 10.0 if dungeons else 13.0
    pages = [page(M.THEMES[style], (f'{fac.upper()} LEVELING', 'LEVELS ' + rng if rng != '1-10' else 'STARTING ZONES'), rows1, 0, t_split, label='WHERE TO QUEST')]
    dur = t_split
    if dungeons:
        rows2 = [row_card(M.THEMES[style], d[0], d[1], tag=('NEW IN FOREVER' if len(d) > 2 and d[2] else None)) for d in dungeons][:6]
        pages.append(page(M.THEMES[style], (f'{fac.upper()} LEVELS', rng + ' DUNGEONS'), rows2, t_split, t_split + 10.0, footer=tip))
        dur = t_split + 10.0
    return pages, dur + 0.0

def class_short(C, cls_slides_h, cls_slides_a, style):
    a, b = cls_slides_h  # class slide + order slide (Horde version)
    th = M.THEMES[style]
    races_h = ', '.join(C.RACES['Horde'][a['chapter']]); races_a = ', '.join(C.RACES['Alliance'][a['chapter']])
    fs = usize(th, a['why'], 44); p1rows = [row_card(th, w_, None, h=112, fsize=fs) for w_ in a['why']]
    p1 = page(th, (a['cls'] + ' LEVELING', a['spec'].upper() if len(a['spec']) < 16 else 'BEST SPEC'), p1rows, 0, 11,
              label=(a['spec'] if len(a['spec']) >= 16 else 'WHY THIS SPEC'))
    racerows = [row_card(th, 'Horde', None, sub=races_h, h=128), row_card(th, 'Alliance', None, sub=races_a, h=128)]
    # put races at the bottom of page 1
    y = 790 + 80 + len(p1rows) * 130 + 30
    for i, r in enumerate(racerows):
        p1.append((r, (W - r.width) // 2, y + i * 146, 2.6 + i * 0.4, 11))
    p2rows = [row_card(th, t, 'LVL ' + lv, h=118) for lv, t in a['miles']]
    p2 = page(th, (a['cls'], 'TALENT MILESTONES'), p2rows, 11, 22, label=a['mile_tree'])
    ot = [f'{i + 1}. {t}' for i, t in enumerate(b['order'])]; fs3 = usize(th, ot, 42); p3rows = [row_card(th, t, None, h=104, fsize=fs3) for t in ot]
    p3 = page(th, (a['cls'], b['title'].replace(a['cls'] + ' ', '')), p3rows, 22, 34, footer=b['tip'] if len(b['order']) <= 5 else None)
    return [p1, p2, p3], 34.0

if __name__ == '__main__':
    cdir, out_dir = sys.argv[1], sys.argv[2]; only = sys.argv[3] if len(sys.argv) > 3 else None
    sys.path.insert(0, cdir); import content as C
    os.makedirs(out_dir, exist_ok=True)
    jobs = []
    zstyles = {'Horde': ['ember', 'fel', 'dusk', 'ember', 'fel', 'dusk'], 'Alliance': ['frost', 'arcane', 'parchment', 'frost', 'arcane', 'parchment']}
    for fac in ('Horde', 'Alliance'):
        for i, z in enumerate(C.ZONES[fac]):
            nm = f'{fac.lower()}_levels_{z[0]}'
            jobs.append((nm, 'zone', fac, z, zstyles[fac][i]))
    cstyle = dict(Warrior='ember', Hunter='dusk', Mage='frost', Paladin='parchment', Priest='arcane', Rogue='fel', Shaman='frost', Warlock='fel', Druid='dusk')
    H_ = C.class_slides('Horde'); A_ = C.class_slides('Alliance')
    for k in range(0, len(H_), 2):
        cl = H_[k]['chapter']; jobs.append((f'class_{cl.lower()}', 'class', (H_[k], H_[k + 1]), (A_[k], A_[k + 1]), cstyle[cl]))
    for job in jobs:
        if only and job[0] != only: continue
        M._SHADOW[0] = M.THEMES[job[4]].get('shadow', True)
        if job[1] == 'zone':
            pages, dur = zone_short(C, job[2], job[3], job[4])
        else:
            pages, dur = class_short(C, job[2], job[3], job[4])
        render(job[0], pages, job[4], out_dir, dur)
