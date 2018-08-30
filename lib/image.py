# -*- coding:utf-8 -*-

from os import listdir
import pygame
from lib.setting import *


def load(config):
    """
    Load all images
    :param config: Global game config
    :return: All images
    """
    files = sorted(listdir(config.IMAGE_PATH))

    if len(files) == 0:
        config.IMAGE_FILE_STATE = config.IMAGE_FILE_STATE_NOT_FOUND
    else:
        config.IMAGE_FILE_STATE = config.IMAGE_FILE_STATE_NORMAL

    return [config.IMAGE_PATH + r'/' + files[i] for i in range(len(files))]


def load_theme(config, image_files):
    """
    Load all color themes
    :param config: Global game config
    :param image_files: Image list
    :return: Themes list
    """
    themes = []

    for theme in config.THEMES_720:
        themes.append(pygame.image.load(image_files[theme]))
        themes.append(pygame.image.load(image_files[theme + 1]))

    return themes


def init_theme(config, image_files, setting):
    """
    Initialize game' s theme
    :param config: Global game config
    :param image_files: Image list
    :param setting: Setting Surface
    :return: Themes list
    """
    themes = load_theme(config, image_files)
    setting.random_theme(config)
    return themes


# change png
# from lib.const import Config
#
# config = Config()
# config.IMAGE_PATH = r'../image/pic'
# images, filename = load(config)
# themes = load_theme(config, images)
#
# for i in range(8, 10):
#     pygame.image.save(themes[i], r"d:/png/" + filename[i + 15])
