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
        if self._xLoc <= self._radius or self._xLoc >= 800 - self._radius:
            self._xSpd = -self._xSpd
        if self._yLoc <= self._radius \
                or brickwall.collide(self) or paddle.collide(self):
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
        has_collided = (not ball.get_collision_state()
                        and (ball._xLoc + ball._radius) >= self._xLoc
                        and (ball._xLoc - ball._radius) <= (self._xLoc + self._width)
                        and (ball._yLoc + ball._radius) >= self._yLoc
                        and (ball._yLoc - ball._radius) <= (self._yLoc + self._height))
        if has_collided:
            ball.set_collision_state(1)
            self._vanishingStep = 1
        return has_collided
        # TODO : handle collisions from the side


class BrickGroup:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._bricks = []

    def collide(self, ball):
        if ball.get_collision_state():
            return False
        result = False
        # todo : sort bricks by distance to ball
        for brick in self._bricks:
            if brick.collide(ball):
                result = True
        return result

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
