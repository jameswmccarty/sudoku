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
#puzz = ['GGGGG','GGGGG','GGGGG','GGGGG','GGGGG']
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


# Provided a list which contains sets of possible solution rows
#  e.g. the first set is possible rows for the first row of the puzzle
#	the second set is possible rows for the second row of the puzzle...
#  Build solution strings, checking for a final solution.
found = 0
def solve(candidates,idx=0,built=''):
	global found
	if idx == dims[1] and built.count('B') == needed_black_squares and col_check(built) and neighbor_check(built):
		found += 1
		pretty_print(built)
	elif idx < dims[1]:
		for c in candidates[idx]:
			solve(candidates,idx+1,built+c)

# Begin with possible rows that follow Rule #1
pool = gen_all_valid_rows(dims[0])

# Using known colors in the input puzzle, filter impossible solution rows
candidates = [] # candidates stores a set of rows that may still be valid
for row in puzz:
	candidates.append(row_filter(row,pool))

solve(candidates,0,'')
print(found)
