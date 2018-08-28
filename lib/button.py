# -*- coding:utf-8 -*-

import pygame


class Button:
    def __init__(self, name, position, image_filename):
        self.name = name
        self.x = position.x
        self.y = position.y
        self.image = pygame.image.load(image_filename)
        # self.image_press = pygame.image.load(image_filename_press)
        self.width, self.height = self.image.get_size()

    def is_press(self, point):
        """
        Judge whether the button is pressed
        :param point: The position of mouse
        :return: bool
        """
        point_x, point_y = point
        if self.x < point_x < self.x + self.width and self.y < point_y < \
                self.y + self.height:
            return True
        else:
            return False

    def render(self, surface):
        """
        Draw button on the surface
        :param surface: game windows
        :return: None
        """
        surface.blit(self.image, (self.x, self.y))
