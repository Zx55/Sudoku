# -*- coding:utf-8 -*-


class Button:
    def __init__(self, name, position, image_normal, func_normal, image_press=None, func_press=None):
        self.label = name
        self.x, self.y = position

        self.image_normal = image_normal
        if image_press is not None:
            self.image_press = image_press
        else:
            self.image_press = None
        self.image = self.image_normal
        self.width, self.height = self.image.get_size()

        self.func_normal = func_normal
        self.func_press = func_press
        self.func = self.func_normal

    def is_press(self, point):
        point_x, point_y = point
        if self.x < point_x < self.x + self.width and self.y < point_y < self.y + self.height:
            return True

        else:
            return False

    def change_state(self, pressed):
        if pressed is True:
            self.image = self.image_press
            self.func = self.func_press

        else:
            self.image = self.image_normal
            self.func = self.func_normal
        self.width, self.height = self.image.get_size()

    def change_image(self, image_normal, image_press=None):
        self.image = self.image_normal = image_normal
        if image_press is not None:
            self.image_press = image_press

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))
