# -*- coding:utf-8 -*-

import pygame
from os import listdir
from lib.button import *


class MusicEngine:
    """
    MusicEngine
    """
    def __init__(self, config, image_files):
        self.music_files = init(config)
        self.image_files = image_files
        self.buttons = self.load_button(config)

    def play(self, config):
        """
        Play music
        :param config: Global game config
        :return: None
        """
        if config.MUSIC_FILE_STATE is config.MUSIC_FILE_STATE_NORMAL:
            if config.MUSIC_STATE is config.MUSIC_STATE_PAUSE:
                pygame.mixer.music.unpause()
                self.buttons[0].change_state(False)
            elif config.MUSIC_STATE is config.MUSIC_STATE_STOP:
                pygame.mixer.music.play()
                self.buttons[0].change_state(False)
            elif config.MUSIC_STATE is config.MUSIC_STATE_INIT:
                pygame.mixer.music.load(self.music_files[config.MUSIC_INDEX])
                pygame.mixer.music.play()

            config.MUSIC_STATE = config.MUSIC_STATE_PLAY

    def pause(self, config):
        """
        Pause music
        :param config: Global game config
        :return: None
        """
        if config.MUSIC_STATE is config.MUSIC_STATE_PLAY:
            pygame.mixer.music.pause()
            config.MUSIC_STATE = config.MUSIC_STATE_PAUSE
            self.buttons[0].change_state(True)

    def stop(self, config):
        """
        Stop music
        :param config: Global game config
        :return: None
        """
        if config.MUSIC_STATE is not config.MUSIC_STATE_STOP:
            pygame.mixer.music.stop()
            config.MUSIC_STATE = config.MUSIC_STATE_STOP
            self.buttons[0].change_state(True)

    def next_track(self, config):
        """
        Play next music
        :param config: Global game config
        :return: None
        """
        config.MUSIC_INDEX = (config.MUSIC_INDEX + 1) % config.MUSIC_MAX_INDEX
        pygame.mixer.music.load(self.music_files[config.MUSIC_INDEX])
        config.MUSIC_STATE = config.MUSIC_STATE_PLAY
        self.buttons[0].change_state(False)
        pygame.mixer.music.play()

    def prev_track(self, config):
        """
        Play previous music
        :param config: Global game config
        :return: None
        """
        config.MUSIC_INDEX = (config.MUSIC_INDEX - 1) % config.MUSIC_MAX_INDEX
        pygame.mixer.music.load(self.music_files[config.MUSIC_INDEX])
        config.MUSIC_STATE = config.MUSIC_STATE_PLAY
        self.buttons[0].change_state(False)
        pygame.mixer.music.play()

    def mute_on(self, config):
        """
        Turn off sounds
        :param config: Global game config
        :return: None
        """
        pygame.mixer.music.set_volume(0.)
        config.MUSIC_MUTE_STATE = config.MUSIC_MUTE_STATE_ON
        self.buttons[4].change_state(True)

    def mute_off(self, config):
        """
        Turn on sounds
        :param config: Global game config
        :return: None
        """
        pygame.mixer.music.set_volume(1.)
        config.MUSIC_MUTE_STATE = config.MUSIC_MUTE_STATE_OFF
        self.buttons[4].change_state(False)

    def render_buttons(self, surface):
        """
        Draw all media buttons on the game window
        :param surface: Game window
        :return: None
        """
        for button in self.buttons:
            button.render(surface)

    def load_button(self, config):
        """
        Generate media buttons
        :param config: Global game config
        :return: Media buttons
        """
        return [
            Button(r"Play/Pause", config.PLAY_PAUSE_POS, self.image_files[config.BUTTON_PAUSE], self.pause,
                   self.image_files[config.BUTTON_PLAY], self.play),
            Button(r"Stop", config.STOP_POS, self.image_files[config.BUTTON_STOP], self.stop),
            Button(r"Next", config.NEXT_POS, self.image_files[config.BUTTON_NEXT], self.next_track),
            Button(r"Prev", config.PREV_POS, self.image_files[config.BUTTON_PREV], self.prev_track),
            Button(r"Mute", config.MUTE_POS, self.image_files[config.BUTTON_MUTE_OFF], self.mute_on,
                   self.image_files[config.BUTTON_MUTE_ON], self.mute_off)
        ]

    def check_media_button_is_press(self, config, point):
        """
        Judge whether each media button is pressed and control music accordingly
        :param config: Global game config
        :param point: Mouse position
        :return: None
        """
        for button in self.buttons:
            if button.is_press(point):
                button.func(config)


def load(config):
    """
    Load all music
    :param config: Global game config
    :return: All music's filename
    """
    files = sorted(listdir(config.MUSIC_PATH))
    config.MUSIC_MAX_INDEX = len(files)

    if config.MUSIC_MAX_INDEX == 0:
        config.MUSIC_FILE_STATE = config.MUSIC_FILE_STATE_NOT_FOUND
    else:
        config.MUSIC_FILE_STATE = config.MUSIC_FILE_STATE_NORMAL

    return [config.MUSIC_PATH + r'/' + files[i] for i in range(len(files))]


def init(config):
    """
    Initialize the pygame music module
    :param config: Global game config
    :return: All music's filename
    """
    track_end = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(track_end)
    pygame.mixer.music.set_volume(1.)

    return load(config)
