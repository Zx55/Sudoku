#pragma once

#ifndef DANCING_LINK_H
#define DANCING_LINK_H

#include <vector>

const int N = 81;
// 1 + 81 * 4 + 9 * 9 * 9 * 4
const int NODES_SIZE = 3241;
const int HEADS_SIZE = 400;
const int STACK_SIZE = 100;

struct Node;
using Column = Node;

struct Node {
	Node *up, *down, *left, *right;
	Column *head;
	int index, size;
};

class DancingLink {
public:
	explicit DancingLink(int *problem);
	DancingLink();
	DancingLink(const DancingLink &dl) = delete;
	DancingLink(DancingLink &&dl) = delete;
	DancingLink &operator=(const DancingLink &dl) = delete;
	DancingLink &operator=(DancingLink &&dl) = delete;
	~DancingLink() = default;

	bool solve();
	int *solution();
	void change_problem(int *problem);

private:
	int _problem[81];

	Column *_head;
	Column *_heads[HEADS_SIZE];

	std::vector<Node *> _stk;

	Node _nodes_alloc[NODES_SIZE];
	int _index_alloc;

	bool _rows[N][10];
	bool _cols[N][10];
	bool _cells[N][10];

	void init(const int *problem);

	void create_cols();
	void create_rows();
	Column *create_col(int n);
	void append_col(int n);
	Node *create_row(int col);
	static void push_left(Column *c1, Column *c2);
	static void push_up(Column *col, Node *row);

	static int get_row_col(int row, int val);
	static int get_col_col(int col, int val);
	static int get_cell_col(int cell, int val);
	Column *get_min_col() const;

	static void remove(Column *col);
	static void restore(Column *col);
};

#endif // DANCING_LINK_H
