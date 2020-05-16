#/usr/bin/python

"""
sudoku puzzle solver v1.0
"""

def cell():
	return set([ x for x in range(1,10) ])

def new_board():
	return [ cell() for i in range(81) ]

def set_val(board, x, y, val):
	board[y*9 + x] = {val}
	elim_poss(board, x, y, val)

def elim_poss(board, x, y, val):
	for i in range(9):
		if i != x and val in board[y*9 + i]:
			board[y*9 + i].remove(val)
	for i in range(9):
		if i != y and val in board[i*9 + x]:
			board[i*9 + x].remove(val)
	for i in range(3):
		for j in range(3):
			nx = 3 * (x // 3) + i
			ny = 3 * (y // 3) + j 
			if nx != x and ny != y and val in board[ny*9 + nx]:
				board[ny*9 + nx].remove(val)

def pretty_print(b):
	for i in range(9):
		print(b[i*9:i*9+9])	

b = new_board()
print(len(b))
idx = 0
with open("test_puzz.txt", 'r') as infile:
	for line in infile.readlines():
		for j, item in enumerate(line.strip().split(' ')):
			if item != '-':
				set_val(b, j, idx, int(item))
		idx += 1

solved = False
while not solved:
	for i in range(81):
		if len(b[i]) == 1:
			elim_poss(b, i%9, i//9, tuple(b[i])[0])
	if sum([ len(x) for x in b ]) == 81:
		pretty_print(b)
		solved = True
	else:
		print("Solving...")
