"""
Rules

1. Fill in the cells under the following rules.
2. You cannot fill in cells containing numbers.
3. A number tells the number of continuous white cells. Each area of white cells contains only one number in it and they are separated by black cells.
4. The black cells are linked to be a continuous wall.
5. Black cells cannot be linked to be 2×2 square or larger.

Solution is currently too slow for the 10x10 examples.

"""

# A puzzle is its dimensions (x,y) and islands
# islands shown as (x,y,size) with a zero index

dims = (5,5)
islands = [ (4,0,1), (0,1,1), (0,3,5), (4,3,2) ]

dims = (7,7)
islands = [ (6,1,3), (4,1,3), (3,2,3), (1,3,3), (1,5,5) ]

dims = (10,10)
islands = [ (7,0,1), (1,1,2), (5,1,3), (8,1,8), (6,4,4), (4,5,4), (3,6,1), (5,7,3), (2,7,5), (3,8,2), (6,9,1), (2,9,3) ]

dims = (10,10)
islands = [ (7,0,5), (6,1,8), (7,2,6), (2,2,2), (0,2,2), (1,3,5), (8,6,1), (9,7,4), (7,7,3), (2,7,2), (3,8,2), (2,9,2), (6,9,1) ]

dims = (7,7)
islands = [ (4,0,3), (2,1,2), (3,2,3), (6,3,1), (3,4,4), (4,5,2), (2,6,2) ]


# geoms holds templates of all islands shapes of size 'N'
# (with no holes) as a set of tuples of offset points (x,y)
geoms = dict()

# allow finding size of an island at a point (x,y)
island_size_at_point = dict()
for x,y,s in islands:
	island_size_at_point[(x,y)] = s

# The number of black squares needed is the puzzle
# area minus the size of the islands
blacks_target_size = dims[0]*dims[1] - sum( [ s for x,y,s in islands ] )
whites_target_size = sum( [ s for x,y,s in islands ] )
cover_set = { (x,y) for x in range(dims[0]) for y in range(dims[1]) }

# islands cannot overlap with a known black square, and will not overlap with another island
# compute squares that must be black 
# squares that must be black are surrounding islands of size 1
# or are at adjacent corners of adjacent islands
blacks = set()
for x in range(dims[0]):
	for y in range(dims[1]):
		if (x,y) not in island_size_at_point:
			adj_count = 0
			for dx,dy in ((-1,0),(1,0),(0,1),(0,-1)):
				if (x+dx,y+dy) in island_size_at_point and island_size_at_point[(x+dx,y+dy)] == 1:
					blacks.add((x,y))
				elif (x+dx,y+dy) in island_size_at_point:
					adj_count += 1
			if adj_count > 1:
				blacks.add((x,y))

# print out the solution board
# just provide the cells that are white
def pretty_print(whites):
	black_tile = '#'
	for y in range(dims[1]):
		for x in range(dims[0]):
			if (x,y) in island_size_at_point:
				print(island_size_at_point[(x,y)] % 10,end='')
			elif (x,y) in whites:
				print('.',end='')
			else:
				print(black_tile,end='')
		print()

# for a given list of points, determine if there is a 'hole'
# for an (x,y) location that is surrounded on 4 sides by points
# in the list, but is not in the list itself
def has_hole(points):
	xs = { p[0] for p in points }
	ys = { p[1] for p in points }
	for x in range(min(xs),max(xs)+1):
		for y in range(min(ys),max(ys)+1):
			if (x,y) not in points and all( (x+dx,y+dy) in points for dx,dy in ((-1,0),(1,0),(0,1),(0,-1)) ):
				return True
	return False

# verify the size of an island given a point (x,y)
# and the list of 'ocean' black points
def find_island_size(point, blacks):
	seen = set()
	seen.add(point)
	q = [ point ]
	while len(q) > 0:
		x,y = q.pop(0)
		for dx,dy in ((-1,0),(1,0),(0,1),(0,-1)):
			if x+dx >= 0 and x+dx < dims[0] and y+dy >= 0 and y+dy < dims[1]:
				if (x+dx,y+dy) not in seen and (x+dx,y+dy) not in blacks:
					seen.add((x+dx,y+dy))
					q.append((x+dx,y+dy))
	return len(seen)

