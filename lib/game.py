# -*- coding:utf-8 -*-

import pygame
from sys import exit
import lib.image as image
import lib.music as music
from lib.button import *
from lib.menu import Menu
from lib.setting import Setting


def check_events(config, me, menu, setting):
    """
    Handle all pygame events
    :param config: Global game config
    :param me: Game MusicEngine
    :param menu: Menu Surface
    :param setting: Setting Surface
    :return: None
    """
    track_end = pygame.USEREVENT + 1

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            config.save_config()
            exit()

        elif event.type is track_end and config.MUSIC_STATE is config.MUSIC_STATE_PLAY:
            me.next_track(config)

        elif event.type is pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if config.GAME_STATE is config.GAME_STATE_SETTING:
                setting.check_setting_buttons_is_press(config, mouse_pos)

            else:
                me.check_media_button_is_press(config, mouse_pos)
                menu.check_utils_button_is_press(config, mouse_pos)

                if config.GAME_STATE is config.GAME_STATE_MENU:
                    menu.check_menu_button_is_press()


def render(config, screen, me, menu, setting, themes):
    """
    Draw all elements on the game window
    :param config: Global game config
    :param screen: Game window
    :param me: Game MusicEngine
    :param menu: Menu Surface
    :param setting: Setting Surface
    :param themes: All game color themes
    :return: None
    """
    screen.blit(themes[config.SETTING_COLOR_THEME], (0, 0))
    me.render_buttons(screen)
    menu.render_utils_buttons(screen)

    if config.GAME_STATE is not config.GAME_STATE_GAMING:
        menu.render_menu_buttons(screen)
    elif config.GAME_STATE is not config.GAME_STATE_MENU:
        pass

    if config.GAME_STATE is config.GAME_STATE_SETTING:
        setting.render(config, screen)

    pygame.display.update()


def run():
    """
    Game start
    :return: None
    """
    # Initialize pygame and other game modules
    pygame.mixer.pre_init(44100, 16, 2)
    pygame.init()

    config = Config()
    image_files = image.load(config)
    setting = Setting(config, image_files)
    menu = Menu(config, image_files)
    themes = image.init_theme(config, image_files, setting)
    me = music.MusicEngine(config, image_files)
    me.play(config)

    # Create game window
    screen = pygame.display.set_mode(config.DISPLAY_RESOLUTION, config.DISPLAY_MODE, 32)
    pygame.display.set_caption("Soduku")

    # Main Loop
    while True:
        check_events(config, me, menu, setting)
        render(config, screen, me, menu, setting, themes)
