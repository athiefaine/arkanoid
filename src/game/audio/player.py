import pygame
from game.audio.synth import SAMPLE_RATE
from game.audio.composer import build_loop


class AudioPlayer:
    def __init__(self, synth="megadrive", compose="thunderforce"):
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
        self._sound = pygame.sndarray.make_sound(build_loop(synth, compose))
        self._paused = False

    def play(self):
        self._sound.play(loops=-1)
        self._paused = False

    def toggle_pause(self):
        if self._paused:
            pygame.mixer.unpause()
        else:
            pygame.mixer.pause()
        self._paused = not self._paused

    def stop(self):
        self._sound.stop()
