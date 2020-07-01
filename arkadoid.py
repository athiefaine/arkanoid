import math
import pygame
import pygame.gfxdraw
import sys

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BRICK_COLORS = [
    (255, 77, 77),
    (0, 102, 255),
    (0, 153, 51),
    (255, 102, 153),
    (255, 102, 0)
]

BRICK_OUTLINE = (192, 192, 192)
BRICK_OUTLINE2 = (64, 64, 64)

BALL_OUTLINE = (128, 128, 128)

BALL_COLOR = (204, 204, 204)

# ball constants
BALL_SPEED = 8
BALL_RADIUS = 5

NO_COLLIDE = 0
H_COLLIDE = 10
V_COLLIDE = 20

# brick constants
BRICK_WIDTH = 40
BRICK_HEIGHT = 16

pygame.init()

size = (1024, 768)

screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)

screen.fill(BLACK)


class Ball(object):
    def __init__(self, screen, radius, x, y):
        self.__screen = screen
        self._radius = radius
        self._xLoc = x
        self._yLoc = y
        self._xSpd = BALL_SPEED
        self._ySpd = -BALL_SPEED

    def draw(self):
        pygame.draw.circle(screen, BALL_OUTLINE, (self._xLoc, self._yLoc), self._radius, 1)
        pygame.draw.circle(screen, BALL_COLOR, (self._xLoc, self._yLoc), self._radius - 1, 0)

    def update(self, brickwall, Paddle):
        self._xLoc += self._xSpd
        self._yLoc += self._ySpd
        if self._xLoc <= self._radius or self._xLoc >= 800 - self._radius:
            self._xSpd = -self._xSpd
        if self._yLoc <= self._radius \
                or brickwall.collide(self) or paddle.collide(self):
            self._ySpd = -self._ySpd


class Paddle(object):
    def __init__(self, screen, color, width, height, x, y):
        self.__screen = screen
        self._color = color
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y

    def draw(self):
        # pygame.draw.rect(screen, self._color, (self._xLoc,self._yLoc,self._width,self._height),0)
        pygame.draw.line(screen, self._color, (self._xLoc, self._yLoc), (self._xLoc + self._width, self._yLoc), 1)
        pygame.draw.line(screen, BLACK, (self._xLoc + int(self._width / 4), self._yLoc),
                         (self._xLoc + self._width - int(self._width / 4), self._yLoc), 1)
        for i in range(1, int(self._height / 2) + 1):
            gradient_step = i * -30
            r = max(0, min(255, self._color[0] + gradient_step))
            g = max(0, min(255, self._color[1] + gradient_step))
            b = max(0, min(255, self._color[2] + gradient_step))
            cut = i * 1
            pygame.draw.line(screen, (r, g, b), \
                             (self._xLoc + cut, self._yLoc + i), (self._xLoc + self._width - cut, self._yLoc + i), 1)
            pygame.draw.line(screen, (r, g, b), \
                             (self._xLoc + cut, self._yLoc - i), (self._xLoc + self._width - cut, self._yLoc - i), 1)

    def update(self, ball):
        self._xLoc = ball._xLoc - (self._width / 2)


    def collide(self, ball):
        paddleX = self._xLoc
        paddleY = self._yLoc
        paddleW = self._width
        paddleH = self._height
        ballX = ball._xLoc
        ballY = ball._yLoc
        radius = ball._radius

        return ((ballX + radius) >= paddleX and (ballX - radius) <= (paddleX + paddleW)) \
               and ((ballY + radius) >= paddleY and (ballY - radius) <= (paddleY + paddleH))


class Brick(pygame.sprite.Sprite):
    def __init__(self, screen, color, width, height, x, y):
        self.__screen = screen
        self._color = color
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y
        self._vanishingStep = 0

    def draw(self):
        for i in range(self._width):
            gradient_step = i * 1
            r = min(255, self._color[0] + gradient_step)
            g = min(255, self._color[1] + gradient_step)
            b = min(255, self._color[2] + gradient_step)
            pygame.draw.line(screen, (r, g, b), \
                             (self._xLoc + i, self._yLoc), (self._xLoc + i, self._yLoc + self._height), 1)
        pygame.draw.rect(screen, BRICK_OUTLINE2, (self._xLoc, self._yLoc, self._width, self._height), 2)
        pygame.draw.line(screen, BRICK_OUTLINE, (self._xLoc + 1, self._yLoc + 1),
                         (self._xLoc + self._width - 2, self._yLoc + 1), 2)
        pygame.draw.line(screen, BRICK_OUTLINE, (self._xLoc + 1, self._yLoc + 2),
                         (self._xLoc + 1, self._yLoc + self._height - 2), 2)
        if self._vanishingStep > 0:
            vanish_padding = 4
            for y in range(int(self._height / vanish_padding) + 1):
                pygame.gfxdraw.box(screen, (
                    self._xLoc, self._yLoc + vanish_padding * y, self._width, int(self._vanishingStep / 6)),
                                   (0, 0, 0, 255))

            self._vanishingStep += 1

    def collide(self, ball):
        brickX = self._xLoc
        brickY = self._yLoc
        brickW = self._width
        brickH = self._height
        ballX = ball._xLoc
        ballY = ball._yLoc
        radius = ball._radius

        hasCollided = ((ballX + radius) >= brickX and (ballX - radius) <= (brickX + brickW)) and (
                (ballY + radius) >= brickY and (ballY - radius) <= (brickY + brickH))
        if hasCollided:
            self._vanishingStep = 1
        return hasCollided
        # TODO : handle collisions from the side


