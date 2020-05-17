#!/usr/bin/python

"""
sudoku puzzle solver v1.2
"""

def cell():
	return set([ x for x in range(1,10) ])

def new_board():
	return [ cell() for i in range(81) ]

def set_val(board, x, y, val):
	board[y*9 + x] = {val}
	elim_poss(board, x, y, val)

def elim_poss(board, x, y, val):
	for i in range(9): # horizontal
		if i != x:
			board[y*9 + i].discard(val)
	for i in range(9): # vertical
		if i != y:
			board[i*9 + x].discard(val)
	for i in range(3): # sub-grid
		for j in range(3):
			nx = 3 * (x // 3) + i
			ny = 3 * (y // 3) + j 
			if not (nx == x and ny == y):
				board[ny*9 + nx].discard(val)

def pretty_print(b):
	for i in range(9):
		print(b[i*9:i*9+9])

def solve(b):
	while True:
		if sum( [ 1 for x in b if len(x) == 0 ] ) > 0:
			return # invalid solution path
		last_sum = sum([ len(x) for x in b ])
		for i in range(81):
			if len(b[i]) == 1:
				elim_poss(b, i%9, i//9, tuple(b[i])[0])
		if sum( [ 1 for x in b if len(x) == 0 ] ) > 0:
			return # invalid solution path
		if sum( [ 1 for x in b if len(x) == 1 ] ) == 81:
			pretty_print(b) # valid solution
			exit()
		if sum([ len(x) for x in b ]) == last_sum: # no changes
			# more than one poss at these squares
			elim_list = [ i for i,x in enumerate([ len(y) for y in b ]) if x > 1 ]
			for i in elim_list:
				for v in tuple(b[i]):
					c = [ set(x) for x in b ]
					set_val(c, i%9, i//9, v)
					solve(c)
					b[i].discard(v)
			return # no solution found

b = new_board()
idx = 0
with open("test_puzz_evil.txt", 'r') as infile:
	for line in infile.readlines():
		for j, item in enumerate(line.strip().split(' ')):
			if item != '-':
				set_val(b, j, idx, int(item))
		idx += 1

solve(b)
