_LEVELS = [1, 2, 4, 8, 16]


class SpeedController:
    def __init__(self):
        self._idx = 0

    @property
    def value(self):
        return _LEVELS[self._idx]

    def up(self):
        self._idx = min(self._idx + 1, len(_LEVELS) - 1)

    def down(self):
        self._idx = max(self._idx - 1, 0)
