# Sudoku

BUAA软件学院程设大作业 <br>

A GUI sudoku game based on pygame and c/c++.

Pygame is responsible for processing logic and rendering game window, while c/c++ is dedicated to the algorithm of generating a sudoku game.

This program uses Las Vegas algorithm and Dancing Link X algorithm to generate a sudoku solution, then digs holes according 
to a specific strategy to generate a sudoku game.

You can see [Sudoku 
Puzzles Generating: from Easy to Evil](http://zhangroup.aporc.org/images/files/Paper_3485.pdf) and [Automatic Sudoku solving
 with DLX](https://code.google.com/archive/p/narorumo/wikis/SudokuDLX.wiki) in detail. The implementation of DLX algorithm 
 refers to [recipes/sudoku](https://github.com/chenshuo/recipes/tree/master/sudoku).