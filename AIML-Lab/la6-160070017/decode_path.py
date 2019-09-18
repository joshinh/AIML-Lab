import sys
import numpy as np
import random 

assert len(sys.argv) == 3 or len(sys.argv) == 4
gridfile = sys.argv[1]
valuefile = sys.argv[2]
if len(sys.argv) == 4:
	p = float(sys.argv[3])
else:
	p = 1.0

f = open(gridfile,"r")
grid_matrix = []
numStates = 0
ed_list = []
for line in f:
	line = line.rstrip()
	line = line.split(" ")
	grid_matrix.append([])
	for i in range(len(line)):
		curr = int(line[i])
		grid_matrix[-1].append(int(line[i]))
		if curr == 2:
			st = numStates
		if curr == 3:
			ed_list.append(numStates)
		numStates += 1

f.close()

num_rows = len(grid_matrix)
num_cols = len(grid_matrix[0])
flat_grad_matrix = [x for y in grid_matrix for x in y]

f = open(valuefile,"r")
value_list = []
action_list = []

for line in f:
	line = line.rstrip()
	line = line.split(" ")
	if line[0] == "iterations":
		continue
	value_list.append(float(line[0]))
	action_list.append(int(line[1]))

curr_state = st
moves = []
t = 0
while True:
	if curr_state in ed_list:
		break

	next_north = curr_state - num_cols
	next_east = curr_state + 1
	next_south = curr_state + num_cols
	next_west = curr_state - 1
	valid_moves = []

	if next_north < 0:
		nvalid = False
	elif flat_grad_matrix[next_north] == 1:
		nvalid = False
	else:
		nvalid = True
		valid_moves.append(0)

	if ((curr_state + 1) % num_cols) == 0:
		evalid = False
	elif flat_grad_matrix[next_east] == 1:
		evalid = False
	else:
		evalid = True
		valid_moves.append(1)

	if next_south > numStates:
		svalid = False
	elif flat_grad_matrix[next_south] == 1:
		svalid = False
	else:
		svalid = True	
		valid_moves.append(2)

	if curr_state % num_cols == 0:
		wvalid = False
	elif flat_grad_matrix[next_west] == 1:
		wvalid = False
	else:
		wvalid = True
		valid_moves.append(3)

	if action_list[curr_state] == 0:
		if nvalid:
			#Generate bernoulli p
			p_rand = np.random.binomial(1,p)
			if p_rand == 1:
				moves.append("N")
				curr_state = next_north
			else:
				index = random.sample(range(len(valid_moves)), 1)[0]
				if valid_moves[index] == 0:
					moves.append("N")
					curr_state = next_north
				elif valid_moves[index] == 1:
					moves.append("E")
					curr_state = next_east
				elif valid_moves[index] == 2:
					moves.append("S")
					curr_state = next_south
				else:
					moves.append("W")
					curr_state = next_west
		else:
			#Stay at same place with prob = 1
			moves.append("N")
		
	elif action_list[curr_state] == 1:
		if evalid:
			#Generate bernoulli p
			p_rand = np.random.binomial(1,p)
			if p_rand == 1:
				moves.append("E")
				curr_state = next_east
			else:
				index = random.sample(range(len(valid_moves)), 1)[0]
				if valid_moves[index] == 0:
					moves.append("N")
					curr_state = next_north
				elif valid_moves[index] == 1:
					moves.append("E")
					curr_state = next_east
				elif valid_moves[index] == 2:
					moves.append("S")
					curr_state = next_south
				else:
					moves.append("W")
					curr_state = next_west
		else:
			#Stay at same place with prob = 1
			moves.append("E")
	elif action_list[curr_state] == 2:
		if svalid:
			#Generate bernoulli p
			p_rand = np.random.binomial(1,p)
			if p_rand == 1:
				moves.append("S")
				curr_state = next_south
			else:
				index = random.sample(range(len(valid_moves)), 1)[0]
				if valid_moves[index] == 0:
					moves.append("N")
					curr_state = next_north
				elif valid_moves[index] == 1:
					moves.append("E")
					curr_state = next_east
				elif valid_moves[index] == 2:
					moves.append("S")
					curr_state = next_south
				else:
					moves.append("W")
					curr_state = next_west
		else:
			#Stay at same place with prob = 1
			moves.append("S")
	else:
		if wvalid:
			#Generate bernoulli p
			p_rand = np.random.binomial(1,p)
			if p_rand == 1:
				moves.append("W")
				curr_state = next_west
			else:
				index = random.sample(range(len(valid_moves)), 1)[0]
				if valid_moves[index] == 0:
					moves.append("N")
					curr_state = next_north
				elif valid_moves[index] == 1:
					moves.append("E")
					curr_state = next_east
				elif valid_moves[index] == 2:
					moves.append("S")
					curr_state = next_south
				else:
					moves.append("W")
					curr_state = next_west
		else:
			#Stay at same place with prob = 1
			moves.append("W")

print(" ".join(moves))