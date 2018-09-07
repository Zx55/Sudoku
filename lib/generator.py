# -*- coding:utf-8 -*-

try:
    import lib._generator as gt

    class Generator:
        def __init__(self, config):
            self.generator = gt.new_Generator()
            config.API_FOUND = True

        def set_seed(self, seed):
            gt.Generator_set_seed(self.generator, seed)

        def set_difficulty(self, difficulty):
            gt.Generator_set_difficulty(self.generator, difficulty)

        def generate_sudoku(self):
            gt.Generator_generate(self.generator)

        def destroy_generator(self):
            gt.delete_Generator(self.generator)

except ModuleNotFoundError:
    class Generator:
        def __init__(self, config):
            config.API_FOUND = False
