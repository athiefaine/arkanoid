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


def fm(freq, duration, mod_ratio=2.0, mod_index=3.0, amplitude=0.5):
    """2-operator FM synthesis — simulates YM2612 metallic/aggressive tones."""
    n = int(SAMPLE_RATE * duration)
    t = np.arange(n) / SAMPLE_RATE
    modulator = mod_index * np.sin(2 * np.pi * freq * mod_ratio * t)
    return amplitude * np.sin(2 * np.pi * freq * t + modulator)


def overdrive(signal, gain=3.0):
    """Hard clipping — simulates the YM2612 DAC saturation."""
    return np.clip(signal * gain, -1.0, 1.0)


def noise(duration, amplitude=0.5):
    n = int(SAMPLE_RATE * duration)
    return amplitude * (np.random.random(n) * 2 - 1)


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
