# -*- coding:utf-8 -*-

import pygame
from lib.button import Button
from random import randint
import tkinter as tk
import tkinter.messagebox as msg


class InputBox:
    def __init__(self, config, image_files):
        self.box_surface = pygame.image.load(image_files[config.INPUT_BOX])
        self.font = pygame.font.Font(config.FONT_MYRAID_PATH, 30)
        self.input_str = []
        self.return_button = Button("Return", config.RETURN_POS,
                                    pygame.image.load(image_files[config.BUTTON_RETURN]), None)

    def key_input(self, config, event, game):
        key = event.key

        if key is pygame.K_BACKSPACE:
            self.input_str = self.input_str[0:-1]

        elif key is pygame.K_RETURN:
            seed_str = "".join(self.input_str)
            if seed_str == "":
                config.GAME_STATE = config.GAME_STATE_PREV = config.GAME_STATE_GAMING
                seed = randint(0, 9223372036854775806)
                game.init(config, seed=seed)

            elif seed_str.isdigit():
                config.GAME_STATE = config.GAME_STATE_PREV = config.GAME_STATE_GAMING
                seed = int("".join(self.input_str)) % 9223372036854775806
                game.init(config, seed=seed)

            else:
                config.GAME_STATE = config.GAME_STATE_PREV = config.GAME_STATE_MENU
                root = tk.Tk()
                root.withdraw()
                msg.showerror('Error', 'Seed must be a number.')

        elif 32 <= key < 127:
            self.input_str.append(chr(key))

    def check_return_button_is_press(self, config, point):
        if self.return_button.is_press(point):
            config.GAME_STATE = config.GAME_STATE_PREV = config.GAME_STATE_MENU

    def render(self, config, surface):
        surface.blit(self.box_surface, config.INPUT_BOX_POS)
        self.return_button.render(surface)

        text = "".join(self.input_str[-32:])
        height, width = self.font.size(text)
        text_render = self.font.render(text, True, config.INPUT_COLOR)
        text_x = config.INPUT_TEXT_POS[0] - height // 2
        text_y = config.INPUT_TEXT_POS[1]
        surface.blit(text_render, (text_x, text_y))
