# Original solo-piano background music for the quest-window videos, in a gentle fantasy / tavern-ballad style.
# Fully synthesised here (no samples, no Blizzard music): additive piano with inharmonic partials, hammer
# noise, sustain-pedal style left hand, a generated melody in an A A' B A form, and a small hall reverb.
# A soft page whoosh still marks every line reveal.
import math, tempfile, wave
import numpy as np
from scipy.signal import fftconvolve

SR = 44100

# mode intervals, chord progression (scale degrees, one chord per bar), tempo, root (Hz), time signature
STYLES = {
    'dusk':      dict(root=146.83, mode=[0, 2, 3, 5, 7, 9, 10], prog=[0, 5, 2, 6, 0, 3, 4, 4], bpm=72, beats=3),   # D dorian
    'parchment': dict(root=130.81, mode=[0, 2, 4, 5, 7, 9, 11], prog=[0, 3, 4, 0, 5, 3, 1, 4], bpm=78, beats=3),   # C major
    'frost':     dict(root=164.81, mode=[0, 2, 3, 5, 7, 8, 10], prog=[0, 5, 2, 6, 0, 5, 3, 4], bpm=64, beats=4),   # E aeolian
    'fel':       dict(root=110.00, mode=[0, 1, 3, 5, 7, 8, 10], prog=[0, 1, 5, 0, 3, 1, 6, 0], bpm=66, beats=4),   # A phrygian
    'ember':     dict(root=123.47, mode=[0, 2, 3, 5, 7, 8, 11], prog=[0, 3, 4, 0, 5, 3, 4, 4], bpm=80, beats=3),   # B harmonic minor
    'arcane':    dict(root=138.59, mode=[0, 2, 4, 6, 7, 9, 11], prog=[0, 1, 4, 0, 5, 1, 3, 4], bpm=68, beats=4),   # C# lydian
}

_cache = {}

def _piano(freq, dur, vel):
    key = (round(freq, 2), round(dur, 2), round(vel, 2))
    if key in _cache: return _cache[key]
    n = int((dur + 0.05) * SR); t = np.arange(n) / SR
    B = 0.00035; v = np.zeros(n)
    bright = 0.55 + 0.45 * vel
    for k in range(1, 10):
        fk = freq * k * math.sqrt(1 + B * k * k)
        if fk > 9000: break
        amp = (1 / k ** 1.25) * (bright ** (k - 1))
        d1 = (1.2 + freq / 260) * (1 + 0.35 * k); d2 = (0.25 + freq / 1400) * (1 + 0.15 * k)
        env = 0.55 * np.exp(-t * d1) + 0.45 * np.exp(-t * d2)
        v += amp * env * np.sin(2 * np.pi * fk * t + k * 0.7)
    att = int(0.004 * SR); v[:att] *= np.linspace(0, 1, att)
    hl = int(0.012 * SR); hammer = np.random.default_rng(int(freq * 10)).normal(0, 1, hl) * np.exp(-np.arange(hl) / SR * 400) * 0.08
    v[:hl] += hammer
    rel = int(0.12 * SR); v[-rel:] *= np.linspace(1, 0, rel)
    v *= vel
    _cache[key] = v
    return v

def _hall(n_sec, seed):
    n = int(n_sec * SR); t = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    ir = rng.normal(0, 1, n) * np.exp(-t * 3.2)
    ir[:int(0.012 * SR)] = 0
    # darken the tail a little
    X = np.fft.rfft(ir); f = np.fft.rfftfreq(n, 1 / SR); X *= 1 / (1 + (f / 4500) ** 2)
    ir = np.fft.irfft(X, n); return ir / np.sqrt(np.sum(ir ** 2))

def _phrase(rng, prog, mode_len, beats):
    """4-bar melody: list of (bar, beat_offset, length_beats, scale_degree)."""
    rhythms3 = [[3], [2, 1], [1, 1, 1], [1, 2], [1.5, 0.5, 1]]
    rhythms4 = [[4], [2, 2], [1, 1, 2], [2, 1, 1], [3, 1], [1.5, 0.5, 2]]
    rh = rhythms3 if beats == 3 else rhythms4
    notes, cur = [], 4 + int(rng.integers(0, 3))
    for b in range(4):
        chord = prog[b]
        pat = rh[0] if b == 3 else rh[int(rng.integers(1, len(rh)))]
        pos = 0.0
        for i, ln in enumerate(pat):
            if i == 0:  # downbeat: nearest chord tone
                tones = [chord + x for x in (0, 2, 4, 7, 9, 11)]
                cur = min(tones, key=lambda d: abs(d - cur) + (0.5 if d == cur else 0))
            else:
                cur += int(rng.choice([-2, -1, -1, 1, 1, 2]))
            cur = max(2, min(11, cur))
            if b == 3: cur = chord + 7 if abs(chord + 7 - cur) < abs(chord - cur) else max(chord, 2)
            notes.append((b, pos, ln, cur)); pos += ln
    return notes

