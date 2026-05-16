"""
Brick collision direction tests.

Brick at x=100, y=100, width=40, height=16 (right=140, bottom=116).
Ball radius=5.

Collision type returned:
  'v' — top/bottom hit → caller should reverse ySpd
  'h' — left/right hit → caller should reverse xSpd
  None — no collision
"""

import pytest
from game.domain.entities import Ball, Brick, BrickGroup, BALL_SPEED

BRICK_X, BRICK_Y, BRICK_W, BRICK_H = 100, 100, 40, 16
COLOR = (255, 0, 0)
RADIUS = 5


def make_brick():
    return Brick(COLOR, BRICK_W, BRICK_H, BRICK_X, BRICK_Y)


def make_ball(x, y):
    b = Ball(RADIUS, x, y)
    b._collisionState = 0
    return b


# --- no collision ---

def test_no_collision_far():
    assert make_brick().collide(make_ball(200, 200)) is None


def test_no_collision_above():
    # ball entirely above brick
    assert make_brick().collide(make_ball(120, 90)) is None


def test_no_collision_right():
    # ball entirely to the right
    assert make_brick().collide(make_ball(150, 108)) is None


# --- vertical collisions (top / bottom) ---

def test_top_collision_returns_v():
    # ball coming from above, small y-overlap, large x-overlap
    # ball center (120, 97): ball_bottom=102, y_overlap=2, x_overlap=25
    assert make_brick().collide(make_ball(120, 97)) == 'v'


def test_bottom_collision_returns_v():
    # ball coming from below, small y-overlap on brick bottom
    # ball center (120, 119): ball_top=114 < 116, y_overlap=2, x_overlap=25
    assert make_brick().collide(make_ball(120, 119)) == 'v'


# --- horizontal collisions (left / right sides) ---

def test_right_side_collision_returns_h():
    # ball overlapping brick's right edge by 2px, centred vertically
    # ball center (143, 108): x_overlap=2, y_overlap=13
    assert make_brick().collide(make_ball(143, 108)) == 'h'


def test_left_side_collision_returns_h():
    # ball overlapping brick's left edge by 2px, centred vertically
    # ball center (97, 108): x_overlap=2, y_overlap=13
    assert make_brick().collide(make_ball(97, 108)) == 'h'


# --- BrickGroup propagates collision type ---

def test_brickgroup_returns_none_no_collision():
    group = BrickGroup(0, 0, 1, 1)
    group._bricks = [make_brick()]
    assert group.collide(make_ball(200, 200)) is None


def test_brickgroup_returns_v():
    group = BrickGroup(0, 0, 1, 1)
    group._bricks = [make_brick()]
    assert group.collide(make_ball(120, 97)) == 'v'


def test_brickgroup_returns_h():
    group = BrickGroup(0, 0, 1, 1)
    group._bricks = [make_brick()]
    assert group.collide(make_ball(143, 108)) == 'h'


# --- Corner case: ball clips corner shared by multiple bricks ---

def test_corner_hit_targets_closest_brick():
    # Ball at (123, 119) moving upper-left clips the corner (120, 116)
    # shared by 3 bricks. The closest (row 0 col 3 at center ~(140,108))
    # should be hit, NOT the farther row 0 col 2 (!).
    #
    # Layout (brick at x=BRICK_W*col, y=100+BRICK_H*row, W=40, H=16):
    #   row 0 col 2: x=80-120, y=100-116   (farther, should NOT be hit)
    #   row 0 col 3: x=120-160, y=100-116  (closest, should be hit)
    #   row 1 col 2: x=80-120, y=116-132   (middle distance)
    #   row 1 col 3: EMPTY

    brick_close  = Brick(COLOR, 40, 16, 120, 100)  # row 0 col 3 — closest
    brick_far    = Brick(COLOR, 40, 16,  80, 100)  # row 0 col 2 — farther

    group = BrickGroup(0, 0, 4, 2)
    group._bricks = [brick_far, brick_close]  # far brick first in list

    ball = make_ball(123, 119)

    col = group.collide(ball)

    assert col is not None
    assert brick_close._vanishingStep == 1   # closest brick hit
    assert brick_far._vanishingStep   == 0   # far brick untouched


# --- Ball.update() applies the right speed reversal ---

class _FakePaddle:
    def collide(self, ball):
        return False


class _FakeWall:
    def __init__(self, col_type):
        self._col = col_type
    def collide(self, ball):
        return self._col


def test_ball_reverses_y_on_vertical_brick_collision():
    ball = Ball(RADIUS, 120, 97)
    ball._ySpd = BALL_SPEED
    wall = _FakeWall('v')
    x_before = ball._xSpd
    ball.update(wall, _FakePaddle())
    assert ball._ySpd == -BALL_SPEED
    assert ball._xSpd == x_before


def test_ball_reverses_x_and_y_on_horizontal_brick_collision():
    # Side hit: both speeds reversed so ball bounces away from wall diagonally.
    # Without Y reversal, the ball would continue into the wall and hit inner bricks.
    ball = Ball(RADIUS, 143, 108)
    ball._xSpd = BALL_SPEED
    wall = _FakeWall('h')
    y_before = ball._ySpd
    ball.update(wall, _FakePaddle())
    assert ball._xSpd == -BALL_SPEED
    assert ball._ySpd == -y_before
