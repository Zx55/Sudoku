# -*- coding:utf-8 -*-

from lib.button import *
from random import randint


class Setting:
    """
    Setting Surface and the buttons on the setting
    """
    def __init__(self, config, image_files):
        self.surface = pygame.image.load(image_files[config.SETTING_SURFACE])
        self.mask = pygame.Surface(config.DISPLAY_RESOLUTION, pygame.SRCALPHA, 32)
        self.mask.fill((0, 0, 0, 185))

        self.x, self.y = config.SETTING_SURFACE_POS
        self.width, self.height = self.surface.get_size()

        self.buttons = []
        self.load_button(config, image_files)
        self.init_button(config)
        self.texts = []
        self.load_text(config)

    def load_button(self, config, image_files):
        """
        Generate setting buttons
        :param config: Global game config
        :param image_files: All images
        :return: All setting buttons
        """
        self.buttons = [
            Button("Close Setting", config.CLOSE_SETTING_POS, image_files[config.BUTTON_CLOSE_SETTING], None),
            Button("Random Theme", config.THEME_RANDOM_POS, image_files[config.BUTTON_RANDOM_THEME], self.random_theme),
            Button("Theme 1", config.THEME_1_POS, image_files[config.BUTTON_THEMES[0]], self.change_theme,
                   image_files[config.BUTTON_THEMES[0] + 1], self.change_theme),
            Button("Theme 2", config.THEME_2_POS, image_files[config.BUTTON_THEMES[1]], self.change_theme,
                   image_files[config.BUTTON_THEMES[1] + 1], self.change_theme),
            Button("Theme 3", config.THEME_3_POS, image_files[config.BUTTON_THEMES[2]], self.change_theme,
                   image_files[config.BUTTON_THEMES[2] + 1], self.change_theme),
            Button("Theme 4", config.THEME_4_POS, image_files[config.BUTTON_THEMES[3]], self.change_theme,
                   image_files[config.BUTTON_THEMES[3] + 1], self.change_theme),
            Button("Theme 5", config.THEME_5_POS, image_files[config.BUTTON_THEMES[4]], self.change_theme,
                   image_files[config.BUTTON_THEMES[4] + 1], self.change_theme),
            Button("Timer", config.SWITCH_TIMER_POS, image_files[config.BUTTON_SWITCH_ON], self.change_setting,
                   image_files[config.BUTTON_SWITCH_OFF], self.change_setting),
            Button("Fullscreen", config.SWITCH_FULLSCREEN_POS, image_files[config.BUTTON_SWITCH_ON], self.change_setting,
                   image_files[config.BUTTON_SWITCH_OFF], self.change_setting),
            Button("Show Error", config.SWITCH_ERROR_POS, image_files[config.BUTTON_SWITCH_ON], self.change_setting,
                   image_files[config.BUTTON_SWITCH_OFF], self.change_setting)
        ]

    def init_button(self, config):
        """
        Initialize setting buttons according to config.SETTING
        :param config: Global game config
        :return: None
        """
        for i in range(len(config.SETTING)):
            if config.SETTING[i] is config.SETTING_ON:
                self.buttons[i + 7].change_state(False)
            else:
                self.buttons[i + 7].change_state(True)

    def load_text(self, config):
        """
        Generate texts on the setting
        :param config: Global game config
        :return: None
        """
        font_setting = pygame.font.Font(config.FONT_MYRAID_PATH, 26)
        font_title = pygame.font.Font(config.FONT_MYRAID_PATH, 21)
        font_option = pygame.font.Font(config.FONT_MYRAID_PATH, 18)
        self.texts = [
            (font_setting.render("Setting", True, config.TEXT_COLOR), config.TEXT_SETTING_POS),
            (font_title.render("Color Theme", True, config.TEXT_COLOR), config.TEXT_THEME_POS),
            (font_title.render("General", True, config.TEXT_COLOR), config.TEXT_GENERAL_POS),
            (font_option.render("Timer", True, config.TEXT_COLOR), config.TEXT_TIMER_POS),
            (font_option.render("Fullscreen", True, config.TEXT_COLOR), config.TEXT_FULLSCREEN_POS),
            (font_option.render("Show errors", True, config.TEXT_COLOR), config.TEXT_ERROR_POS)
        ]

    def render(self, config, surface):
        """
        Draw all elements on the setting surface
        :param config: Global game config
        :param surface: game window
        :return: None
        """
        surface.blit(self.mask, (0, 0))
        surface.blit(self.surface, config.SETTING_SURFACE_POS)

        for button in self.buttons:
            button.render(surface)
        for text, pos in self.texts:
            surface.blit(text, pos)

    def render_buttons(self, surface):
        """
        Draw all setting buttons on the game window
        :param surface: Game window
        :return: None
        """
        for button in self.buttons:
            button.render(surface)

    def check_setting_buttons_is_press(self, config, point):
        """
        Judge whether each setting button is pressed and change setting accordingly
        :param config: Global game config
        :param point: Mouse Position
        :return: None
        """
        if self.buttons[0].is_press(point):
            config.GAME_STATE = config.GAME_STATE_PREV
        elif self.buttons[1].is_press(point):
            self.random_theme(config)
        else:
            for i in range(2, len(self.buttons)):
                if self.buttons[i].is_press(point):
                    self.buttons[i].func(config, i)
                    break

    def random_theme(self, config):
        """
        Change color theme randomly
        :param config: Global game config
        :return: None
        """
        i = randint(0, 4)
        self.buttons[2 + config.SETTING_COLOR_THEME // 2].change_state(False)
        config.SETTING_COLOR_THEME = config.THEMES_720[i] - 15
        self.buttons[i + 2].change_state(True)

    def change_theme(self, config, i):
        """
        Change theme
        :param config: Global game config
        :param i: the number of color theme that player wants to change
        :return: None
        """
        self.buttons[2 + config.SETTING_COLOR_THEME // 2].change_state(False)
        config.SETTING_COLOR_THEME = config.THEMES_720[i - 2] - 15
        self.buttons[i].change_state(True)

    def change_setting(self, config, i):
        """
        Change setting
        :param config: Global game config
        :param i: the number of setting that player wants to change
        :return: None
        """
        if config.SETTING[i - 7] is config.SETTING_ON:
            config.SETTING[i - 7] = config.SETTING_OFF
            self.buttons[i].change_state(True)
        else:
            config.SETTING[i - 7] = config.SETTING_ON
            self.buttons[i].change_state(False)
