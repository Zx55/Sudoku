#pragma once
#ifndef GENERATOR_H
#define GENERATOR_H
#define _CRT_SECURE_NO_WARNINGS
#include "dancinglink.h"
#include <ctime>
#include <random>
#include <algorithm>

enum difficulty
{
    difficulty_easy,
    difficulty_normal,
    difficulty_hard
};

struct ReturnItem
{
    int solution[81];
    int problem[81];
    ReturnItem() = default;
    ~ReturnItem() = default;
};

class Generator
{
  public:
    explicit Generator(long long s);
    Generator();
    Generator(const Generator &g) = delete;
    Generator(Generator &&g) = delete;
    Generator &operator=(const Generator &g) = delete;
    Generator &operator=(Generator &&g) = delete;
    ~Generator() = default;

    void set_seed(long long s);
    void set_difficulty(int difficulty);
    static void show_sudoku(int *ar);
    ReturnItem ret() const
    {
        return _item;
    }

    void generate();

  private:
    static std::mt19937 _mt;

    DancingLink _dlx;

    ReturnItem _item;
    long long _seed = 0;
    bool _has_seed;
    int _difficulty;
    int _given;
    int _bound;

    void generate_solution();
    int dig_holes();
    int dig_holes_pack();
    void propagation();
    void write_json();

    void exchange_digit();
    void exchange_row_random();
    void exchange_col_random();
    void exchange_row_block();
    void exchange_col_block();
    // void grid_row();

    static void swap(int *ar, int i, int j);
    void exchange_row(unsigned row1, unsigned row2);
    void exchange_col(unsigned col1, unsigned col2);

    static void set_status(int *pack, int n, int val);
    static void set_status(int *pack, int row, int col, int val);
    static int get_status(const int *pack, int row, int col);
};

#endif // GENERATOR_H
