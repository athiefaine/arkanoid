import numpy as np
from game.audio.synth import sine, sawtooth, square, adsr, mix, SAMPLE_RATE

BPM = 110
BEAT = 60.0 / BPM
BAR = 4 * BEAT

NOTES = {
    'A1': 55.00, 'F1': 43.65, 'C2': 65.41, 'G1': 49.00,
    'A2': 110.00, 'C3': 130.81, 'E3': 164.81, 'G3': 196.00,
    'F2': 87.31,  'G2': 98.00,  'B2': 123.47, 'D3': 146.83,
    'A3': 220.00, 'C4': 261.63, 'E4': 329.63, 'G4': 392.00,
    'F3': 174.61, 'B3': 246.94, 'D4': 293.66,
    'A4': 440.00, 'F4': 349.23, 'C5': 523.25,
}

# Am → F → C → G
CHORDS = [
    {'bass': 'A1', 'arp': ['A3', 'C4', 'E4', 'A4'], 'pad': ['A2', 'C3', 'E3', 'A3']},
    {'bass': 'F1', 'arp': ['F3', 'A3', 'C4', 'F4'], 'pad': ['F2', 'A2', 'C3', 'F3']},
    {'bass': 'C2', 'arp': ['C4', 'E4', 'G4', 'C5'], 'pad': ['C3', 'E3', 'G3', 'C4']},
    {'bass': 'G1', 'arp': ['G3', 'B3', 'D4', 'G4'], 'pad': ['G2', 'B2', 'D3', 'G3']},
]


def _build_bass():
    parts = []
    for chord in CHORDS:
        sig = sawtooth(NOTES[chord['bass']], BAR, amplitude=0.5)
        sig = adsr(sig, attack=0.02, decay=0.15, sustain=0.5, release=0.2)
        parts.append(sig)
    return np.concatenate(parts)


def _build_arp():
    eighth = BEAT / 2
    parts = []
    for chord in CHORDS:
        notes = chord['arp']
        bar = []
        for i in range(8):
            freq = NOTES[notes[i % len(notes)]]
            sig = square(freq, eighth, amplitude=0.2)
            sig = adsr(sig, attack=0.005, decay=0.04, sustain=0.4, release=0.04)
            bar.append(sig)
        parts.append(np.concatenate(bar))
    return np.concatenate(parts)


def _build_pad():
    parts = []
    for chord in CHORDS:
        voices = []
        for note_name in chord['pad']:
            freq = NOTES[note_name]
            n = int(SAMPLE_RATE * BAR)
            t = np.arange(n) / SAMPLE_RATE
            vibrato = 1 + 0.002 * np.sin(2 * np.pi * 5.5 * t)
            phase = np.cumsum(2 * np.pi * freq * vibrato / SAMPLE_RATE)
            sig = 0.15 * np.sin(phase)
            sig = adsr(sig, attack=0.4, decay=0.1, sustain=0.75, release=0.4)
            voices.append(sig)
        parts.append(mix(*voices))
    return np.concatenate(parts)


def build_loop():
    combined = mix(_build_bass(), _build_arp(), _build_pad())
    peak = np.max(np.abs(combined))
    if peak > 0:
        combined = combined / peak * 0.85
    stereo = np.column_stack([combined, combined])
    return (stereo * 32767).astype(np.int16)
