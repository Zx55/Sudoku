# -*- coding:utf-8 -*-

import sys


api_path = r"./lib/_generator.cp36-win_amd64.pyd"
sys.path.insert(0, api_path)

try:
    import _generator

    class Generator:
        def __init__(self, config):
            self.generator = _generator.new_Generator()
            config.API_FOUND = True

        def set_seed(self, seed):
            _generator.Generator_set_seed(self.generator, seed)

        def set_difficulty(self, difficulty):
            _generator.Generator_set_difficulty(self.generator, difficulty)

        def generate_sudoku(self):
            _generator.Generator_generate(self.generator)

        def destroy_generator(self):
            _generator.delete_Generator(self.generator)

except ModuleNotFoundError:
    class Generator:
        def __init__(self, config):
            config.API_FOUND = False
