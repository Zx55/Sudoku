# -*- coding:utf-8 -*-

import pygame
import json


class Config:
    def __init__(self):
        # Global game state
        # ---------------------------------------------------------------------------------------
        self.GAME_STATE_MENU = 0
        self.GAME_STATE_SETTING = 1
        self.GAME_STATE_GAMING = 2
        self.GAME_STATE_CLEAR = 3
        self.GAME_STATE_INPUT = 4
        self.GAME_STATE = self.GAME_STATE_MENU
        self.GAME_STATE_PREV = self.GAME_STATE
        # ---------------------------------------------------------------------------------------
        # Display config
        self.DISPLAY_MODE_FULLSCREEN = pygame.FULLSCREEN | pygame.HWSURFACE
        self.DISPLAY_MODE_WINDOW = 0
        self.DISPLAY_MODE = self.DISPLAY_MODE_WINDOW

        self.DISPLAY_RESOLUTION_FULLSCREEN = (1920, 1080)
        self.DISPLAY_RESOLUTION_WINDOW = (1280, 720)
        self.DISPLAY_RESOLUTION = self.DISPLAY_RESOLUTION_WINDOW
        # ---------------------------------------------------------------------------------------
        # MusicEngine config
        self.MUSIC_PATH = r'./sound'
        self.MUSIC_FILE_STATE_INIT = -1
        self.MUSIC_FILE_STATE_NORMAL = 0
        self.MUSIC_FILE_STATE_NOT_FOUND = 1
        self.MUSIC_FILE_STATE = self.MUSIC_FILE_STATE_INIT

        self.TRACK_END = pygame.USEREVENT + 1

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
        # ---------------------------------------------------------------------------------------
        # Font config
        self.FONT_MYRAID_PATH = r'./font/MyriadPro-Bold.ttf'
        self.FONT_ERAS_PATH = r'./font/ERASMD.TTF'
        self.TEXT_COLOR = (70, 70, 70)
        self.INPUT_COLOR = (70, 70, 70)
        self.NUM_COLOR_BUILTIN = (20, 20, 20)
        self.NUM_COLOR_NEW = (90, 145, 255)
        self.TIMER_COLOR = (20, 20, 20)
        # ---------------------------------------------------------------------------------------
        # Image config
        self.IMAGE_PATH = r'./image/pic'
        self.IMAGE_FILE_STATE_INIT = -1
        self.IMAGE_FILE_STATE_NORMAL = 0
        self.IMAGE_FILE_STATE_NOT_FOUND = 1
        self.IMAGE_FILE_STATE = self.IMAGE_FILE_STATE_INIT

        # Image index
        self.ICON = 102
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
        self.BUTTON_REDO_INACTIVE = 76
        self.BUTTON_UNDO_INACTIVE = 77
        self.BUTTON_FLUSH = 74
        self.BUTTON_GAME_MENU = 75

        self.BUTTON_EASY = 11
        self.BUTTON_NORMAL = 12
        self.BUTTON_HARD = 13
        self.BUTTON_RANDOM = 99
        self.BUTTON_LOAD = 14
        self.BUTTON_LOAD_INACTIVE = 73

        self.INPUT_BOX = 100
        self.BUTTON_RETURN = 101
        self.BUTTON_CONFIRM = 103

        self.THEMES_720 = [15, 17, 19, 21, 23]

        self.SETTING_SURFACE = 25
        self.BUTTON_CLOSE_SETTING = 26
        self.BUTTON_RANDOM_THEME = 27
        self.BUTTON_THEMES = [28, 30, 32, 34, 36]
        self.BUTTON_SWITCH_ON = 38
        self.BUTTON_SWITCH_OFF = 39

        self.CELL_SURFACE = 40
        self.BUTTON_CELL = 41
        self.BUTTON_CELL_OVER = 78
        self.CELL_NUM_BUILTIN = 42
        self.CELL_NUM_NEW = 51
        self.CELL_NUM_NEW_OVER = 79
        self.CELL_BUTTON_EXPAND = 60
        self.EXPAND_NUM = 61
        self.EXPAND_NUM_OVER = 90
        self.HIGHLIGHT_ROW = 88

        self.BUTTON_CLEAR_MENU = 70
        self.BUTTON_CLEAR_RESTART = 71
        self.TEXT_CONG = 72
        # ---------------------------------------------------------------------------------------
        # Generator config
        self.GENERATOR_API_PATH = r"./lib/_generator.cp36-win_amd64.pyd"
        self.API_FOUND = True
        # ---------------------------------------------------------------------------------------
        # Gaming config
        self.CELL_CLICK_INDEX = [-1, -1, -1, -1, -1] # cell_no, (index: x, y), no, button_no
        self.CELL_BUTTON_NUM = 0
        self.CELL_BUTTON_POSSIBLE = [1, 1, 1, 1, 1, 1, 1, 1, 1]

        self.CELL_OVER_INDEX = [-1, -1]

        self.UN_STK = [
            [],
            0
        ]
        self.RE_STK = [
            [],
            0
        ]
        self.SOLUTION = None
        self.PROBLEM = None
        # ---------------------------------------------------------------------------------------
        # Setting config
        self.SETTING_ON = 1
        self.SETTING_OFF = 0

        self.SETTING_TIMER = 0
        self.TIME = 0
        self.TIMER_TICK = pygame.USEREVENT + 2
        pygame.time.set_timer(self.TIMER_TICK, 1000)

        self.SETTING_FULLSCREEN = 1
        self.SETTING_SHOW_HIGHLIGHT = 2
        self.SETTING_SHOW_POSSIBLE = 3

        self.SETTING_PATH = r'./data/setting.json'

        # Read settings from json file
        with open(self.SETTING_PATH, "r") as fp:
            self.SETTING, SAVE_DATA, self.TIME = json.load(fp)
        self.SOLUTION, self.PROBLEM = SAVE_DATA

        self.SETTING_COLOR_THEME = 0
        # ---------------------------------------------------------------------------------------
        # Position config
        self.FACTOR = 1.5
        self.PLAY_PAUSE_POS = (840, 10)
        self.STOP_POS = (900, 10)
        self.NEXT_POS = (960, 10)
        self.PREV_POS = (1020, 10)
        self.MUTE_POS = (1080, 10)
        self.QUIT_POS = (1220, 10)
        self.UNDO_POS = (1160, 660)
        self.REDO_POS = (1220, 660)
        self.GAME_MENU_POS = (1100, 660)
        self.FLUSH_POS = (1040, 660)
        self.SETTING_POS = (1160, 10)
        self.EASY_POS = (490, 195)
        self.NORMAL_POS = (490, 265)
        self.HARD_POS = (490, 335)
        self.RANDOM_POS = (490, 405)
        self.LOAD_POS = (490, 475)
        self.INPUT_BOX_POS = (340, 265)
        self.INPUT_TEXT_POS = (640, 280)
        self.CONFIRM_POS = (490, 405)
        self.RETURN_POS = (490, 475)
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
        self.TEXT_POSSIBLE_POS = (480, 470)
        self.SWITCH_POSSIBLE_POS = (750, 465)
        self.TEXT_HOMEPAGE_POS = (460, 520)
        self.CELL_POS = [
            (350, 100),
            (550, 100),
            (750, 100),
            (350, 300),
            (550, 300),
            (750, 300),
            (350, 500),
            (550, 500),
            (750, 500),
        ]
        self.CELL_BUTTON_BIAS = [
                (9, 8),
                (65, 8),
                (121, 8),
                (9, 63),
                (65, 63),
                (121, 63),
                (9, 118),
                (65, 118),
                (121, 118),
        ]
        self.EXPAND_NUM_BIAS = [
            (12, 10),
            (35, 10),
            (58, 10),
            (12, 33),
            (35, 33),
            (58, 33),
            (12, 56),
            (35, 56),
            (58, 56),
        ]
        self.CLEAR_MENU_POS = (490, 335)
        self.CLEAR_RE_POS = (490, 405)
        self.CONG_POS = (435, 220)
        self.TIMER_POS = (20, 20)
        # ---------------------------------------------------------------------------------------
        # Data Path
        self.DIFFICULTY_EASY = 0
        self.DIFFICULTY_NORMAL = 1
        self.DIFFICULTY_HARD = 2
        self.DATA_GENERATE = 3
        self.DIFFICULTY = self.DIFFICULTY_EASY

        self.DATA_PATH = [
            "./data/easy.json",
            "./data/normal.json",
            "./data/hard.json",
            "./data/generate_data.json"
        ]

    def save_config(self, game):
        """
        Save setting when game is terminated
        :return: None
        """
        if self.GAME_STATE is self.GAME_STATE_GAMING:
            data = [
                self.SETTING,
                [
                    self.SOLUTION,
                    game.cells.data
                ],
                self.TIME
            ]

        else:
            data = [
                self.SETTING,
                [
                    None,
                    None
                ],
                0
            ]

        with open(self.SETTING_PATH, "w") as fp:
            json.dump(data, fp)