def make_audio(style, dur, reveals, seed):
    s = STYLES.get(style, STYLES['dusk']); rng = np.random.default_rng(seed)
    beat = 60 / s['bpm']; beats = s['beats']; bar = beat * beats
    n = int(dur * SR) + 1; dry = np.zeros((n, 2))
    mode = s['mode']
    def hz(deg, octv=0):
        return s['root'] * 2 ** ((mode[deg % 7] + 12 * (deg // 7 + octv)) / 12)
    def put(sig, start, pan):
        st = int(start * SR)
        if st >= n: return
        ln = min(len(sig), n - st)
        dry[st:st + ln, 0] += sig[:ln] * (1 - pan) ; dry[st:st + ln, 1] += sig[:ln] * pan
    prog = s['prog']
    A = _phrase(rng, prog[:4], 7, beats); A2 = list(A[:-1]) + [(3, 0.0, beats, prog[3] + 7)]
    Bp = _phrase(rng, prog[4:], 7, beats)
    form = [(A, prog[:4]), (A2, prog[:4]), (Bp, prog[4:]), (A, prog[:4])]
    nbars = int(math.ceil(dur / bar)) + 1
    start = 0.4
    for blk in range(0, nbars, 4):
        mel, chords = form[(blk // 4) % 4]
        t0 = start + blk * bar
        if t0 > dur: break
        for b in range(4):
            tb = t0 + b * bar
            if tb > dur: break
            c = chords[b]
            # left hand: low root, then a gentle broken chord, held like a sustain pedal
            lh = [(0, c, -2, 0.50), (1, c + 4, -1, 0.34), (2, c + 7, -1, 0.30)] if beats == 3 else \
                 [(0, c, -2, 0.50), (1, c + 4, -1, 0.32), (2, c + 7, -1, 0.30), (3, c + 9, -1, 0.26)]
            for bt, deg, octv, vel in lh:
                put(_piano(hz(deg, octv), bar * 1.25 - bt * beat, vel * (0.9 + 0.2 * rng.random())), tb + bt * beat, 0.42)
        # right hand melody (skip the very first block's first bar so it breathes in)
        for b, pos, ln, deg in mel:
            tn = t0 + b * bar + pos * beat
            if tn > dur - 0.8 or (blk == 0 and b == 0 and pos == 0 and False): continue
            vel = 0.62 + 0.18 * rng.random()
            put(_piano(hz(deg, 0), max(0.6, ln * beat * 1.6), vel), tn + 0.006 * rng.random(), 0.58)
    # hall reverb
    wet = np.stack([fftconvolve(dry[:, 0], _hall(2.4, seed + 1))[:n], fftconvolve(dry[:, 1], _hall(2.4, seed + 2))[:n]], axis=1)
    out = dry * 0.78 + wet * 0.42
    # soft page whoosh on each reveal
    wl = int(0.35 * SR)
    for r in reveals:
        noise = rng.normal(0, 1, wl)
        X = np.fft.rfft(noise); f = np.fft.rfftfreq(wl, 1 / SR)
        X *= (1 / (1 + (700 / np.maximum(f, 1)) ** 4)) * (1 / (1 + (f / 5000) ** 4))
        w = np.fft.irfft(X, wl) * np.sin(np.linspace(0, np.pi, wl)) ** 2
        w = w / (np.max(np.abs(w)) + 1e-9) * 0.09
        st = int(max(0, r - 0.1) * SR); ln = min(wl, n - st)
        if ln > 0: out[st:st + ln, 0] += w[:ln]; out[st:st + ln, 1] += w[:ln] * 0.9
    fi, fo = int(0.3 * SR), int(1.2 * SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]; out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    out = np.tanh(out * 1.1); out /= (np.max(np.abs(out)) + 1e-9); out *= 0.8
    pcm = (out * 32767).astype(np.int16)
    path = tempfile.mktemp(suffix='.wav')
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
    return path
