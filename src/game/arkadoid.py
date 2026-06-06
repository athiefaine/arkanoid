import pygame

from game.domain.entities import Ball, Paddle, BrickWall
from game.graphics.renderer import Renderer, BRICK_COLORS
from game.input.handler import InputHandler
from game.audio.player import AudioPlayer
from game.speed import SpeedController
from game.domain.scoring import ScoreTracker

# "grid" | "trench"
BACKGROUND = "grid"

# "megadrive" | "megadrive_fierce" | "synthwave"
SYNTH_PROFILE = "synthwave"

# "shmup" | "shmup_pressure" | "ambient"
COMPOSE_PROFILE = "shmup_pressure"

PADDLE_START_X = 350
PADDLE_Y = 645


def main(background=BACKGROUND):
    pygame.init()
    screen = pygame.display.set_mode((1024, 768), pygame.DOUBLEBUF)

    renderer = Renderer(screen, background)
    input_handler = InputHandler()
    audio = AudioPlayer(synth=SYNTH_PROFILE, compose=COMPOSE_PROFILE)
    audio.play()

    brick_group = BrickWall(0, 100, 20, 5, BRICK_COLORS)
    paddle = Paddle(100, 12, PADDLE_START_X, PADDLE_Y)
    ball = Ball(5, 0, 0)
    ball.anchor_to_paddle(paddle)

    clock = pygame.time.Clock()

    state = 'idle'  # 'idle' | 'aiming' | 'playing' | 'paused'
    speed = SpeedController()
    aim_angle = 0  # degrees from vertical, -75 (left) to +75 (right)
    tracker = ScoreTracker()

    while True:
        input_handler.process()

        if input_handler.toggle_pause:
            if state == 'playing':
                state = 'paused'
                audio.toggle_pause()
            elif state == 'paused':
                state = 'playing'
                audio.toggle_pause()

        if input_handler.speed_up:
            speed.up()
        if input_handler.speed_down:
            speed.down()

        if state == 'paused':
            clock.tick(60)
            continue

        

        prev_x = paddle._xLoc
        if state != 'aiming':
            paddle.update(input_handler.left, input_handler.right)
        paddle_dx = paddle._xLoc - prev_x

        for _ in range(speed.value):
            if state == 'idle':
                ball.anchor_to_paddle(paddle)
                if input_handler.launch:
                    aim_angle = 0
                    state = 'aiming'
                break  # always single iteration in idle

            elif state == 'aiming':
                if input_handler.left:
                    aim_angle = max(-75, aim_angle - 2)
                elif input_handler.right:
                    aim_angle = min(75, aim_angle + 2)
                ball.anchor_to_paddle(paddle)
                if input_handler.launch:
                    ball.launch(aim_angle)
                    state = 'playing'
                break  # always single iteration in aiming

            elif state == 'playing':
                # Ball lost below paddle
                if ball._yLoc - ball._radius > paddle._yLoc + paddle._height:
                    paddle._xLoc = PADDLE_START_X
                    ball.anchor_to_paddle(paddle)
                    tracker.on_ball_lost()
                    state = 'idle'
                    break

                # All bricks cleared — regenerate and keep playing
                if not brick_group._bricks:
                    brick_group = BrickWall(0, 100, 20, 5, BRICK_COLORS)
                    break

                events = ball.update(brick_group, paddle)
                if events['brick_hit']:
                    tracker.on_brick_hit()
                if events['paddle_hit']:
                    tracker.on_paddle_hit()
                brick_group.update()

        renderer.clear()
        renderer.draw_background(paddle_dx)
        renderer.draw_wall(brick_group)
        renderer.draw_ball(ball)
        if state == 'aiming':
            renderer.draw_reticle(ball, aim_angle)
        renderer.draw_paddle(paddle)
        renderer.draw_borders()
        renderer.draw_score(tracker.score, tracker.multiplier)
        renderer.draw_speed(speed.value)

        renderer.flip()
        clock.tick(60)


def main_trench():
    main("trench")


if __name__ == '__main__':
    main()
