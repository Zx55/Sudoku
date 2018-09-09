#include "generator.h"

std::mt19937 Generator::_mt;

Generator::Generator(long long s) : _seed(s), _has_seed(true), _difficulty(_seed % 3)
{
    memset(_item.problem, 0, sizeof _item.problem);
    memset(_item.solution, 0, sizeof _item.solution);

    set_difficulty(_difficulty);
}

Generator::Generator() : _has_seed(false)
{
    memset(_item.problem, 0, sizeof _item.problem);
    memset(_item.solution, 0, sizeof _item.solution);
}

void Generator::set_seed(long long s)
{
    _seed = s;
    _has_seed = true;
    _difficulty = _seed % 3;
    set_difficulty(_difficulty);
}

void Generator::set_difficulty(int difficulty)
{
    _difficulty = difficulty % 3;
    const auto bias = _mt() % 5;

    switch (_difficulty)
    {
    case difficulty_easy:
        _given = 36 + bias; // 36~40
        _bound = 3;
        break;
    case difficulty_normal:
        _given = 28 + bias; // 28~32
        _bound = 1;
        break;
    default:
        _given = 22 + bias; // 22~26
        _bound = 0;
        break;
    }
}

void Generator::show_sudoku(int *ar)
{
    putchar('\n');
    auto row = 0, col = 0;
    auto flag = true;
    for (auto i = 0; i < N; ++i)
    {
        if (col % 3 == 0 && i != 0)
        {
            printf("| ");
        }
        if (i % 9 == 0 && i != 0)
            putchar('\n');

        if (flag && row % 3 == 0)
        {
            puts(" ----------------------");
            flag = false;
        }

        if (i % 9 == 0)
            putchar('|');

        printf("%d ", ar[i]);

        if (++col > 8)
        {
            ++row;
            flag = true;
            col = 0;
        }
    }
    printf("|\n ----------------------\n");
}

void Generator::generate()
{
    if (!_has_seed)
        _seed = std::time(nullptr);
    _mt.seed(static_cast<unsigned int>(_seed));

    int holes, bound;

    switch (_difficulty)
    {
    case difficulty_easy:
        bound = 40;
        break;
    case difficulty_normal:
        bound = 32;
        break;
    default:
        bound = 26;
        break;
    }

    do
    {
        generate_solution();
        holes = dig_holes();
    } while (holes > bound);

    propagation();
    write_json();
}

void Generator::generate_solution()
{
    bool flag;

    std::vector<std::vector<int>> index{
        {0, 1, 2, 9, 10, 11, 18, 19, 20},
        {30, 31, 32, 39, 40, 41, 48, 49, 50},
        {60, 61, 62, 69, 70, 71, 78, 79, 80}};

    do
    {
        memset(_item.solution, 0, sizeof _item.solution);

        for (auto i = 0; i < 3; ++i)
        {
            shuffle(index[i].begin(), index[i].end(), _mt);
            for (auto j = 0; j < 9; ++j)
            {
                _item.solution[index[i][j]] = j + 1;
            }
        }

        _dlx.change_problem(_item.solution);
        flag = _dlx.solve();
    } while (!flag);

    const auto solution = _dlx.solution();
    for (auto i = 0; i < N; ++i)
    {
        _item.solution[i] = solution[i];
    }
}

int Generator::dig_holes()
{
    for (auto i = 0; i < N; ++i)
        _item.problem[i] = _item.solution[i];

    const int pre_dig[] = {0, 1, 2, 3, 4, 5, 9, 15, 16, 17, 18, 27, 30, 33, 36, 45, 55, 57, 60, 64, 73};
    for (int i : pre_dig)
    {
        _item.problem[i] = 0;
    }

    int row_left[] = {3, 5, 8, 6, 8, 8, 6, 8, 8};
    int col_left[] = {3, 5, 8, 6, 8, 8, 6, 8, 8};

    int i, j, row = 0, col = 6;
    for (i = N - 21, j = 6; i >= _given && j < 81; ++j)
    {
        if (_item.problem[j] != 0 && row_left[row] > _bound &&
            col_left[col] > _bound)
        {
            const auto tmp = _item.problem[j];
            bool flag = true;

            for (auto k = 1; k <= 9; ++k)
            {
                if (k != tmp)
                {
                    _item.problem[j] = k;
                    _dlx.change_problem(_item.problem);
                    if (_dlx.solve())
                    {
                        flag = false;
                        break;
                    }
                }
            }

            if (!flag)
                _item.problem[j] = tmp;
            else
            {
                _item.problem[j] = 0;
                --i, --row_left[row], --col_left[col];
            }
        }

        if (++col > 8)
        {
            ++row;
            col = 0;
        }
    }

    return i;
}

