import sys
import pygame


class InputHandler:
    def __init__(self):
        self.quit = False
        self.toggle_pause = False
        self.speed_up = False
        self.speed_down = False

    def process(self):
        self.toggle_pause = False
        self.speed_up = False
        self.speed_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.toggle_pause = True
                elif event.unicode == '>':
                    self.speed_up = True
                elif event.unicode == '<':
                    self.speed_down = True
