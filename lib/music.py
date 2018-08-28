# -*- coding:utf-8 -*-

import pygame
from os import listdir


def load_music(config):
    """
    from ../sound load music
    :param config: Game config
    :return: A list of music filename
    """
    files = sorted(listdir(config.MUSIC_PATH))
    config.MUSIC_MAX_INDEX = len(files)

    if config.MUSIC_MAX_INDEX == 0:
        config.MUSIC_FILE_STATE = config.MUSIC_FILE_STATE_NOT_FOUND
    else:
        config.MUSIC_FILE_STATE = config.MUSIC_FILE_STATE_NORMAL

    return [config.MUSIC_PATH + r'/' + files[i] for i in range(len(files))]


def music_play(config, music_files):
    """
    Play music
    :param config: Game config
    :param music_files: Music list
    :return: None
    """
    if config.MUSIC_FILE_STATE is config.MUSIC_FILE_STATE_NORMAL:
        if config.MUSIC_STATE is config.MUSIC_STATE_PAUSE:
            pygame.mixer.music.unpause()
        elif config.MUSIC_STATE is config.MUSIC_STATE_STOP:
            pygame.mixer.music.play()
        elif config.MUSIC_STATE is config.MUSIC_STATE_INIT:
            pygame.mixer.music.load(music_files[config.MUSIC_INDEX])
            pygame.mixer.music.play()

        config.MUSIC_STATE = config.MUSIC_STATE_PLAY


def music_pause(config):
    """
    Pause music
    :param config: Game config
    :return: None
    """
    if config.MUSIC_STATE is config.MUSIC_STATE_PLAY:
        pygame.mixer.music.pause()
        config.MUSIC_STATE = config.MUSIC_STATE_PAUSE


def music_stop(config):
    """
    Stop music
    :param config: Game config
    :return: None
    """
    if config.MUSIC_STATE is not config.MUSIC_STATE_STOP:
        pygame.mixer.music.stop()
        config.MUSIC_STATE = config.MUSIC_STATE_STOP


def music_next(config, music_files):
    """
    Next music
    :param config: Game config
    :param music_files: Music list
    :return: None
    """
    config.MUSIC_INDEX = (config.MUSIC_INDEX + 1) % config.MUSIC_MAX_INDEX
    pygame.mixer.music.load(music_files[config.MUSIC_INDEX])
    pygame.mixer.music.play()


def music_prev(config, music_files):
    """
    Previous music
    :param config: Game config
    :param music_files: Music list
    :return: None
    """
    config.MUSIC_INDEX = (config.MUSIC_INDEX - 1) % config.MUSIC_MAX_INDEX
    pygame.mixer.music.load(music_files[config.MUSIC_INDEX])
    pygame.mixer.music.play()


def music_init(config):
    pygame.mixer.pre_init(44100, 16, 2)

    music_files = load_music(config)

    track_end = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(track_end)

    return music_files
