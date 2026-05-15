import numpy as np

SAMPLE_RATE = 44100


def sine(freq, duration, amplitude=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return amplitude * np.sin(2 * np.pi * freq * t)


def sawtooth(freq, duration, amplitude=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    phase = (t * freq) % 1.0
    return amplitude * (2 * phase - 1)


def square(freq, duration, amplitude=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return amplitude * np.sign(np.sin(2 * np.pi * freq * t))


def adsr(signal, attack=0.01, decay=0.1, sustain=0.7, release=0.1):
    n = len(signal)
    env = np.ones(n) * sustain
    a = min(int(attack * SAMPLE_RATE), n)
    d = min(int(decay * SAMPLE_RATE), n - a)
    r = min(int(release * SAMPLE_RATE), n)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if d > 0:
        env[a:a + d] = np.linspace(1, sustain, d)
    if r > 0:
        env[n - r:] *= np.linspace(1, 0, r)
    return signal * env


def mix(*signals):
    n = max(len(s) for s in signals)
    out = np.zeros(n)
    for s in signals:
        out[:len(s)] += s
    return out