# verify there are no 2x2 squares in a set of black points
# verify there are no black cells not connected to another cell
def verify_ocean(blacks):
	for x,y in blacks:
		if all( (x+dx,y+dy) in blacks for dx,dy in ((0,1),(1,0),(1,1)) ):
			return False
	for x,y in blacks:
		if not any( (x+dx,y+dy) in blacks for dx,dy in ((-1,0),(1,0),(0,1),(0,-1))):
			return False
	return True

# for a given size, find all offsets from a point that
# define an island of that size
def gen_offsets(size):
	global geoms
	if size in geoms or size <= 0:
		return
	if size == 1:
		geoms[1] = {((0,0),)}
		return
	if size - 1 not in geoms:
		gen_offsets(size-1)
	q = [ x for x in geoms[size-1] ]
	offsets = set()
	while len(q) > 0:
		shape = q.pop(0)
		if len(shape) == size and not has_hole(shape):
			shape = tuple(sorted(shape))
			offsets.add(shape)
		elif len(shape) < size:
			for x,y in shape:
				for dx,dy in ((-1,0),(1,0),(0,1),(0,-1)):
					if (x+dx,y+dy) not in shape:
						next_shape = [ x for x in shape ] + [ (x+dx,y+dy) ]
						q.append(next_shape)
	geoms[size] = offsets

# islands must be the size given
# an island must fit on the board
# an island must not overlap another island
# an island must not occupy the same square as a known black tile

gen_offsets(max(island_size_at_point.values()))

# apply shape offsets for each island anchor point
# but do not keep islands that would occupy a known black square
# or be off the edge of the board
mapped_islands = []
for x,y,s in islands:
	trial_islands = []
	other_islands_points = [ x for x in island_size_at_point.keys() ]
	other_islands_points.remove((x,y))
	for offset_map in geoms[s]:
		trial_island = []
		for dx,dy in offset_map:
			trial_island.append((x+dx,y+dy))
		if not any ( x < 0 or x >= dims[0] or y < 0 or y >= dims[1] for x,y in trial_island):
			if not any( p in blacks for p in trial_island):
				if not any( p in other_islands_points for p in trial_island):
					trial_islands.append(trial_island)
	mapped_islands.append(trial_islands)

# remove islands from consideration that would overlap another island
# on the map.  if there is only one option for an island shape, then
# anything that touches it must be incorrect.
mapped_size = -1
while mapped_size != sum( [ len(x) for x in mapped_islands ] ):
	mapped_size = sum( [ len(x) for x in mapped_islands ] )
	for idx,island_set_a in enumerate(mapped_islands):
		if len(island_set_a) == 1:
			for entry_a in island_set_a:
				for j in range(len(mapped_islands)):
					if idx != j:
						for entry_b in mapped_islands[j]:
							if len(set(entry_a).intersection(set(entry_b))) > 0:
								mapped_islands[j].remove(entry_b)

def build_trial_solution(mapped_islands,whites=set(),idx=0):
	if idx == len(mapped_islands):
		yield whites.copy()
	elif idx < len(mapped_islands):
		for points in mapped_islands[idx]:
			trial_whites = { point for point in whites }
			if len(trial_whites.intersection(set(points))) == 0: # island does not overlap ones picked so far
				next_map = [ x[:] for x in mapped_islands ]
				next_map[idx] = points
				for jdx in range(idx+1,len(mapped_islands)):
					for entry in next_map[jdx]:
						if len(set(entry).intersection(set(points))) > 0:
							next_map[jdx].remove(entry)
				if 0 not in { len(x) for x in next_map }:
					trial_whites = trial_whites.union(points)
					yield from build_trial_solution(next_map,trial_whites,idx+1)

mapped_islands.sort(key=lambda x: len(x),reverse=True)
#print( [ len(mapped_islands[i]) for i in range(len(mapped_islands)) ] )

for whites in build_trial_solution(mapped_islands):
	if len(whites) == whites_target_size:
		trial_blacks = cover_set - whites
		if verify_ocean(trial_blacks) and all( find_island_size(p,trial_blacks) == island_size_at_point[p] for p in island_size_at_point.keys() ):
			pretty_print(whites)

