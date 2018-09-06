# -*- coding:utf-8 -*-

import pygame
from copy import deepcopy
from lib.button import Button


class Cell:
    def __init__(self, config, image_files, no, pos):
        self.index = None

        self.no = no
        self.pos = pos
        self.cell_bias = config.CELL_BUTTON_BIAS
        self.expand_bias = config.EXPAND_NUM_BIAS

        self.buttons = []
        self.expand_buttons = [Button(i, (0, 0),
                                      pygame.image.load(image_files[config.EXPAND_NUM + i]), None,
                                      pygame.image.load(image_files[config.EXPAND_NUM_OVER + i]), None)
                               for i in range(9)]

    def read(self, config, data, button_cell, nums_new, nums_new_over):
        a, b = self.no % 3 * 3, self.no // 3 * 3
        self.index = [(i, j) for i in range(b, b + 3) for j in range(a, a + 3)]

        x, y = self.pos
        k = 0
        for l in range(9):
            i, j = self.index[l]
            bias_x, bias_y = self.cell_bias[l]
            if data[i][j] == 0:
                self.buttons.append(Button([i, j, l, k], (x + bias_x, y + bias_y),
                                           button_cell[0], None, button_cell[1], None))
                config.CELL_BUTTON_NUM += 1
                k += 1

            elif data[i][j] < 0:
                self.buttons.append(Button([i, j, l, k], (x + bias_x, y + bias_y),
                                           nums_new[-data[i][j] - 1], None,
                                           nums_new_over[-data[i][j] - 1], None))
                k += 1

    def render_button(self, surface):
        for button in self.buttons:
            button.render(surface)


