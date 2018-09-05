# -*- coding:utf-8 -*-

from os import listdir
from lib.setting import *


def load(config):
    files = sorted(listdir(config.IMAGE_PATH))

    if len(files) == 0:
        config.IMAGE_FILE_STATE = config.IMAGE_FILE_STATE_NOT_FOUND

    else:
        config.IMAGE_FILE_STATE = config.IMAGE_FILE_STATE_NORMAL

    return [config.IMAGE_PATH + r'/' + files[i] for i in range(len(files))]


def load_theme(config, image_files):
    themes = []

    for theme in config.THEMES_720:
        themes.append(pygame.image.load(image_files[theme]))
        themes.append(pygame.image.load(image_files[theme + 1]))

    return themes


def init_theme(config, image_files, setting):
    themes = load_theme(config, image_files)
    setting.random_theme(config)
    return themes
