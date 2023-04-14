#!/usr/bin/python

"""
Ikebana

Fill in the gray squares with either black or white in a way that adheres to these three rules:
1) Whenever there are consecutive squares of the same color in a row or column, the full line of same-colored squares must have even length
2) Every square must share an edge with at least one same-colored square
3) There must be exactly one more white square than black square in the completed grid

"""

from collections import deque

# G - Gray
# B - Black
# W - White

puzz = ['GGGWB','GGGGG','WBBGG','GGGGW','GGBGG']
#puzz = ['GGBGG','WWGGW','WBGGG','WBBBG','WGBWG']
#puzz = ['GGGGG','GGGGG','GGGGG','GGGGG','GGGGG']
#puzz = ['GGGG','GGGG','GGGG']
#puzz = ['GGGGGGGG','GGGGGGGG','GGGGGGGG','GGGGGGGG','GGGGGGGG','GGGGGGGG','GGGGGGGG','GGGGGGGG']

dims = (len(puzz[0]),len(puzz))
needed_black_squares = (dims[0]*dims[1])//2
if dims[0]*dims[1] % 2 == 0:
	needed_black_squares -= 1

# Return true of an input line follows Rule #1
def even_length_line(line):
	if len(line) <= 1:
		return True
	if 'G' in line: # only evaluate a complete line
		return False
	last_col = line[0]
	length   = 1
	for idx in range(1,len(line)):
		if line[idx] != last_col:
			if length != 1 and length % 2 == 1:
				return False
			last_col = line[idx]
			length = 1
		else:
			length += 1
	if length != 1 and length % 2 == 1:
		return False
	return True

# transpose rows and columns of a puzzle
def transpose_puzz(puzz):
	new_puzz = []
	for i in range(dims[0]):
		new_row = ''
		for j in range(dims[1]):
			new_row += puzz[j][i]
		new_puzz.append(new_row)
	return new_puzz

# Given a full board as a 1D string, check the columns against Rule #1
def col_check(board):
	for i in range(dims[0]):
		col = ''.join( board[dims[0]*j+i] for j in range(dims[1]) )
		if not even_length_line(col):
			return False
	return True

# Generate a set of strings of lenght 'size' that follow Rule #1
def gen_all_valid_rows(size):
	pool = set()
	q = deque()
	q.append('B')
	q.append('W')
	while len(q) > 0:
		c = q.popleft()
		if len(c) == size and even_length_line(c):
			pool.add(c)
		elif len(c) < size:
			q.append(c+'B')
			q.append(c+'W')
	return pool

# Given a row from the puzzle and a pool of strings, return a set of strings that
# do not conflict with the known values
def row_filter(known,pool):
	for idx,char in enumerate(known):
		if char != 'G':
			pool = { x for x in pool if x[idx] == char }
	return pool

# Given a 1D string representing a board (e.g. appended rows) return True if 
# Rule #2 is satisified
def neighbor_check(board):
	if 'G' in board: # incomplete puzzle
		return False
	colors = dict()
	colors['B'] = set()
	colors['W'] = set()
	for col in range(dims[1]):
		for row in range(dims[0]):
			colors[board[col*dims[0]+row]].add((row,col))
	for pool in colors.values():
		for e in pool:
			x,y = e
			if not any( v in pool for v in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) ):
				return False
	return True

def pretty_print(board):
	for i in range(dims[1]):
		print(board[i*dims[0]:i*dims[0]+dims[0]], end=' ')
		num_b = board[i*dims[0]:i*dims[0]+dims[0]].count('B') % 10
		print(num_b)
	print("-------")

# Return a new tuple of lists containing sets of still
# valid rows and columns after eliminating those that
# cannot be possible based on constraints.  The constraint
# to consider is either only one string for a row or column or 
# only one color at a given board position.  If any set size is 
# 0, there are no valid solutions given the input, and return
# (None, None) instead.
def do_set_elim(rows,cols):
	curr_poss_sets = -1 
	while curr_poss_sets != sum( [ len(x) for x in rows ]) + sum( [ len(x) for x in cols ] ):
		curr_poss_sets = sum( [ len(x) for x in rows ]) + sum( [ len(x) for x in cols ] )
		for idx,r in enumerate(rows):
			for jdx in range(len(cols)):
				if len(r) == 1 or len( { x[jdx] for x in r } ) == 1:
					forced_color = list(r)[0][jdx]
					next_cols = set()
					for c in cols[jdx]:
						if c[idx] == forced_color:
							next_cols.add(c)
					if len(next_cols) == 0:
						return (None,None)
					cols[jdx] = next_cols
		for jdx,c in enumerate(cols):
			for idx in range(len(rows)):
				if len(c) == 1 or len( { x[idx] for x in c } ) == 1:
					forced_color = list(c)[0][idx]
					next_rows = set()
					for r in rows[idx]:
						if r[jdx] == forced_color:
							next_rows.add(r)
					if len(next_rows) == 0:
						return (None,None)
					rows[idx] = next_rows
	return (rows,cols)		

# Solve a board for a lists of candidate rows and columns
found = 0
def solve(rows,cols):
	global found
	if 0 in { len(x) for x in rows } or 0 in { len(x) for x in cols }:
		return
	if all( len(x) == 1 for x in rows ):
		board = ''.join([list(x)[0] for x in rows])
		if board.count('B') == needed_black_squares and neighbor_check(board):
			pretty_print(board)
			found += 1
		return
	elif all( len(x) == 1 for x in cols ):
		board = ''
		for _ in range(dims[1]):
			board += ''.join([list(x)[0][_] for x in cols])
		if board.count('B') == needed_black_squares and neighbor_check(board):
			pretty_print(board)
			found += 1
		return		 
	else:
		for row_idx,row_set in enumerate(rows):
			if len(row_set) > 1:
				for row in row_set:
					next_rows = [ x for x in rows ]
					next_cols = [ x for x in cols ]
					next_rows[row_idx] = { row }
					next_rows,next_cols = do_set_elim(next_rows,next_cols)
					if next_rows != None and next_cols != None:
						solve(next_rows,next_cols)
				return # catch other longer groups down stream
					

# Begin with possible rows that follow Rule #1
pool = gen_all_valid_rows(dims[0])

# Using known colors in the input puzzle, filter impossible solution rows
candidate_rows = [] # candidates stores a set of rows that may still be valid
candidate_cols = []
for row in puzz:
	candidate_rows.append(row_filter(row,pool))

if dims[0] != dims[1]:
	pool = gen_all_valid_rows(dims[1])
for col in transpose_puzz(puzz):
	candidate_cols.append(row_filter(col,pool))

candidate_rows,candidate_cols = do_set_elim(candidate_rows,candidate_cols)
solve(candidate_rows,candidate_cols)
print(found)

