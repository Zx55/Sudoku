# -*- coding:utf-8 -*-

import pygame
import json
from random import randint
from lib.cell import Cells
from lib.button import Button
from lib.generator import Generator


class Game:
    def __init__(self, config, image_files):
        self.image_files = image_files
        self.generator = Generator(config)

        self.difficulty = config.DIFFICULTY
        self.cells = None
        self.font = pygame.font.Font(config.FONT_MYRAID_PATH, 30)

        self.game_buttons = [
            Button(0, config.UNDO_POS, pygame.image.load(image_files[config.BUTTON_UNDO]), None,
                   pygame.image.load(image_files[config.BUTTON_UNDO_INACTIVE]), None),
            Button(0, config.REDO_POS, pygame.image.load(image_files[config.BUTTON_REDO]), None,
                   pygame.image.load(image_files[config.BUTTON_REDO_INACTIVE]), None),
            Button("Menu", config.GAME_MENU_POS,
                   pygame.image.load(image_files[config.BUTTON_GAME_MENU]), None),
            Button("Flush", config.FLUSH_POS,
                   pygame.image.load(image_files[config.BUTTON_FLUSH]), None),
        ]

        self.congratulation = pygame.image.load(image_files[config.TEXT_CONG])
        self.clear_buttons = [
            Button("Restart", config.CLEAR_RE_POS,
                   pygame.image.load(image_files[config.BUTTON_CLEAR_RESTART]), None),
            Button("Menu", config.CLEAR_MENU_POS,
                   pygame.image.load(image_files[config.BUTTON_CLEAR_MENU]), None)
        ]

    def init(self, config, difficulty=None, load=False, seed=None):
        if difficulty is not None:
            self.difficulty = difficulty
            config.TIME = 0

            if config.API_FOUND is True:
                self.generator.set_difficulty(difficulty)
                self.generator.generate_sudoku()

        if seed is not None and config.API_FOUND is True:
            config.TIME = 0
            self.generator.set_seed(seed)
            self.generator.generate_sudoku()

        load_data(config, difficulty, load, seed)
        config.UN_STK[0].clear()
        config.RE_STK[0].clear()
        config.CELL_BUTTON_NUM = config.UN_STK[1] = config.RE_STK[1] = 0
        self.cells = Cells(config, self.image_files)

    def check_stack(self, config):
        if config.UN_STK[1] == 0 and self.game_buttons[0].label == 0:
            self.game_buttons[0].change_state(True)
            self.game_buttons[0].label = 1

        elif config.UN_STK[1] != 0 and self.game_buttons[0].label == 1:
            self.game_buttons[0].change_state(False)
            self.game_buttons[0].label = 0

        if config.RE_STK[1] == 0 and self.game_buttons[1].label == 0:
            self.game_buttons[1].change_state(True)
            self.game_buttons[1].label = 1

        elif config.RE_STK[1] != 0 and self.game_buttons[1].label == 1:
            self.game_buttons[1].change_state(False)
            self.game_buttons[1].label = 0

    def check_clear_button_is_press(self, config, point):
        if self.clear_buttons[0].is_press(point):
            config.GAME_STATE = config.GAME_STATE_PREV = config.GAME_STATE_GAMING
            config.TIME = 0
            self.init(config)

        elif self.clear_buttons[1].is_press(point):
            config.GAME_STATE = config.GAME_STATE_MENU

    def check_game_button_is_press(self, config, point):
        if self.game_buttons[0].is_press(point):
            self.cells.undo(config)

        elif self.game_buttons[1].is_press(point):
            self.cells.redo(config)

        elif self.game_buttons[2].is_press(point):
            config.GAME_STATE = config.GAME_STATE_MENU
            config.PROBLEM = self.cells.data

        elif self.game_buttons[3].is_press(point):
            self.init(config)

    def check_right_click(self, config, point):
        if config.CELL_CLICK_INDEX[0] != -1:
            config.CELL_CLICK_INDEX[0] = -1
        self.cells.check_cell_button_is_over(config, point)

    def render(self, config, surface):
        self.cells.render(config, surface)

        if config.SETTING[config.SETTING_TIMER] is config.SETTING_ON:
            self.render_timer(config, surface)

        self.check_stack(config)
        for button in self.game_buttons:
            button.render(surface)

    def render_clear(self, config, surface):
        surface.blit(self.congratulation, config.CONG_POS)
        for button in self.clear_buttons:
            button.render(surface)

    def render_timer(self, config, surface):
        sec = config.TIME % 60
        minute = config.TIME // 60 % 60
        hour = config.TIME // 3600
        time_str = "{} : {:0>2} : {:0>2}".format(hour, minute, sec)
        surface.blit(self.font.render(time_str, True, config.TIMER_COLOR), config.TIMER_POS)


def load_data(config, difficulty, load, seed):
    if (load is False and difficulty is not None) or seed is not None:
        # Create a new game or Create a random game from generator
        if config.API_FOUND is True:
            with open(config.DATA_PATH[config.DATA_GENERATE]) as fp:
                solution, problem = json.load(fp)
                config.SOLUTION = [solution[i * 9: i * 9 + 9] for i in range(9)]
                config.PROBLEM = [problem[i * 9: i * 9 + 9] for i in range(9)]

        # Create a new game from local data
        else:
            with open(config.DATA_PATH[difficulty], "r") as fp:
                data = json.load(fp)
                config.SOLUTION, config.PROBLEM = data[randint(0, len(data) - 1)]

    # Flush
    elif load is False and difficulty is None:
        for i in range(9):
            for j in range(9):
                if config.PROBLEM[i][j] < 0:
                    config.PROBLEM[i][j] = 0
