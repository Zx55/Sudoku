# -*- coding:utf-8 -*-

import pygame
from lib.const import Config
from lib.music import *
from lib.image import *
from lib.button import *


def loop(config, music_files, image_files):
    """
    Main Loop
    :param config: Game config
    :param music_files: Music list
    :param image_files: Image list
    :return: None
    """
    screen = pygame.display.set_mode(config.DISPLAY_RESOLUTION,
                                     config.DISPLAY_MODE, 32)
    pygame.display.set_caption("Soduku")

    media_buttons = load_media_button(config, image_files)

    track_end = pygame.USEREVENT + 1
    pygame.mixer.music.set_volume(1.)
    music_play(config, music_files, media_buttons)

    while True:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                return

            elif event.type is track_end and config.MUSIC_STATE is \
                    config.MUSIC_STATE_PLAY:
                music_next(config, music_files)

            elif event.type is pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_media_button_is_press(config, music_files,
                                            media_buttons, (mouse_x, mouse_y))
                check_menu_button_is_press()

        screen.fill((220, 0, 100))
        render_media_button(media_buttons, screen)

        pygame.display.update()


def run():
    """
    Game start
    :return: None
    """

    # Initialize pygame
    config = Config()

    music_files = music_init(config)
    image_files = image_load(config)
    print(music_files, image_files)
    pygame.init()

    loop(config, music_files, image_files)
