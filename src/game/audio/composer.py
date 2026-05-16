import numpy as np
from game.audio.synth import fm, sawtooth, square, sine, overdrive, adsr, mix, SAMPLE_RATE
from game.audio.profiles.synth_profiles import SYNTH_PROFILES
from game.audio.profiles.compose_profiles import COMPOSE_PROFILES

NOTE_FRACTIONS = {"whole": 1, "half": 2, "4th": 4, "8th": 8, "16th": 16}


def _note_duration(beat, fraction_name):
    return beat * 4 / NOTE_FRACTIONS[fraction_name]


def _sine_vibrato(freq, duration, amplitude):
    n = int(SAMPLE_RATE * duration)
    t = np.arange(n) / SAMPLE_RATE
    vibrato = 1 + 0.002 * np.sin(2 * np.pi * 5.5 * t)
    phase = np.cumsum(2 * np.pi * freq * vibrato / SAMPLE_RATE)
    return amplitude * np.sin(phase)


def _generate_note(freq, duration, voice_params):
    osc = voice_params["osc"]
    amp = voice_params.get("amplitude", 0.4)

    if osc == "fm":
        sig = fm(freq, duration,
                 mod_ratio=voice_params.get("mod_ratio", 2.0),
                 mod_index=voice_params.get("mod_index", 3.0),
                 amplitude=amp)
        if "overdrive" in voice_params:
            sig = overdrive(sig, voice_params["overdrive"])
        sig *= voice_params.get("post_gain", 1.0)
    elif osc == "sawtooth":
        sig = sawtooth(freq, duration, amp)
    elif osc == "square":
        sig = square(freq, duration, amp)
    elif osc == "sine":
        sig = sine(freq, duration, amp)
    elif osc == "sine_vibrato":
        sig = _sine_vibrato(freq, duration, amp)
    else:
        sig = sine(freq, duration, amp)

    if "adsr" in voice_params:
        sig = adsr(sig, **voice_params["adsr"])
    return sig


def _make_kick():
    n = int(SAMPLE_RATE * 0.15)
    t = np.arange(n) / SAMPLE_RATE
    phase = np.cumsum(2 * np.pi * 150 * np.exp(-t * 40) / SAMPLE_RATE)
    return np.sin(phase) * np.exp(-t * 25) * 0.7


def _make_hihat():
    n = int(SAMPLE_RATE * 0.04)
    t = np.arange(n) / SAMPLE_RATE
    return (np.random.random(n) * 2 - 1) * np.exp(-t * 100) * 0.2


def _build_voice(voice_name, voice_cfg, synth_voice, notes_map, beat, chords):
    note_dur = _note_duration(beat, voice_cfg["note_dur"])
    cycling = voice_cfg.get("cycle", False)
    parts = []

    for chord in chords:
        note_names = chord[voice_name]
        if cycling:
            n_steps = round(_note_duration(beat, "whole") / note_dur)
            bar = [_generate_note(notes_map[note_names[i % len(note_names)]], note_dur, synth_voice)
                   for i in range(n_steps)]
        else:
            bar = [_generate_note(notes_map[n], note_dur, synth_voice) for n in note_names]
        parts.append(np.concatenate(bar))

    return np.concatenate(parts)


def _build_pad(synth_voice, notes_map, beat, chords):
    bar_dur = beat * 4
    parts = []
    for chord in chords:
        voices = [_generate_note(notes_map[n], bar_dur, synth_voice) for n in chord["pad"]]
        parts.append(mix(*voices))
    return np.concatenate(parts)


def _build_percussion(beat, n_chords):
    bar_dur = beat * 4
    n_total = int(SAMPLE_RATE * bar_dur * n_chords)
    kick_buf = np.zeros(n_total)
    hat_buf = np.zeros(n_total)
    kick = _make_kick()
    hat = _make_hihat()
    eighth_samples = int(SAMPLE_RATE * beat / 2)

    for bar_idx in range(n_chords):
        bar_start = int(bar_idx * SAMPLE_RATE * bar_dur)
        for step in range(8):
            pos = bar_start + step * eighth_samples
            if step in (0, 4):
                end = min(pos + len(kick), n_total)
                kick_buf[pos:end] += kick[:end - pos]
            end = min(pos + len(hat), n_total)
            hat_buf[pos:end] += hat[:end - pos]

    return kick_buf + hat_buf


def build_loop(synth="megadrive", compose="thunderforce"):
    synth_profile = SYNTH_PROFILES[synth]
    compose_profile = COMPOSE_PROFILES[compose]

    beat = 60.0 / compose_profile["bpm"]
    notes_map = compose_profile["notes"]
    chords = compose_profile["chords"]
    voices_cfg = compose_profile["voices"]

    # Fail early with a clear message listing all missing notes
    used = {n for chord in chords for voice in chord.values()
            if isinstance(voice, list) for n in voice}
    missing = used - notes_map.keys()
    if missing:
        raise KeyError(f"Notes missing from profile notes dict: {sorted(missing)}")

    signals = []

    for voice_name, voice_cfg in voices_cfg.items():
        if voice_name == "percussion":
            if voice_cfg:
                signals.append(_build_percussion(beat, len(chords)))
            continue
        if voice_name not in synth_profile:
            continue
        synth_voice = synth_profile[voice_name]
        if voice_name == "pad":
            signals.append(_build_pad(synth_voice, notes_map, beat, chords))
        else:
            signals.append(_build_voice(voice_name, voice_cfg, synth_voice, notes_map, beat, chords))

    combined = mix(*signals)
    peak = np.max(np.abs(combined))
    if peak > 0:
        combined = combined / peak * 0.85
    stereo = np.column_stack([combined, combined])
    return (stereo * 32767).astype(np.int16)
