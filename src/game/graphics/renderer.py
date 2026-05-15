import math
import pygame
import pygame.gfxdraw

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COLOR1 = (0, 51, 153)
BACKGROUND_COLOR2 = (0, 102, 255)
BRICK_COLORS = [
    (255, 77, 77),
    (0, 102, 255),
    (0, 153, 51),
    (255, 102, 153),
    (255, 102, 0)
]


class Renderer:
    def __init__(self, screen, background):
        self._screen = screen
        self._draw_background = {
            "grid": self._draw_background_grid,
            "trench": self._draw_background_trench,
        }[background]

    def clear(self):
        self._screen.fill(BLACK)
        pygame.draw.line(self._screen, BLACK, (0, 649), (800, 649), 1)

    def flip(self):
        pygame.display.flip()

    def draw_borders(self):
        pygame.draw.rect(self._screen, WHITE, (0, 0, 802, 800), 1)
        pygame.draw.rect(self._screen, BLACK, (803, 0, 423, 800), 0)

    def draw_background(self, glow, v_scroll, h_scroll):
        r1 = max(0, min(255, BACKGROUND_COLOR1[0] + glow))
        g1 = max(0, min(255, BACKGROUND_COLOR1[1] + glow))
        b1 = max(0, min(255, BACKGROUND_COLOR1[2] + glow))
        r2 = max(0, min(255, BACKGROUND_COLOR2[0] + glow * 2))
        g2 = max(0, min(255, BACKGROUND_COLOR2[1] + glow * 2))
        b2 = max(0, min(255, BACKGROUND_COLOR2[2] + glow * 2))
        self._draw_background(r1, g1, b1, r2, g2, b2, v_scroll, h_scroll)

    def _draw_background_grid(self, r1, g1, b1, r2, g2, b2, v_scroll, h_scroll):
        for y in range(16):
            for x in range(24):
                pygame.draw.rect(self._screen, (r2, g2, b2),
                                 (-360 + x * 60 + h_scroll, -10 + y * 60 + v_scroll, 50, 50), 2)
        for y in range(16):
            for x in range(24):
                pygame.draw.rect(self._screen, (r1, g1, b1),
                                 (-385 + x * 60 + h_scroll, -35 + y * 60 + v_scroll, 40, 40), 0)
                pygame.draw.rect(self._screen, (r2, g2, b2),
                                 (-375 + x * 60 + h_scroll, -25 + y * 60 + v_scroll, 20, 20), 0)

    def _draw_background_trench(self, r1, g1, b1, r2, g2, b2, v_scroll, h_scroll):
        for y in range(32):
            for x in range(14):
                scroll_speed = 1 / math.sin(math.radians(x * (90 / 7) + 7))
                zoom_factor = scroll_speed / 0.5
                pygame.draw.rect(self._screen, (r2, g2, b2),
                                 (x * 60, -35 - 640 + y * 60 + v_scroll * scroll_speed,
                                  3 * zoom_factor, 3 * zoom_factor), 0)

    def draw_ball(self, ball):
        pygame.draw.circle(self._screen, (128, 128, 128), (ball._xLoc, ball._yLoc), ball._radius, 1)
        pygame.draw.circle(self._screen, (204, 204, 204), (ball._xLoc, ball._yLoc), ball._radius - 1, 0)

    def draw_paddle(self, paddle):
        radius = paddle._height // 2
        cx_left = int(paddle._xLoc + radius)
        cx_right = int(paddle._xLoc + paddle._width - radius)
        cy = int(paddle._yLoc)
        rect_w = cx_right - cx_left

        DARK = (20, 25, 35)
        LIGHT = (165, 180, 195)
        RIM = (205, 220, 235)
        SPECULAR = (245, 250, 255)

        for i in range(-radius, radius + 1):
            t = (i + radius) / (2 * radius)
            r = int(LIGHT[0] * (1 - t) + DARK[0] * t)
            g = int(LIGHT[1] * (1 - t) + DARK[1] * t)
            b = int(LIGHT[2] * (1 - t) + DARK[2] * t)
            chord = int((radius ** 2 - i ** 2) ** 0.5)
            pygame.draw.line(self._screen, (r, g, b),
                             (cx_left - chord, cy + i), (cx_right + chord, cy + i), 1)

        pygame.draw.line(self._screen, RIM, (cx_left, cy - radius + 1), (cx_right, cy - radius + 1), 1)
        pygame.draw.circle(self._screen, SPECULAR, (cx_left + rect_w // 3, cy - radius + 2), 2)

    def draw_brick(self, brick):
        for i in range(brick._width):
            r = min(255, brick._color[0] + i)
            g = min(255, brick._color[1] + i)
            b = min(255, brick._color[2] + i)
            pygame.draw.line(self._screen, (r, g, b),
                             (brick._xLoc + i, brick._yLoc),
                             (brick._xLoc + i, brick._yLoc + brick._height), 1)
        pygame.draw.rect(self._screen, (64, 64, 64),
                         (brick._xLoc, brick._yLoc, brick._width, brick._height), 2)
        pygame.draw.line(self._screen, (192, 192, 192),
                         (brick._xLoc + 1, brick._yLoc + 1),
                         (brick._xLoc + brick._width - 2, brick._yLoc + 1), 2)
        pygame.draw.line(self._screen, (192, 192, 192),
                         (brick._xLoc + 1, brick._yLoc + 2),
                         (brick._xLoc + 1, brick._yLoc + brick._height - 2), 2)
        if brick._vanishingStep > 0:
            vanish_padding = 4
            for y in range(int(brick._height / vanish_padding) + 1):
                pygame.gfxdraw.box(self._screen, (
                    brick._xLoc, brick._yLoc + vanish_padding * y,
                    brick._width, int(brick._vanishingStep / 6)),
                                   (0, 0, 0, 255))

    def draw_wall(self, wall):
        for brick in wall._bricks:
            self.draw_brick(brick)
