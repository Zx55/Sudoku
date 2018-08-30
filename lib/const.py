# -*- coding:utf-8 -*-

import pygame.locals
import json


class Config:
    def __init__(self):
        # Global game state
        self.GAME_STATE_MENU = 0
        self.GAME_STATE_SETTING = 1
        self.GAME_STATE_GAMING = 2
        self.GAME_STATE = self.GAME_STATE_MENU
        self.GAME_STATE_PREV = self.GAME_STATE

        # Display config
        self.DISPLAY_MODE_FULLSCREEN = pygame.FULLSCREEN | pygame.HWSURFACE
        self.DISPLAY_MODE_WINDOW = 0
        self.DISPLAY_MODE = self.DISPLAY_MODE_WINDOW

        self.DISPLAY_RESOLUTION_FULLSCREEN = (1920, 1080)
        self.DISPLAY_RESOLUTION_WINDOW = (1280, 720)
        self.DISPLAY_RESOLUTION = self.DISPLAY_RESOLUTION_WINDOW

        # MusicEngine config
        self.MUSIC_PATH = r'./sound'
        self.MUSIC_FILE_STATE_INIT = -1
        self.MUSIC_FILE_STATE_NORMAL = 0
        self.MUSIC_FILE_STATE_NOT_FOUND = 1
        self.MUSIC_FILE_STATE = self.MUSIC_FILE_STATE_INIT

        self.MUSIC_INDEX = 0
        self.MUSIC_MAX_INDEX = 0

        self.MUSIC_STATE_INIT = 0
        self.MUSIC_STATE_PLAY = 1
        self.MUSIC_STATE_PAUSE = 2
        self.MUSIC_STATE_STOP = 3
        self.MUSIC_STATE = self.MUSIC_STATE_INIT

        self.MUSIC_MUTE_STATE_OFF = 0
        self.MUSIC_MUTE_STATE_ON = 1
        self.MUSIC_MUTE_STATE = self.MUSIC_MUTE_STATE_OFF

        # Font config
        self.FONT_MYRAID_PATH = r'./font/MyriadPro-Bold.ttf'
        self.TEXT_COLOR = (70, 70, 70)

        # Image config
        self.IMAGE_PATH = r'./image/pic'
        self.IMAGE_FILE_STATE_INIT = -1
        self.IMAGE_FILE_STATE_NORMAL = 0
        self.IMAGE_FILE_STATE_NOT_FOUND = 1
        self.IMAGE_FILE_STATE = self.IMAGE_FILE_STATE_INIT

        # Image index
        self.BUTTON_PLAY = 0
        self.BUTTON_PAUSE = 1
        self.BUTTON_STOP = 2
        self.BUTTON_NEXT = 3
        self.BUTTON_PREV = 4
        self.BUTTON_MUTE_OFF = 5
        self.BUTTON_MUTE_ON = 6

        self.BUTTON_EXIT = 7
        self.BUTTON_SETTING = 8

        self.BUTTON_REDO = 9
        self.BUTTON_UNDO = 10

        self.BUTTON_EASY = 11
        self.BUTTON_NORMAL = 12
        self.BUTTON_HARD = 13
        self.BUTTON_MUSIC = 14

        # THEMES_1080 = [THEME_720[i] + 1 for i in range(len(THEME_720))]
        self.THEMES_720 = [15, 17, 19, 21, 23]

        self.SETTING_SURFACE = 25
        self.BUTTON_CLOSE_SETTING = 26
        self.BUTTON_RANDOM_THEME = 27
        # BUTTON_THEMES_SELECTED = [BUTTON_THEMES[i] + 1 for i in range(len(BUTTON_THEMES))]
        self.BUTTON_THEMES = [28, 30, 32, 34, 36]
        self.BUTTON_SWITCH_ON = 38
        self.BUTTON_SWITCH_OFF = 39

        # Setting config
        self.SETTING_ON = 1
        self.SETTING_OFF = 0

        self.SETTING_TIMER = 0
        self.SETTING_FULLSCREEN = 1
        self.SETTING_SHOW_ERROR = 2

        self.SETTING_PATH = r'./lib/setting.json'

        # Read settings from json file
        with open(self.SETTING_PATH, "r") as fp:
            self.SETTING = json.load(fp)

        self.SETTING_COLOR_THEME = 0

        # All elements' position
        self.FACTOR = 1.5
        self.PLAY_PAUSE_POS = (840, 10)
        self.STOP_POS = (900, 10)
        self.NEXT_POS = (960, 10)
        self.PREV_POS = (1020, 10)
        self.MUTE_POS = (1080, 10)
        self.QUIT_POS = (1220, 10)
        self.SETTING_POS = (1160, 10)
        self.EASY_POS = (490, 210)
        self.NORMAL_POS = (490, 285)
        self.HARD_POS = (490, 360)
        self.MUSIC_POS = (490, 435)
        self.SETTING_SURFACE_POS = (440, 178)
        self.CLOSE_SETTING_POS = (822, 160)
        self.TEXT_SETTING_POS = (460, 200)
        self.TEXT_THEME_POS = (470, 240)
        self.THEME_RANDOM_POS = (480, 265)
        self.THEME_1_POS = (530, 265)
        self.THEME_2_POS = (580, 265)
        self.THEME_3_POS = (630, 265)
        self.THEME_4_POS = (680, 265)
        self.THEME_5_POS = (730, 265)
        self.TEXT_GENERAL_POS = (470, 310)
        self.TEXT_TIMER_POS = (480, 350)
        self.SWITCH_TIMER_POS = (750, 345)
        self.TEXT_FULLSCREEN_POS = (480, 390)
        self.SWITCH_FULLSCREEN_POS = (750, 385)
        self.TEXT_ERROR_POS = (480, 430)
        self.SWITCH_ERROR_POS = (750, 425)

    def save_config(self):
        """
        Save setting when game is terminated
        :return: None
        """
        with open(self.SETTING_PATH, "w") as fp:
            json.dump(self.SETTING, fp)
