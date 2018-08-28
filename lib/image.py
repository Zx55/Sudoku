# -*- coding:utf-8 -*-

import pygame
from os import listdir


def image_load(config):
    files = sorted(listdir(config.IMAGE_PATH))
    config.IMAGE_MAX_INDEX = len(files)

    if config.IMAGE_MAX_INDEX == 0:
        config.IMAGE_FILE_STATE = config.IMAGE_FILE_STATE_NOT_FOUND
    else:
        config.IMAGE_FILE_STATE = config.IMAGE_FILE_STATE_NORMAL

    return [config.IMAGE_PATH + r'/' + files[i] for i in range(len(files))]
