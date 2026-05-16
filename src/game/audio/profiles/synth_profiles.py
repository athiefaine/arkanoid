"""
Synth profiles — define HOW each voice sounds.

Each profile is a dict of voice_name -> oscillator params.
Recognized oscillator types: "fm", "sawtooth", "square", "sine", "sine_vibrato".
"""

SYNTH_PROFILES = {
    "megadrive": {
        "lead": {
            "osc": "fm", "mod_ratio": 2.0, "mod_index": 5.0,
            "overdrive": 1.8, "amplitude": 0.7,
            "adsr": {"attack": 0.004, "decay": 0.06, "sustain": 0.55, "release": 0.04},
            "post_gain": 0.35,
        },
        "bass": {
            "osc": "fm", "mod_ratio": 1.0, "mod_index": 2.5, "amplitude": 0.5,
            "adsr": {"attack": 0.005, "decay": 0.08, "sustain": 0.45, "release": 0.05},
        },
        "arp": {
            "osc": "square", "amplitude": 0.2,
            "adsr": {"attack": 0.002, "decay": 0.03, "sustain": 0.25, "release": 0.015},
        },
    },

    # Slow legato lead over fast bass — pair with "hunger_desperate"
    "megadrive_legato": {
        "lead": {
            "osc": "fm", "mod_ratio": 1.0, "mod_index": 2.5,
            "amplitude": 0.7,
            "adsr": {"attack": 0.015, "decay": 0.12, "sustain": 0.85, "release": 0.15},
            "post_gain": 0.45,
        },
        "bass": {
            "osc": "fm", "mod_ratio": 2.0, "mod_index": 3.0, "amplitude": 0.5,
            "adsr": {"attack": 0.003, "decay": 0.04, "sustain": 0.4, "release": 0.02},
        },
        "arp": {
            "osc": "square", "amplitude": 0.08,
            "adsr": {"attack": 0.002, "decay": 0.02, "sustain": 0.1, "release": 0.01},
        },
    },

    # Pair with "hunger_desperate" compose profile
    "megadrive_fierce": {
        "lead": {
            "osc": "fm", "mod_ratio": 2.0, "mod_index": 3.5,
            "overdrive": 1.5, "amplitude": 0.7,
            "adsr": {"attack": 0.003, "decay": 0.05, "sustain": 0.6, "release": 0.03},
            "post_gain": 0.35,
        },
        "bass": {
            "osc": "fm", "mod_ratio": 1.0, "mod_index": 2.0, "amplitude": 0.5,
            "adsr": {"attack": 0.003, "decay": 0.07, "sustain": 0.5, "release": 0.04},
        },
        "arp": {
            "osc": "square", "amplitude": 0.15,
            "adsr": {"attack": 0.001, "decay": 0.025, "sustain": 0.2, "release": 0.01},
        },
    },

    "synthwave": {
        "lead": {
            "osc": "sine_vibrato", "amplitude": 0.45,
            "adsr": {"attack": 0.02, "decay": 0.1, "sustain": 0.85, "release": 0.15},
            "post_gain": 1.0,
        },
        "bass": {
            "osc": "sawtooth", "amplitude": 0.5,
            "adsr": {"attack": 0.02, "decay": 0.15, "sustain": 0.5, "release": 0.2},
        },
        "arp": {
            "osc": "square", "amplitude": 0.1,
            "adsr": {"attack": 0.005, "decay": 0.04, "sustain": 0.3, "release": 0.04},
        },
        "pad": {
            "osc": "sine_vibrato", "amplitude": 0.15,
            "adsr": {"attack": 0.4, "decay": 0.1, "sustain": 0.75, "release": 0.4},
        },
    },
}
