import sys
import pygame

from game.input.hid_gamepad import HidGamepad, AXIS_DEAD_ZONE, VENDOR, PRODUCT


class InputHandler:
    def __init__(self):
        self.toggle_pause = False
        self.launch = False
        self.speed_up = False
        self.speed_down = False
        self.left = False
        self.right = False
        self._joystick = None
        self._hid_gamepad = None
        self._init_joystick()

    def _init_joystick(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self._joystick = pygame.joystick.Joystick(0)
            self._joystick.init()
        else:
            try:
                self._hid_gamepad = HidGamepad(VENDOR, PRODUCT)
            except OSError:
                self._hid_gamepad = None

    def process(self):
        self.toggle_pause = False
        self.launch = False
        self.speed_up = False
        self.speed_down = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause = True
                elif event.key == pygame.K_SPACE:
                    self.launch = True
                elif event.unicode == '>':
                    self.speed_up = True
                elif event.unicode == '<':
                    self.speed_down = True
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    self.launch = True
            if event.type == pygame.JOYDEVICEADDED:
                self._init_joystick()
            if event.type == pygame.JOYDEVICEREMOVED:
                self._joystick = None

        keys = pygame.key.get_pressed()
        self.left = keys[pygame.K_LEFT]
        self.right = keys[pygame.K_RIGHT]

        if self._joystick:
            if self._joystick.get_numaxes() > 0:
                axis = self._joystick.get_axis(0)
                if axis < -0.3:
                    self.left = True
                elif axis > 0.3:
                    self.right = True
            if self._joystick.get_numhats() > 0:
                hat_x, _ = self._joystick.get_hat(0)
                if hat_x < 0:
                    self.left = True
                elif hat_x > 0:
                    self.right = True

        if self._hid_gamepad:
            try:
                data = self._hid_gamepad.read()
                if data and len(data) >= 3:
                    x, buttons = data[0], data[2]
                    if x < 128 - AXIS_DEAD_ZONE:
                        self.left = True
                    elif x > 128 + AXIS_DEAD_ZONE:
                        self.right = True
                    if buttons & 0x01:
                        self.launch = True
            except Exception:
                self._hid_gamepad = None
