import math
import pygame
import pygame.gfxdraw

_RETICLE_LENGTH = 80
_RETICLE_DOT_STEP = 12

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
        self._font = pygame.font.Font(None, 28)
        self._glow = 0
        self._glow_dir = 1
        self._v_scroll = 0
        self._h_scroll = 0

    def clear(self):
        self._screen.fill(BLACK)
        pygame.draw.line(self._screen, BLACK, (0, 649), (800, 649), 1)

    def flip(self):
        pygame.display.flip()

    def draw_score(self, score, multiplier=1.0):
        score_str = f'{score:,}'.replace(',', "'")
        surf = self._font.render(score_str, True, (255, 255, 255))
        self._screen.blit(surf, (810, 40))
        if multiplier > 1.0:
            level = int(multiplier)
            progress = multiplier - level
            color = (255, 220, 0) if level < 3 else (255, 100, 50)
            surf = self._font.render(f'x{level}', True, color)
            self._screen.blit(surf, (810, 65))
            bar_x, bar_y, bar_w, bar_h = 810, 84, 50, 5
            pygame.draw.rect(self._screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))
            fill = round(bar_w * progress)
            if fill > 0:
                pygame.draw.rect(self._screen, color, (bar_x, bar_y, fill, bar_h))

    def draw_speed(self, multiplier):
        if multiplier == 1:
            return
        surf = self._font.render(f'x{multiplier}', True, (255, 220, 0))
        self._screen.blit(surf, (810, 10))

    def draw_borders(self):
        pygame.draw.rect(self._screen, WHITE, (0, 0, 802, 800), 1)
        pygame.draw.rect(self._screen, BLACK, (803, 0, 423, 800), 0)

    def draw_background(self, paddle_dx=0):
        self._glow += self._glow_dir
        if self._glow > 30 or self._glow < 0:
            self._glow_dir = -self._glow_dir
        self._h_scroll += paddle_dx / -8
        self._v_scroll = 0 if self._v_scroll >= 50 else self._v_scroll + 4

        r1 = max(0, min(255, BACKGROUND_COLOR1[0] + self._glow))
        g1 = max(0, min(255, BACKGROUND_COLOR1[1] + self._glow))
        b1 = max(0, min(255, BACKGROUND_COLOR1[2] + self._glow))
        r2 = max(0, min(255, BACKGROUND_COLOR2[0] + self._glow * 2))
        g2 = max(0, min(255, BACKGROUND_COLOR2[1] + self._glow * 2))
        b2 = max(0, min(255, BACKGROUND_COLOR2[2] + self._glow * 2))
        self._draw_background(r1, g1, b1, r2, g2, b2, self._v_scroll, self._h_scroll)

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

    def draw_reticle(self, ball, angle_deg):
        rad = math.radians(angle_deg)
        dx = math.sin(rad)
        dy = -math.cos(rad)
        x0, y0 = ball._xLoc, ball._yLoc
        steps = _RETICLE_LENGTH // _RETICLE_DOT_STEP
        for i in range(1, steps + 1):
            t = i / steps
            radius = max(1, round(3 * (1 - t * 0.6)))
            x = int(x0 + dx * i * _RETICLE_DOT_STEP)
            y = int(y0 + dy * i * _RETICLE_DOT_STEP)
            pygame.draw.circle(self._screen, (220, 220, 255), (x, y), radius)

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
