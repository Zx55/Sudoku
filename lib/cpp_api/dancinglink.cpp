#include "dancinglink.h"

DancingLink::DancingLink(int *problem)
{
	init(problem);
}

DancingLink::DancingLink() : _head(nullptr) {}

bool DancingLink::solve()
{
	if (_head->left == _head)
	{
		const auto sz = _stk.size();
		for (size_t i = 0; i < sz; ++i)
		{
			Node *n = _stk[i];

			int index = -1, val = -1;
			while (index == -1 || val == -1)
			{
				if (n->index < 100)
					index = n->index;
				else
					val = n->index % 10;
				n = n->right;
			}
			_problem[index] = val;
		}
		return true;
	}

	Column *const col = get_min_col();

	remove(col);
	for (Node *row = col->down; row != col; row = row->down)
	{
		_stk.push_back(row);
		for (Node *n = row->right; n != row; n = n->right)
			remove(n->head);

		if (solve())
			return true;

		_stk.pop_back();
		for (Node *n = row->left; n != row; n = n->left)
			restore(n->head);
	}
	restore(col);
	return false;
}

int *DancingLink::solution()
{
	return &_problem[0];
}

void DancingLink::change_problem(int *problem)
{
	init(problem);
}

void DancingLink::init(const int *problem)
{
	for (auto i = 0; i < N; ++i)
	{
		_problem[i] = problem[i];
	}

	_index_alloc = 0;
	_stk.clear();
	_stk.reserve(100);

	memset(_rows, 0, sizeof _rows);
	memset(_cols, 0, sizeof _cols);
	memset(_cells, 0, sizeof _cells);

	// Remove the filled grid.
	for (auto i = 0; i < N; ++i)
	{
		const int row = i / 9;
		const int col = i % 9;
		const int cell = row / 3 * 3 + col / 3;
		const int val = _problem[i];
		_rows[row][val] = true;
		_cols[col][val] = true;
		_cells[cell][val] = true;
	}

	create_cols();
	create_rows();
}

void DancingLink::create_cols()
{
	_head = create_col(0);
	_head->left = _head->right = _head;
	memset(_heads, 0, sizeof _heads);

	// The first 81 column describe if the grid is filled.
	for (int i = 0; i < N; ++i)
	{
		if (_problem[i] == 0)
			append_col(i);
	}

	// The next 243 columns constrain the number that each row, column and cell can be filled.
	for (int i = 0; i < 9; ++i)
	{
		for (int v = 1; v < 10; ++v)
		{
			if (!_rows[i][v])
				append_col(get_row_col(i, v));
			if (!_cols[i][v])
				append_col(get_col_col(i, v));
			if (!_cells[i][v])
				append_col(get_cell_col(i, v));
		}
	}
}

void DancingLink::create_rows()
{
	for (int i = 0; i < N; ++i)
	{
		if (_problem[i] == 0)
		{
			const int row = i / 9;
			const int col = i % 9;
			const int cell = row / 3 * 3 + col / 3;

			for (int v = 1; v < 10; ++v)
			{
				if (!(_rows[row][v] || _cols[col][v] || _cells[cell][v]))
				{
					Node *node_pos = create_row(i);
					Node *node_row = create_row(get_row_col(row, v));
					Node *node_col = create_row(get_col_col(col, v));
					Node *node_cell = create_row(get_cell_col(cell, v));
					push_left(node_pos, node_row);
					push_left(node_pos, node_col);
					push_left(node_pos, node_cell);
				}
			}
		}
	}
}

Column *DancingLink::create_col(int n)
{
	Column *col = &_nodes_alloc[_index_alloc++];

	col->left = col->right = col->up = col->down = col;
	col->head = col;
	col->index = n;

	return col;
}

void DancingLink::append_col(int n)
{
	Column *col = create_col(n);
	push_left(_head, col);
	_heads[n] = col;
}

Node *DancingLink::create_row(int col)
{
	Node *row = &_nodes_alloc[_index_alloc++];

	row->left = row->right = row->up = row->down = row;
	row->index = col;
	row->head = _heads[col];
	push_up(row->head, row);

	return row;
}

void DancingLink::push_left(Column *c1, Column *c2)
{
	c2->left = c1->left;
	c2->right = c1;
	c1->left->right = c2;
	c1->left = c2;
}

void DancingLink::push_up(Column *col, Node *row)
{
	row->up = col->up;
	row->down = col;
	col->up->down = row;
	col->up = row;

	++col->size;
	row->head = col;
}

inline int DancingLink::get_row_col(int row, int val)
{
	return 100 + row * 10 + val;
}

inline int DancingLink::get_col_col(int col, int val)
{
	return 200 + col * 10 + val;
}

inline int DancingLink::get_cell_col(int cell, int val)
{
	return 300 + cell * 10 + val;
}

Column *DancingLink::get_min_col() const
{
	int min_size = 10000;
	Column *ret = nullptr;

	for (Column *col = _head->right; col != _head; col = col->right)
	{
		if (col->size < min_size)
		{
			min_size = col->size;
			ret = col;

			if (col->size == 1)
				return ret;
		}
	}

	return ret;
}

void DancingLink::remove(Column *col)
{
	col->right->left = col->left;
	col->left->right = col->right;

	for (Node *row = col->down; row != col; row = row->down)
	{
		for (Node *n = row->right; n != row; n = n->right)
		{
			n->down->up = n->up;
			n->up->down = n->down;
			--n->head->size;
		}
	}
}

void DancingLink::restore(Column *col)
{
	for (Node *row = col->up; row != col; row = row->up)
	{
		for (Node *n = row->left; n != row; n = n->left)
		{
			++n->head->size;
			n->down->up = n;
			n->up->down = n;
		}
	}
	col->right->left = col;
	col->left->right = col;
}