class Cells:
    def __init__(self, config, image_files):
        self.cells = [Cell(config, image_files, i, config.CELL_POS[i]) for i in range(9)]
        self.data = deepcopy(config.PROBLEM)

        self.cell_surface = pygame.image.load(image_files[config.CELL_SURFACE])
        self.button_cell = [
                pygame.image.load(image_files[config.BUTTON_CELL]),
                pygame.image.load(image_files[config.BUTTON_CELL_OVER])
            ]

        self.button_cell_expand = pygame.image.load(image_files[config.CELL_BUTTON_EXPAND])
        self.nums_builtin = [pygame.image.load(image_files[i + config.CELL_NUM_BUILTIN])
                             for i in range(9)]
        self.nums_new = [pygame.image.load(image_files[i + config.CELL_NUM_NEW])
                         for i in range(9)]
        self.nums_new_over = [pygame.image.load(image_files[i + config.CELL_NUM_NEW_OVER])
                              for i in range(9)]

        self.highlight = [
                pygame.image.load(image_files[config.HIGHLIGHT_ROW]),
                pygame.image.load(image_files[config.HIGHLIGHT_ROW + 1])
            ]

        for i in range(9):
            self.cells[i].read(config, self.data, self.button_cell, self.nums_new, self.nums_new_over)

    def check_cell_button_is_over(self, config, point):
        config.CELL_OVER_INDEX[0] = -1

        for no in range(9):
            cell = self.cells[no]
            for button in cell.buttons:
                i, j, k, _ = button.label
                if button.is_press(point):
                    config.CELL_OVER_INDEX = [no, k]
                    if self.data[i][j] == 0:
                        button.change_state(True)

                    elif self.data[i][j] < 0:
                        button.change_image(self.nums_new_over[-self.data[i][j] - 1])

                else:
                    if self.data[i][j] == 0:
                        button.change_state(False)

                    elif self.data[i][j] < 0:
                        button.change_image(self.nums_new[-self.data[i][j] - 1])

    def check_cell_button_is_press_left(self, config, point):
        for cell in self.cells:
            for button in cell.buttons:
                if button.is_press(point) and config.CELL_CLICK_INDEX[0] == -1:
                    config.CELL_CLICK_INDEX = [cell.no, *button.label]
                    config.CELL_BUTTON_POSSIBLE = [1] * 9

                    if config.SETTING[config.SETTING_SHOW_POSSIBLE] == 1:
                        self.check_possible(config)

                    self.check_expand_button_is_over(config, point)

    def check_cell_button_is_press_right(self, config, point):
        if config.CELL_CLICK_INDEX[0] == -1:
            for no in range(9):
                cell = self.cells[no]
                for button in cell.buttons:
                    i, j, _, k = button.label
                    if button.is_press(point) and self.data[i][j] < 0:
                        push(config.UN_STK, (no, i, j, k, self.data[i][j]))
                        button.change_image(self.button_cell[0], self.button_cell[1])
                        self.data[i][j] = 0
                        config.CELL_BUTTON_NUM += 1

    def check_expand_button_is_over(self, config, point):
        cell = self.cells[config.CELL_CLICK_INDEX[0]]
        possible = config.CELL_BUTTON_POSSIBLE

        for i in range(9):
            button = cell.expand_buttons[i]

            if possible[i] == 1 and button.is_press(point):
                button.change_state(True)

            else:
                button.change_state(False)

    def check_expand_button_is_press_left(self, config, point):
        cell = self.cells[config.CELL_CLICK_INDEX[0]]
        possible = config.CELL_BUTTON_POSSIBLE

        for l in range(9):
            button = cell.expand_buttons[l]

            if possible[l] == 1 and button.is_press(point):
                no, i, j, _, k = config.CELL_CLICK_INDEX
                if self.data[i][j] == 0:
                    config.CELL_BUTTON_NUM -= 1

                push(config.UN_STK, (no, i, j, k, self.data[i][j]))

                num = button.label + 1
                self.data[i][j] = -num
                cell.buttons[k].change_image(self.nums_new[num - 1])
                config.CELL_CLICK_INDEX[0] = -1
                config.CELL_OVER_INDEX[0] = -1

    def check_possible(self, config):
        no, i, j, _, _ = config.CELL_CLICK_INDEX

        if no != -1:
            possible = [1] * 9
            cell = self.cells[no]

            for k in range(9):
                if self.data[i][k] != 0:
                    possible[abs(self.data[i][k]) - 1] = 0

                if self.data[k][j] != 0:
                    possible[abs(self.data[k][j]) - 1] = 0

                index_x, index_y = cell.index[k]
                if self.data[index_x][index_y] != 0:
                    possible[abs(self.data[index_x][index_y]) - 1] = 0

            config.CELL_BUTTON_POSSIBLE = possible

    def check_clear(self, config):
        for i in range(9):
            for j in range(9):
                if self.data[i][j] < 0 and self.data[i][j] != -config.SOLUTION[i][j]:
                    return False
        return True

    def undo(self, config):
        if not is_empty(config.UN_STK):
            no, i, j, k, item = pop(config.UN_STK)
            push(config.RE_STK, (no, i, j, k, self.data[i][j]))

            if item == 0:
                self.cells[no].buttons[k].change_image(self.button_cell[0])
                config.CELL_BUTTON_NUM += 1

            else:
                self.cells[no].buttons[k].change_image(self.nums_new[-item - 1])
                if self.data[i][j] == 0:
                    config.CELL_BUTTON_NUM -= 1

            self.data[i][j] = item

    def redo(self, config):
        if not is_empty(config.RE_STK):
            no, i, j, k, item = pop(config.RE_STK)
            push(config.UN_STK, (no, i, j, k,  self.data[i][j]))

            if item == 0:
                self.cells[no].buttons[k].change_image(self.button_cell[0])
                config.CELL_BUTTON_NUM += 1

            else:
                self.cells[no].buttons[k].change_image(self.nums_new[-item - 1])
                if self.data[i][j] == 0:
                    config.CELL_BUTTON_NUM -= 1

            self.data[i][j] = item

    def render_highlight(self, config, surface):
        no_raw = config.CELL_OVER_INDEX[0] // 3 * 3
        no_col = config.CELL_OVER_INDEX[0] % 3
        bias = self.cells[0].cell_bias
        k = config.CELL_OVER_INDEX[1]

        for i in range(3):
            x, y = self.cells[no_raw + i].pos
            surface.blit(self.highlight[0], (x, y + bias[k][1]))

            x, y = self.cells[no_col + i * 3].pos
            surface.blit(self.highlight[1], (x + bias[k][0], y))

    def render_expand(self, config, surface):
        cell = self.cells[config.CELL_CLICK_INDEX[0]]
        k = config.CELL_CLICK_INDEX[-2]
        x, y = cell.pos
        expand_pos = (x + cell.cell_bias[k][0] - 20, y + cell.cell_bias[k][1] - 20)
        surface.blit(self.button_cell_expand, expand_pos)

        possible = config.CELL_BUTTON_POSSIBLE
        for i in range(9):
            if possible[i] == 1:
                button = cell.expand_buttons[i]
                button.x = expand_pos[0] + cell.expand_bias[button.label][0]
                button.y = expand_pos[1] + cell.expand_bias[button.label][1]
                button.render(surface)

    def render(self, config, surface):
        for cell in self.cells:
            surface.blit(self.cell_surface, cell.pos)

        if config.SETTING[config.SETTING_SHOW_HIGHLIGHT] is config.SETTING_ON \
                and config.CELL_OVER_INDEX[0] != -1:
            self.render_highlight(config, surface)

        for cell in self.cells:
            x, y = cell.pos
            for k in range(9):
                i, j = cell.index[k]
                bias_x, bias_y = config.CELL_BUTTON_BIAS[k]

                if self.data[i][j] > 0:
                    surface.blit(self.nums_builtin[self.data[i][j] - 1], (x + bias_x, y + bias_y))

            for button in cell.buttons:
                button.render(surface)


def push(stk, item):
    stk[0].append(item)
    stk[1] += 1


def pop(stk):
    item = stk[0].pop(-1)
    stk[1] -= 1
    return item


def top(stk):
    return stk[0][-1]


def is_empty(stk):
    return stk[1] == 0