int Generator::dig_holes_pack()
{
    for (auto i = 0; i < N; ++i)
        _item.problem[i] = _item.solution[i];

    int pack[] = {
        511, 511, 511, 511, 511, 511, 511, 511, 511, // rows
        511, 511, 511, 511, 511, 511, 511, 511, 511, // cols
        511, 511, 511, 511, 511, 511, 511, 511, 511, // cells
    };

    const int pre_dig[] = {0, 1, 2, 3, 4, 5, 9, 15, 16, 17, 18, 27, 30, 33, 36, 45, 55, 57, 60, 64, 73};
    for (auto i = 0; i < 21; ++i)
    {
        set_status(pack, i, _item.problem[pre_dig[i]]);
        _item.problem[pre_dig[i]] = 0;
    }

    int row_left[] = {3, 5, 8, 6, 8, 8, 6, 8, 8};
    int col_left[] = {3, 5, 8, 6, 8, 8, 6, 8, 8};

    int i, j, row = 0, col = 6;
    for (i = N - 21, j = 6; i >= _given && j < 81; ++j)
    {
        if (_item.problem[j] != 0 && row_left[row] > _bound &&
            col_left[col] > _bound)
        {
            const auto tmp = _item.problem[j];
            bool flag = true;

            int status = get_status(pack, row, col);
            for (auto k = 1; k <= 9; ++k)
            {
                if (k != tmp)
                {
                    if ((status & 0x1) == 0)
                    {
                        _item.problem[j] = k;
                        _dlx.change_problem(_item.problem);
                        if (_dlx.solve())
                        {
                            flag = false;
                            break;
                        }
                    }
                    status >>= 1;
                }
            }

            if (!flag)
                _item.problem[j] = tmp;
            else
            {
                set_status(pack, row, col, _item.problem[i]);
                _item.problem[j] = 0;
                --i, --row_left[row], --col_left[col];
            }
        }

        if (++col > 8)
        {
            ++row;
            col = 0;
        }
    }

    return i;
}

void Generator::propagation()
{
    const auto n = _mt() % 6 + 15;

    for (unsigned i = 0; i < n; ++i)
    {
        switch (_mt() % 5)
        {
        case 0:
            exchange_digit();
            break;
        case 1:
            exchange_row_random();
            break;
        case 2:
            exchange_col_random();
            break;
        case 3:
            exchange_row_block();
            break;
        default:
            exchange_col_block();
            break;
        }
    }
}

void Generator::write_json()
{
    std::FILE *fp = std::fopen(".\\data\\generate_data.json", "w");

    const auto sz = N - 1;
    std::fprintf(fp, "[[");
    for (auto i = 0; i < sz; ++i)
        std::fprintf(fp, "%d, ", _item.solution[i]);
    std::fprintf(fp, "%d], [", _item.solution[80]);

    for (auto i = 0; i < sz; ++i)
        std::fprintf(fp, "%d, ", _item.problem[i]);
    std::fprintf(fp, "%d]]", _item.problem[80]);

    std::fclose(fp);
}

void Generator::exchange_digit()
{
    const auto num1 = _mt() % 8 + 1;
    auto num2 = _mt() % 8 + 1;
    while (num1 == num2)
        num2 = _mt() % 8 + 1;

    for (auto i = 0; i < N; ++i)
    {
        if (_item.solution[i] == num1)
        {
            _item.solution[i] = num2;

            if (_item.problem[i] != 0)
                _item.problem[i] = num2;
        }
        else if (_item.solution[i] == num2)
        {
            _item.solution[i] = num1;

            if (_item.problem[i] != 0)
                _item.problem[i] = num1;
        }
    }
}

void Generator::exchange_row_random()
{
    const auto block = _mt() % 3;
    const auto exclude_row = _mt() % 3;
    const auto row1 = (exclude_row + 1) % 3 + block * 3;
    const auto row2 = (exclude_row + 2) % 3 + block * 3;

    exchange_row(row1, row2);
}

void Generator::exchange_col_random()
{
    const auto block = _mt() % 3;
    const auto exclude_col = _mt() % 3;
    const auto col1 = (exclude_col + 1) % 3 + block * 3;
    const auto col2 = (exclude_col + 2) % 3 + block * 3;

    exchange_col(col1, col2);
}

void Generator::exchange_row_block()
{
    const auto exclude_block = _mt() % 3;
    const auto block1 = (exclude_block + 1) % 3;
    const auto block2 = (exclude_block + 2) % 3;

    const auto row1 = block1 * 3;
    const auto row2 = block2 * 3;
    for (auto i = 0; i < 3; ++i)
        exchange_row(row1 + i, row2 + i);
}

void Generator::exchange_col_block()
{
    const auto exclude_block = _mt() % 3;
    const auto block1 = (exclude_block + 1) % 3;
    const auto block2 = (exclude_block + 2) % 3;

    const auto col1 = block1 * 3;
    const auto col2 = block2 * 3;
    for (auto i = 0; i < 3; ++i)
        exchange_col(col1 + i, col2 + i);
}

void Generator::swap(int *ar, int i, int j)
{
    const auto tmp = ar[i];
    ar[i] = ar[j];
    ar[j] = tmp;
}

void Generator::exchange_row(const unsigned row1, const unsigned row2)
{
    for (unsigned i = 0, j = row1 * 9, k = row2 * 9; i < 9; ++i, ++j, ++k)
    {
        swap(_item.solution, j, k);
        swap(_item.problem, j, k);
    }
}

void Generator::exchange_col(const unsigned col1, const unsigned col2)
{
    for (unsigned i = 0, j = i * 9 + col1, k = i * 9 + col2;
         i < 9; ++i, j += 9, k += 9)
    {
        swap(_item.solution, j, k);
        swap(_item.problem, j, k);
    }
}

void Generator::set_status(int *pack, int n, int val)
{
    const int row = n / 9;
    const int col = n % 9;
    const int cell = row / 3 * 3 + col / 3;

    const int mask = ~(1 << (val - 1));
    pack[row] &= mask;
    pack[9 + col] &= mask;
    pack[18 + cell] &= mask;
}

void Generator::set_status(int *pack, int row, int col, int val)
{
    const int cell = row / 3 * 3 + col / 3;

    const int mask = ~(1 << (val - 1));
    pack[row] &= mask;
    pack[9 + col] &= mask;
    pack[18 + cell] &= mask;
}

int Generator::get_status(const int *pack, int row, int col)
{
    const int cell = row / 3 * 3 + col / 3;

    return pack[row] & pack[9 + col] & pack[18 + cell];
}
