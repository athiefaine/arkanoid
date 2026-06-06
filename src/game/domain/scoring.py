POINTS_PER_BRICK   = 100
MULTIPLIER_PER_HIT = 0.1
MULTIPLIER_PER_MISS = 0.5
MULTIPLIER_MIN     = 1.0


class ScoreTracker:
    def __init__(self):
        self.score = 0
        self.multiplier = MULTIPLIER_MIN
        self._brick_since_paddle = False

    def on_brick_hit(self):
        self.multiplier += MULTIPLIER_PER_HIT
        self._brick_since_paddle = True
        self.score += round(POINTS_PER_BRICK * self.multiplier)

    def on_paddle_hit(self):
        if not self._brick_since_paddle:
            self.multiplier = max(MULTIPLIER_MIN, self.multiplier - MULTIPLIER_PER_MISS)
        self._brick_since_paddle = False

    def on_ball_lost(self):
        self.multiplier = MULTIPLIER_MIN
        self._brick_since_paddle = False
