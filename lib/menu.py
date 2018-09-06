# -*- coding:utf-8 -*-

import pygame
from lib.button import Button


class Menu:
    def __init__(self, config, image_files):
        self.image_files = image_files

        self.menu_buttons = [
            Button(config.DIFFICULTY_EASY, config.EASY_POS,
                   pygame.image.load(self.image_files[config.BUTTON_EASY]), None),
            Button(config.DIFFICULTY_NORMAL, config.NORMAL_POS,
                   pygame.image.load(self.image_files[config.BUTTON_NORMAL]), None),
            Button(config.DIFFICULTY_HARD, config.HARD_POS,
                   pygame.image.load(self.image_files[config.BUTTON_HARD]), None),
            Button(True, config.LOAD_POS,
                   pygame.image.load(self.image_files[config.BUTTON_LOAD]), None,
                   pygame.image.load(self.image_files[config.BUTTON_LOAD_INACTIVE]), None)
        ]
        self.utils_buttons = [
            Button(r"Quit", config.QUIT_POS,
                   pygame.image.load(self.image_files[config.BUTTON_EXIT]), None),
            Button(r"Setting", config.SETTING_POS,
                   pygame.image.load(self.image_files[config.BUTTON_SETTING]), None)
        ]

    def check_load(self, config):
        button = self.menu_buttons[-1]
        if config.PROBLEM is None and button.label is True:
            button.change_state(True)
            button.label = False

        elif config.PROBLEM is not None and button.label is False:
            button.change_state(False)
            button.label = True

    def check_menu_button_is_press(self, config, point, game):
        for button in self.menu_buttons[:-1]:
            if button.is_press(point):
                config.GAME_STATE = config.GAME_STATE_PREV = config.GAME_STATE_GAMING
                game.init(config, difficulty=button.label)

        if self.menu_buttons[-1].is_press(point) and config.PROBLEM is not None:
            config.GAME_STATE = config.GAME_STATE_PREV = config.GAME_STATE_GAMING
            game.init(config, load=True)

    def check_utils_button_is_press(self, config, point):
        if self.utils_buttons[0].is_press(point):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif self.utils_buttons[1].is_press(point):
            config.GAME_STATE_PREV = config.GAME_STATE
            config.GAME_STATE = config.GAME_STATE_SETTING

    def render_utils_buttons(self, surface):
        for button in self.utils_buttons:
            button.render(surface)

    def render_menu_buttons(self, config, surface):
        self.check_load(config)
        for button in self.menu_buttons:
            button.render(surface)
