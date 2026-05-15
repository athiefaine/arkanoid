import pygame

from game.domain.entities import Ball, Paddle, BrickWall
from game.graphics.renderer import Renderer, BRICK_COLORS
from game.input.handler import InputHandler

# "grid" | "trench"
BACKGROUND = "grid"


def main(background=BACKGROUND):
    pygame.init()
    screen = pygame.display.set_mode((1024, 768), pygame.DOUBLEBUF)

    renderer = Renderer(screen, background)
    input_handler = InputHandler()

    brick_group = BrickWall(0, 100, 20, 5, BRICK_COLORS)
    paddle = Paddle(100, 12, 350, 645)
    ball = Ball(5, 400, 600)

    clock = pygame.time.Clock()
    glow = 0
    glow_direction = 1
    v_scroll = 0
    h_scroll = 0
    paused = False

    while True:
        input_handler.process()
        if input_handler.toggle_pause:
            paused = not paused

        if paused:
            clock.tick(60)
            continue

        if not brick_group._bricks and ball._yLoc > 600:
            brick_group = BrickWall(0, 100, 20, 5, BRICK_COLORS)

        glow += glow_direction
        if glow > 30 or glow < 0:
            glow_direction = -glow_direction

        renderer.clear()
        renderer.draw_background(glow, v_scroll, h_scroll)
        renderer.draw_wall(brick_group)
        renderer.draw_ball(ball)
        renderer.draw_paddle(paddle)
        renderer.draw_borders()

        prev_x = paddle._xLoc
        ball.update(brick_group, paddle)
        paddle.update(ball)
        h_scroll += (paddle._xLoc - prev_x) / -8
        brick_group.update()

        renderer.flip()
        clock.tick(60)

        if v_scroll < 50:
            v_scroll += 4
        else:
            v_scroll = 0


def main_trench():
    main("trench")


if __name__ == '__main__':
    main()
