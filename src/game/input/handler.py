import sys
import pygame


class InputHandler:
    def __init__(self):
        self.quit = False
        self.toggle_pause = False

    def process(self):
        self.toggle_pause = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.toggle_pause = True
