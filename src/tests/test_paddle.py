from game.domain.entities import Paddle, PADDLE_SPEED

WIDTH, HEIGHT, Y = 100, 12, 645
ARENA_W = 800


def make_paddle(x):
    return Paddle(WIDTH, HEIGHT, x, Y)


def test_moves_left():
    p = make_paddle(200)
    p.update(left=True, right=False)
    assert p._xLoc == 200 - PADDLE_SPEED


def test_moves_right():
    p = make_paddle(200)
    p.update(left=False, right=True)
    assert p._xLoc == 200 + PADDLE_SPEED


def test_no_input_no_move():
    p = make_paddle(200)
    p.update(left=False, right=False)
    assert p._xLoc == 200


def test_left_bound():
    p = make_paddle(2)
    p.update(left=True, right=False)
    assert p._xLoc == 0


def test_right_bound():
    p = make_paddle(ARENA_W - WIDTH - 2)
    p.update(left=False, right=True)
    assert p._xLoc == ARENA_W - WIDTH
