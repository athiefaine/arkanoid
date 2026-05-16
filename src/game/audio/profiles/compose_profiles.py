"""
Compose profiles — define WHAT is played.

Each profile specifies:
  - bpm, voices active, note durations
  - chords: list of bars, each bar contains note lists per voice

Note durations: "whole", "half", "4th", "8th", "16th"
"""

# --- D natural minor: D E F G A Bb C ---
_TF_NOTES = {
    'Bb1': 58.27,  'C2': 65.41,  'D2': 73.42,  'F2': 87.31,
    'G2':  98.00,  'A2': 110.00, 'Bb2': 116.54, 'C3': 130.81,
    'D3': 146.83,  'E3': 164.81, 'F3': 174.61,  'G3': 196.00,
    'A3': 220.00,  'Bb3': 233.08, 'C4': 261.63, 'D4': 293.66,
    'E4': 329.63,  'F4': 349.23, 'G4': 392.00,  'A4': 440.00,
    'Bb4': 466.16, 'C5': 523.25, 'D5': 587.33,  'E5': 659.25,
    'F5': 698.46,  'G5': 784.00, 'A5': 880.00,
}

# --- A natural minor: A B C D E F G ---
_SW_NOTES = {
    'A1': 55.00,   'C2': 65.41,  'F1': 43.65,  'G1': 49.00,
    'A2': 110.00,  'C3': 130.81, 'E3': 164.81,  'G3': 196.00,
    'F2': 87.31,   'G2': 98.00,  'B2': 123.47,  'D3': 146.83,
    'A3': 220.00,  'C4': 261.63, 'E4': 329.63,  'G4': 392.00,
    'F3': 174.61,  'B3': 246.94, 'D4': 293.66,
    'A4': 440.00,  'F4': 349.23, 'C5': 523.25,
}

COMPOSE_PROFILES = {
    "shmup": {
        "bpm": 160,
        "notes": _TF_NOTES,
        "voices": {
            "lead":       {"note_dur": "8th"},
            "bass":       {"note_dur": "8th"},
            "arp":        {"note_dur": "16th", "cycle": True},
            "percussion": True,
        },
        "chords": [
            {   # Dm
                "bass": ['D2','A2','D2','A2','D2','A2','G2','A2'],
                "arp":  ['D3','F3','A3','D4'],
                "lead": ['D5','F5','A5','G5','F5','D5','C5','D5'],
            },
            {   # C
                "bass": ['C2','G2','C2','G2','C2','G2','F2','G2'],
                "arp":  ['C3','E3','G3','C4'],
                "lead": ['C5','E5','G5','F5','E5','C5','Bb4','C5'],
            },
            {   # Bb
                "bass": ['Bb1','F2','Bb1','F2','Bb1','F2','C2','Bb1'],
                "arp":  ['Bb2','D3','F3','Bb3'],
                "lead": ['Bb4','D5','F5','D5','C5','Bb4','A4','Bb4'],
            },
            {   # C → Dm
                "bass": ['C2','G2','A2','G2','C2','D2','A2','D2'],
                "arp":  ['C3','E3','G3','C4'],
                "lead": ['C5','Bb4','A4','G4','A4','C5','D5','A4'],
            },
        ],
    },

    # --- Slow, atmospheric, synthwave style ---
    "ambient": {
        "bpm": 110,
        "notes": _SW_NOTES,
        "voices": {
            "bass": {"note_dur": "8th"},
            "arp":  {"note_dur": "8th", "cycle": True},
            "pad":  {"note_dur": "whole"},
        },
        "chords": [
            {   # Am
                "bass": ['A1','A1','A1','A1','A1','A1','A1','A1'],
                "arp":  ['A3','C4','E4','A4'],
                "pad":  ['A2','C3','E3','A3'],
            },
            {   # F
                "bass": ['F1','F1','F1','F1','F1','F1','F1','F1'],
                "arp":  ['F3','A3','C4','F4'],
                "pad":  ['F2','A2','C3','F3'],
            },
            {   # C
                "bass": ['C2','C2','C2','C2','C2','C2','C2','C2'],
                "arp":  ['C4','E4','G4','C5'],
                "pad":  ['C3','E3','G3','C4'],
            },
            {   # G
                "bass": ['G1','G1','G1','G1','G1','G1','G1','G1'],
                "arp":  ['G3','B3','D4','G4'],
                "pad":  ['G2','B2','D3','G3'],
            },
        ],
    },

    "shmup_pressure": {
        "bpm": 160,
        "notes": {
            'F#1': 46.25, 'A1':  55.00,
            'C#2': 69.30, 'D2':  73.42,  'F#2': 92.50,  'G#2': 103.83, 'A2': 110.00,
            'B2':  123.47, 'C#3': 138.59, 'D3':  146.83, 'F#3': 185.00,
            'G#3': 207.65, 'A3':  220.00, 'B3':  246.94,
            'C#4': 277.18, 'D4':  293.66, 'E4':  329.63,
            'F#4': 369.99, 'G#4': 415.30, 'A4':  440.00,
            'B4':  493.88, 'C#5': 554.37,
        },
        "voices": {
            "lead":       {"note_dur": "half"},
            "bass":       {"note_dur": "16th", "cycle": True},
            "arp":        {"note_dur": "16th", "cycle": True},
            "percussion": True,
        },
        "chords": [
            {   # F#m (i) — leap up a minor 3rd
                "bass": ['F#1', 'F#2'],
                "arp":  ['F#3', 'A3', 'C#4', 'F#4'],
                "lead": ['F#4', 'A4'],
            },
            {   # F#m (i) — high point then fall
                "bass": ['F#1', 'F#2'],
                "arp":  ['A3', 'C#4', 'F#4', 'A4'],
                "lead": ['C#5', 'A4'],
            },
            {   # C#m (v) — tension, falling 3rd
                "bass": ['C#2', 'F#2'],
                "arp":  ['C#4', 'E4', 'G#4', 'C#5'],
                "lead": ['G#4', 'E4'],
            },
            {   # F#m (i) — 4th leap up, energy
                "bass": ['F#1', 'F#2'],
                "arp":  ['F#3', 'A3', 'C#4', 'F#4'],
                "lead": ['B3', 'F#4'],
            },
            {   # A (III — relative major, brightness)
                "bass": ['A1', 'A2'],
                "arp":  ['A3', 'C#4', 'E4', 'A4'],
                "lead": ['A4', 'E4'],
            },
            {   # D (bVI) — 5th leap, open and strong
                "bass": ['D2', 'A2'],
                "arp":  ['D3', 'F#3', 'A3', 'D4'],
                "lead": ['D4', 'A4'],
            },
            {   # Chromatic walk: C# → B → A → G# (signature of the original)
                "bass": ['C#2', 'B2', 'A2', 'G#2'],
                "arp":  ['C#4', 'B3', 'A3', 'G#3'],
                "lead": ['C#4', 'B3'],
            },
            {   # F#m (i) — resolution, settle home
                "bass": ['F#1', 'F#2'],
                "arp":  ['F#3', 'A3', 'C#4', 'F#4'],
                "lead": ['A4', 'F#4'],
            },
        ],
    },
}
