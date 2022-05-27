"""
Solves a grid puzzle involving numbers on a grid.

1) The numbers 1, 2, 3, and 4 are on a square grid.
2) No two of the same number may be within a chess "Knight's move" away.
3) No more than two of the same number may occupy the same Row or Column of the grid.

The number 0 represents an empty space.

"""

import math

puzzle = ['030000',
	  '000044',
	  '000000',
	  '000000',
	  '030000',
	  '000011']


puzzle = ''.join(puzzle) # convert to 1D string
dim = int(math.sqrt(len(puzzle))) # length of side


"""
provided an X and Y coordinate, convert to the
index in a flat array, or None if out of bounds.
"""
def convert_idx(x,y):
	if x < 0 or x >= dim or y < 0 or y >= dim:
		return None
	return y*dim+x

"""
verify that the provided puzzle string
does not violate the row or column rule
"""
def check_rows_cols(board):
	for i in range(dim):
		for check in "1234":
			if board[i*dim:i*dim+dim].count(check) > 2:
				return False
			if ''.join([board[i+j*dim] for j in range(dim)]).count(check) > 2:
				return False
	return True

"""
verify that the provided index of the puzzle string
does not violate the "Knight's move" rule
"""
def check_knight_moves(idx, board):
	knight_move_deltas = [ (2,1),(2,-1),(-2,1),(-2,-1),(-1,2),(1,-2),(-1,-2),(1,2) ]
	x,y = idx%dim,idx//dim
	for dx,dy in knight_move_deltas:
		new_idx = convert_idx(x+dx,y+dy)
		if new_idx != None:
			if board[new_idx] == board[idx]:
				return False
	return True

"""
provided a list of sets of possible values, reduce the set
to the minimum number by eliminating possiblities that are
a knight's move away.  Return the new set of possible values
for each location, or None if the solution is impossible.
"""
def do_set_elim(poss_sets):
	knight_move_deltas = [ (2,1),(2,-1),(-2,1),(-2,-1),(-1,2),(1,-2),(-1,-2),(1,2) ]
	new_poss_sets = [ x.copy() for x in poss_sets ]
	changed = True
	while changed:
		changed = False
		for idx in range(len(new_poss_sets)):
			if len(new_poss_sets[idx]) == 1:
				x,y = idx%dim,idx//dim
				for dx,dy in knight_move_deltas:
					new_idx = convert_idx(x+dx,y+dy)
					if new_idx != None:
						curr_len = len(new_poss_sets[new_idx])
						new_poss_sets[new_idx].discard(list(new_poss_sets[idx])[0])
						if len(new_poss_sets[new_idx]) == 0:
							return None
						if len(new_poss_sets[new_idx]) != curr_len:
							changed = True
	return new_poss_sets

def solve(puzzle,poss_sets):
	if '0' not in puzzle:
		if False not in { check_knight_moves(i,puzzle) for i in range(len(puzzle)) } and check_rows_cols(puzzle):
			print(puzzle)
	elif poss_sets != None and check_rows_cols(puzzle):
		first_zero = puzzle.index('0')
		for num in list(poss_sets[first_zero]):
			new_poss_sets = [ x for x in poss_sets ]
			new_poss_sets[first_zero] = set(num)
			new_poss_sets = do_set_elim(new_poss_sets)
			solve(puzzle[0:first_zero]+num+puzzle[first_zero+1:],new_poss_sets)
			
init_poss_sets = []
for num in puzzle:
	if num == '0':
		init_poss_sets.append( {'1','2','3','4' } )
	else:
		init_poss_sets.append( { num } )

solve(puzzle,init_poss_sets)
						
			

