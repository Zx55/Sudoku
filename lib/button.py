# -*- coding:utf-8 -*-

import pygame
from lib.const import *
from lib.music import *


class Button:
    def __init__(self, name, position, image_normal, image_press=None):
        self.name = name
        self.x, self.y = position

        self.image_normal = pygame.image.load(image_normal)
        if image_press is not None:
            self.image_press = pygame.image.load(image_press)
        else:
            self.image_press = None
        self.image = self.image_normal

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

    def change_image(self, pressed):
        if pressed is True:
            self.image = self.image_press
        else:
            self.image = self.image_normal
        self.width, self.height = self.image.get_size()

    def render(self, surface):
        """
        Draw button on the surface
        :param surface: game windows
        :return: None
        """
        surface.blit(self.image, (self.x, self.y))


def load_media_button(config, image_files):
    """
    Generate media buttons
    :param config: Game config
    :param image_files: Image list
    :return: Media buttons
    """
    buttons = [0] * 5

    buttons[0] = Button(r"Play/Pause", (600, 10), image_files[
        config.BUTTON_PAUSE], image_files[config.BUTTON_PLAY])
    buttons[1] = Button(r"Stop", (670, 10), image_files[
        config.BUTTON_STOP])
    buttons[2] = Button(r"Next", (740, 10), image_files[config.BUTTON_NEXT])
    buttons[3] = Button(r"Prev", (810, 10), image_files[config.BUTTON_PREV])
    buttons[4] = Button(r"Mute", (880, 10), image_files[
        config.BUTTON_MUTE_OFF], image_files[config.BUTTON_MUTE_ON])

    return buttons


def render_media_button(buttons, surface):
    for button in buttons:
        button.render(surface)


def check_media_button_is_press(config, music_files, buttons, point):
    if buttons[0].is_press(point):
        if config.MUSIC_STATE is config.MUSIC_STATE_PLAY:
            music_pause(config, buttons)
        else:
            music_play(config, music_files, buttons)
    elif buttons[1].is_press(point):
        music_stop(config, buttons)
    elif buttons[2].is_press(point):
        music_next(config, music_files)
    elif buttons[3].is_press(point):
        music_prev(config, music_files)
    elif buttons[4].is_press(point):
        if config.MUSIC_MUTE_STATE is config.MUSIC_MUTE_STATE_ON:
            music_mute_off(config, buttons)
        else:
            music_mute_on(config, buttons)


def load_menu_button(image_files):
    pass


def render_menu_button():
    pass


def check_menu_button_is_press():
    pass
