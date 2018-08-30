# -*- coding:utf-8 -*-

from lib.const import *


class Button:
    def __init__(self, name, position, image_normal, func_noraml, image_press=None, func_press=None):
        self.name = name
        self.x, self.y = position

        self.image_normal = pygame.image.load(image_normal)
        if image_press is not None:
            self.image_press = pygame.image.load(image_press)
        else:
            self.image_press = None
        self.image = self.image_normal
        self.width, self.height = self.image.get_size()

        self.func_normal = func_noraml
        self.func_press = func_press
        self.func = self.func_normal

    def is_press(self, point):
        """
        Judge whether the button is pressed
        :param point: Mouse position
        :return: Return True if pressed, otherwise return False
        """
        point_x, point_y = point
        if self.x < point_x < self.x + self.width and self.y < point_y < self.y + self.height:
            return True
        else:
            return False

    def change_state(self, pressed):
        """
        Change button state from pressed to normal, and vice versa
        :param pressed: Whether the button is pressed
        :return: None
        """
        if pressed is True:
            self.image = self.image_press
            self.func = self.func_press
        else:
            self.image = self.image_normal
            self.func = self.func_normal
        self.width, self.height = self.image.get_size()

    def render(self, surface):
        """
        Draw button on the surface
        :param surface: Game window
        :return: None
        """
        surface.blit(self.image, (self.x, self.y))
