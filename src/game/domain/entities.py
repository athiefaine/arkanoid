BALL_SPEED = 8
BRICK_WIDTH = 40
BRICK_HEIGHT = 16


class Ball:
    def __init__(self, radius, x, y):
        self._radius = radius
        self._xLoc = x
        self._yLoc = y
        self._xSpd = BALL_SPEED
        self._ySpd = -BALL_SPEED
        self._collisionState = 0

    def get_collision_state(self):
        return self._collisionState

    def set_collision_state(self, value):
        self._collisionState = value

    def update(self, brickwall, paddle):
        if self._collisionState and self._collisionState < 5:
            self._collisionState += 1
        else:
            self._collisionState = 0
        self._xLoc += self._xSpd
        self._yLoc += self._ySpd
        x_wall = self._xLoc <= self._radius or self._xLoc >= 800 - self._radius
        if x_wall:
            self._xSpd = -self._xSpd
        if self._yLoc <= self._radius or paddle.collide(self):
            self._ySpd = -self._ySpd
        brick_col = brickwall.collide(self)
        if brick_col == 'v':
            self._ySpd = -self._ySpd
        elif brick_col == 'h':
            if not x_wall:  # wall already reversed xSpd this frame — don't cancel it
                self._xSpd = -self._xSpd
            self._ySpd = -self._ySpd


class Paddle:
    def __init__(self, width, height, x, y):
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y

    def update(self, ball):
        self._xLoc = ball._xLoc - (self._width / 2)

    def collide(self, ball):
        return ((ball._xLoc + ball._radius) >= self._xLoc
                and (ball._xLoc - ball._radius) <= (self._xLoc + self._width)
                and (ball._yLoc + ball._radius) >= self._yLoc
                and (ball._yLoc - ball._radius) <= (self._yLoc + self._height))


class Brick:
    def __init__(self, color, width, height, x, y):
        self._color = color
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y
        self._vanishingStep = 0

    def update(self):
        if self._vanishingStep > 0:
            self._vanishingStep += 1

    def collide(self, ball):
        if ball.get_collision_state():
            return None
        dx_left  = (ball._xLoc + ball._radius) - self._xLoc
        dx_right = (self._xLoc + self._width)  - (ball._xLoc - ball._radius)
        dy_top   = (ball._yLoc + ball._radius) - self._yLoc
        dy_bottom = (self._yLoc + self._height) - (ball._yLoc - ball._radius)
        if dx_left <= 0 or dx_right <= 0 or dy_top <= 0 or dy_bottom <= 0:
            return None
        ball.set_collision_state(1)
        self._vanishingStep = 1
        if min(dx_left, dx_right) < min(dy_top, dy_bottom):
            return 'h'
        return 'v'


class BrickGroup:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._bricks = []

    def collide(self, ball):
        if ball.get_collision_state():
            return None
        by_distance = sorted(
            self._bricks,
            key=lambda b: (b._xLoc + b._width / 2 - ball._xLoc) ** 2
                        + (b._yLoc + b._height / 2 - ball._yLoc) ** 2
        )
        for brick in by_distance:
            col = brick.collide(ball)
            if col is not None:
                return col
        return None

    def update(self):
        for brick in self._bricks:
            brick.update()
        self._bricks = [b for b in self._bricks if b._vanishingStep <= 30]


class BrickWall(BrickGroup):
    def __init__(self, x, y, width, height, colors):
        super().__init__(x, y, width, height)
        for row in range(self._height):
            for col in range(self._width):
                self._bricks.append(Brick(
                    colors[row], BRICK_WIDTH, BRICK_HEIGHT,
                    self._x + col * BRICK_WIDTH,
                    self._y + BRICK_HEIGHT * row
                ))