class BrickGroup(pygame.sprite.Group):
    def __init__(self, screen, x, y, width, height):
        self.__screen = screen
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._bricks = []

    def collide(self, ball):
        for brick in self._bricks:
            if brick is not None and brick.collide(ball):
                return True
        return False

    def update(self, ball):
        for i in range(len(self._bricks)):
            if (self._bricks[i] is not None) and self._bricks[i]._vanishingStep > 30:
                self._bricks[i] = None

        for brick in self._bricks:
            if brick is None:
                self._bricks.remove(brick)


class BrickWall(BrickGroup):
    def __init__(self, screen, x, y, width, height):
        super(BrickWall, self).__init__(screen, x, y, width, height)

        for row in range(self._height):
            for column in range(self._width):
                self._bricks.append(Brick(screen, BRICK_COLORS[row], \
                                          BRICK_WIDTH, BRICK_HEIGHT, self._x + column * BRICK_WIDTH,
                                          self._y + BRICK_HEIGHT * row))

    def draw(self):
        for brick in self._bricks:
            if brick is not None:
                brick.draw()


clock = pygame.time.Clock()

brick_group = BrickWall(screen, 0, 100, 20, 5)
brick_group.draw()

paddle = Paddle(screen, WHITE, 100, 20, 350, 645)
paddle.draw()
ball = Ball(screen, 5, 400, 600)
ball.draw()

pygame.draw.rect(screen, (51, 204, 255), (300, 300, 50, 50), 1)
glow = 0
glow_direction = 1

BACKGROUND_COLOR1 = (0, 51, 153)
BACKGROUND_COLOR2 = (0, 102, 255)
v_scroll = 0
h_scroll = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if not brick_group._bricks and ball._yLoc > 600:
        brick_group = BrickWall(screen, 0, 100, 20, 5)

    # background start
    screen.fill(BLACK)
    pygame.draw.line(screen, BLACK, (0, 649), (800, 649), 1)

    glow += glow_direction
    if glow > 30 or glow < 0:
        glow_direction = - glow_direction
    r1 = max(0, min(255, BACKGROUND_COLOR1[0] + glow))
    g1 = max(0, min(255, BACKGROUND_COLOR1[1] + glow))
    b1 = max(0, min(255, BACKGROUND_COLOR1[2] + glow))
    r2 = max(0, min(255, BACKGROUND_COLOR2[0] + glow * 2))
    g2 = max(0, min(255, BACKGROUND_COLOR2[1] + glow * 2))
    b2 = max(0, min(255, BACKGROUND_COLOR2[2] + glow * 2))

    for y in range(32):
        for x in range(14):
            scroll_speed = 1 / math.sin(math.radians(x * (90 / 7) + 7))
            zoom_factor = scroll_speed / 0.5
            print(str(x) + ' -> ' + str(zoom_factor))
            pygame.draw.rect(screen, (r2, g2, b2), (x * 60, -35 - 640 + y * 60 + v_scroll * scroll_speed, 3 * zoom_factor, 3 * zoom_factor), 0)
            #print (str(x )+ ' -> ' + str (x * (90/7)) + ' -> ' + str(scroll_speed))
            #pygame.draw.rect(screen, (r1, g1, b1), (x * 60, -35 - 640 + y * 60 + v_scroll * scroll_speed, 40 * zoom_factor, 40 * zoom_factor), 0)
            #pygame.draw.rect(screen, (r2, g2, b2), (10 + x * 60, -25 - 640 + y * 60 + v_scroll * scroll_speed, 20* zoom_factor, 20* zoom_factor), 0)
            #pygame.draw.line(screen, (r2, g2, b2), (15 + x *60, -20 + y * 60 + v_scroll * scroll_speed ), \
            #                 (15 + x * 60, 70 + y * 60 + v_scroll * scroll_speed), 2)
            #pygame.draw.line(screen, (r2, g2, b2), (25 + x * 60, -20 + y * 60 + v_scroll * scroll_speed), \
             #                (25 + x * 60, 70 + y * 60 + v_scroll * scroll_speed), 2)
            #pygame.draw.rect(screen, (r2, g2, b2), (-35 + x * 60, -10 - 640 + y * 60 + v_scroll * scroll_speed, 50, 50), 2)

    # background end

    brick_group.draw()

    ball.update(brick_group, paddle)
    ball.draw()

    prev_x_paddle = paddle._xLoc
    paddle.update(ball)
    paddle.draw()
    h_scroll += (paddle._xLoc - prev_x_paddle) / -8

    pygame.draw.rect(screen, WHITE, (0, 0, 802, 800), 1)
    brick_group.update(ball)
    pygame.draw.rect(screen, BLACK, (803, 0, 423, 800), 0)

    pygame.display.flip()

    clock.tick(60)

    if v_scroll < 50:
        v_scroll += 4
    else:
        v_scroll = 0
