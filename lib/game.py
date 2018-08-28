# -*- coding:utf-8 -*-

import pygame
from lib.const import Config
from lib.music import *


def loop(config, music_files):
    """
    Main Loop
    :param config: Game config
    :param music_files: Music list
    :return:
    """
    screen = pygame.display.set_mode(config.DISPLAY_RESOLUTION,
                                     config.DISPLAY_MODE, 32)
    pygame.display.set_caption("Soduku")

    track_end = pygame.USEREVENT + 1
    music_play(config, music_files)

    while True:
        print(config.MUSIC_STATE)
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                return

            elif event.type is track_end and config.MUSIC_STATE is \
                    config.MUSIC_STATE_PLAY:
                music_next(config, music_files)

            elif event.type is pygame.MOUSEBUTTONDOWN:
                pass

            elif event.type is pygame.KEYDOWN:
                if event.key is pygame.K_k:
                    music_pause(config)
                elif event.key is pygame.K_j:
                    music_play(config, music_files)
                elif event.key is pygame.K_s:
                    music_stop(config)
                elif event.key is pygame.K_n:
                    music_next(config, music_files)
                elif event.key is pygame.K_p:
                    music_prev(config, music_files)

        screen.fill((255, 255, 255))
        pygame.display.update()


def run():
    """
    Game start
    :return: None
    """

    # Initialize pygame
    config = Config()

    music_files = music_init(config)
    print(music_files)
    pygame.init()

    loop(config, music_files)


run()
