# -*- coding:utf-8 -*-

import pygame
from sys import exit
from lib.const import Config
import lib.image as image
import lib.music as music
from lib.menu import Menu
from lib.setting import Setting
from lib.game import Game


def check_events(config, me, menu, setting, game):
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            config.save_config(game)
            exit()

        elif event.type is config.TRACK_END and config.MUSIC_STATE is config.MUSIC_STATE_PLAY:
            me.next_track(config)

        elif event.type is config.TIMER_TICK and config.GAME_STATE is config.GAME_STATE_GAMING:
            config.TIME += 1

        elif event.type is pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if config.GAME_STATE is config.GAME_STATE_SETTING:
                setting.check_setting_buttons_is_press(config, mouse_pos)

            else:
                me.check_media_button_is_press(config, mouse_pos)
                menu.check_utils_button_is_press(config, mouse_pos)

                if config.GAME_STATE is config.GAME_STATE_MENU:
                    menu.check_menu_button_is_press(config, mouse_pos, game)

                elif config.GAME_STATE is config.GAME_STATE_GAMING:
                    # Left click
                    if event.button == 1:
                        if config.CELL_CLICK_INDEX[0] == -1:
                            game.cells.check_cell_button_is_press_left(config, mouse_pos)
                            game.check_game_button_is_press(config, mouse_pos)
                        else:
                            game.cells.check_expand_button_is_press_left(config, mouse_pos)

                    # Right click
                    elif event.button == 3:
                        game.cells.check_cell_button_is_press_right(config, mouse_pos)
                        game.check_right_click(config, mouse_pos)

                elif config.GAME_STATE is config.GAME_STATE_CLEAR:
                    game.check_clear_button_is_press(config, mouse_pos)

        elif event.type is pygame.MOUSEMOTION:
            if config.GAME_STATE is config.GAME_STATE_GAMING:
                if config.CELL_CLICK_INDEX[0] == -1:
                    game.cells.check_cell_button_is_over(config, event.pos)

                else:
                    game.cells.check_expand_button_is_over(config, event.pos)


def render(config, screen, me, menu, setting, themes, game):
    screen.blit(themes[config.SETTING_COLOR_THEME], (0, 0))
    me.render_buttons(screen)
    menu.render_utils_buttons(screen)

    if config.GAME_STATE is config.GAME_STATE_MENU \
            or config.GAME_STATE_PREV is config.GAME_STATE_MENU:
        menu.render_menu_buttons(config, screen)

    elif config.GAME_STATE is config.GAME_STATE_GAMING \
            or config.GAME_STATE_PREV is config.GAME_STATE_GAMING:
        game.render(config, screen)
        if config.CELL_CLICK_INDEX[0] != -1:
            game.cells.render_expand(config, screen)

    elif config.GAME_STATE is config.GAME_STATE_CLEAR:
        game.render_clear(config, screen)

    if config.GAME_STATE is config.GAME_STATE_SETTING:
        setting.render(config, screen)

    pygame.display.update()


def result_check(config):
    if config.GAME_STATE is config.GAME_STATE_GAMING and config.CELL_BUTTON_NUM == 0:
        config.GAME_STATE = config.GAME_STATE_PREV = config.GAME_STATE_CLEAR
        config.SAVE_DATA = None


def run():
    # Initialize pygame and other game modules
    pygame.mixer.pre_init(44100, 16, 2)
    pygame.init()

    config = Config()
    image_files = image.load(config)
    setting = Setting(config, image_files)
    menu = Menu(config, image_files)
    game = Game(config, image_files)
    themes = image.init_theme(config, image_files, setting)
    me = music.MusicEngine(config, image_files)
    me.play(config)

    # Create game window
    screen = pygame.display.set_mode(config.DISPLAY_RESOLUTION, config.DISPLAY_MODE, 32)
    pygame.display.set_caption("Sudoku")

    # Main Loop
    while True:
        check_events(config, me, menu, setting, game)
        render(config, screen, me, menu, setting, themes, game)
        result_check(config)
