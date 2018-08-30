# -*- coding:utf-8 -*-

import pygame
from lib.button import Button


class Menu:
    """
    Menu Surface and the buttons on the menu
    """
    def __init__(self, config, image_files):
        self.image_files = image_files
        self.menu_buttons = self.load_menu_button(config)
        self.utils_buttons = self.load_utils_button(config)

    def load_menu_button(self, config):
        """
        Generate menu buttons
        :param config: Global game config
        :return: Menu buttons
        """
        return [
            Button("Easy", config.EASY_POS, self.image_files[config.BUTTON_EASY], None),
            Button("Normal", config.NORMAL_POS, self.image_files[config.BUTTON_NORMAL], None),
            Button("Hard", config.HARD_POS, self.image_files[config.BUTTON_HARD], None),
            Button("Music", config.MUSIC_POS, self.image_files[config.BUTTON_MUSIC], None)
        ]

    def check_menu_button_is_press(self):
        pass

    def render_menu_buttons(self, surface):
        """
        Draw all menu buttons on the game window
        :param surface: game window
        :return: None
        """
        for button in self.menu_buttons:
            button.render(surface)

    def load_utils_button(self, config):
        """
        Generate utils buttons
        :param config: Global game config
        :return: Utils buttons
        """
        return [
            Button(r"Quit", config.QUIT_POS, self.image_files[config.BUTTON_EXIT], None),
            Button(r"Setting", config.SETTING_POS, self.image_files[config.BUTTON_SETTING], None)
        ]

    def check_utils_button_is_press(self, config, point):
        """
        Judge whether each utils button is pressed and control game accordingly
        :param config: Global game config
        :param point: Mouse position
        :return: None
        """
        if self.utils_buttons[0].is_press(point):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif self.utils_buttons[1].is_press(point):
            config.GAME_STATE_PREV = config.GAME_STATE
            config.GAME_STATE = config.GAME_STATE_SETTING

    def render_utils_buttons(self, surface):
        """
        Draw all utils buttons on the game window
        :param surface: Game window
        :return: None
        """
        for button in self.utils_buttons:
            button.render(surface)
