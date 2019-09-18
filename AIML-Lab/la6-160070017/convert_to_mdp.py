import sys

assert len(sys.argv) == 2 or len(sys.argv) == 3
filename = sys.argv[1]
if len(sys.argv) == 3:
	p = float(sys.argv[2])
else:
	p = 1.0

f = open(filename,"r")
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

if not ed_list:
	ed_list.append(-1)

print("numStates " + str(numStates))
print("numActions " + str(4))
print("start " + str(st))
print("end " + " ".join(str(x) for x in ed_list))

num_rows = len(grid_matrix)
num_cols = len(grid_matrix[0])
flat_grad_matrix = [x for y in grid_matrix for x in y]

for i in range(len(grid_matrix)):
	for j in range(len(grid_matrix[i])):
		curr_state = (i * num_cols) + j
		if curr_state in ed_list:
			continue
		#North
		if i == 0:
			nvalid = False
		else:
			next_state = curr_state - num_cols
			if flat_grad_matrix[next_state] == 1:
				nvalid = False
			else:
				nvalid = True
		#East
		if j == (num_cols - 1):
			evalid = False
		else:
			next_state = curr_state + 1
			if flat_grad_matrix[next_state] == 1:
				evalid = False
			else:
				evalid = True
		#South
		if i == (num_rows - 1):
			svalid = False
		else:
			next_state = curr_state + num_cols
			if flat_grad_matrix[next_state] == 1:
				svalid = False
			else:
				svalid = True

		#West
		if j == 0:
			wvalid = False
		else:
			next_state = curr_state - 1
			if flat_grad_matrix[next_state] == 1:
				wvalid = False
			else:
				wvalid = True

		num_valid = 0

		if nvalid:
			num_valid += 1
		if evalid:
			num_valid += 1
		if svalid:
			num_valid += 1
		if wvalid:
			num_valid += 1

		next_north = curr_state - num_cols
		next_east = curr_state + 1
		next_south = curr_state + num_cols
		next_west = curr_state - 1

		if nvalid:
			if next_north in ed_list:
				rnorth = 1
			else:
				rnorth = 0
			print("transition " + str(curr_state) + " " + str(0) + " " + str(next_north) + " " + str(rnorth) + " " + str(p + (1-p)/num_valid))
			if p != 1.0:
				if evalid:
					print("transition " + str(curr_state) + " " + str(0) + " " + str(next_east) + " " + str(rnorth) + " " + str((1-p)/num_valid))
				if svalid:
					print("transition " + str(curr_state) + " " + str(0) + " " + str(next_south) + " " + str(rnorth) + " " + str((1-p)/num_valid))
				if wvalid:
					print("transition " + str(curr_state) + " " + str(0) + " " + str(next_west) + " " + str(rnorth) + " " + str((1-p)/num_valid))
		else:
			print("transition " + str(curr_state) + " " + str(0) + " " + str(curr_state) + " " + str(0) + " " + str(1.0))

		if evalid:
			if next_east in ed_list:
				reast = 1
			else:
				reast = 0
			print("transition " + str(curr_state) + " " + str(1) + " " + str(next_east) + " " + str(reast) + " " + str(p + (1-p)/num_valid))
			if p != 1.0:
				if nvalid:
					print("transition " + str(curr_state) + " " + str(1) + " " + str(next_north) + " " + str(reast) + " " + str((1-p)/num_valid))
				if svalid:
					print("transition " + str(curr_state) + " " + str(1) + " " + str(next_south) + " " + str(reast) + " " + str((1-p)/num_valid))
				if wvalid:
					print("transition " + str(curr_state) + " " + str(1) + " " + str(next_west) + " " + str(reast) + " " + str((1-p)/num_valid))
		else:
			print("transition " + str(curr_state) + " " + str(1) + " " + str(curr_state) + " " + str(0) + " " + str(1.0))


		if svalid:
			if next_south in ed_list:
				rsouth = 1
			else:
				rsouth = 0
			print("transition " + str(curr_state) + " " + str(2) + " " + str(next_south) + " " + str(rsouth) + " " + str(p + (1-p)/num_valid))
			if p != 1.0:
				if nvalid:
					print("transition " + str(curr_state) + " " + str(2) + " " + str(next_north) + " " + str(rsouth) + " " + str((1-p)/num_valid))
				if evalid:
					print("transition " + str(curr_state) + " " + str(2) + " " + str(next_east) + " " + str(rsouth) + " " + str((1-p)/num_valid))
				if wvalid:
					print("transition " + str(curr_state) + " " + str(2) + " " + str(next_west) + " " + str(rsouth) + " " + str((1-p)/num_valid))
		else:
			print("transition " + str(curr_state) + " " + str(2) + " " + str(curr_state) + " " + str(0) + " " + str(1.0))


		if wvalid:
			if next_west in ed_list:
				rwest = 1
			else:
				rwest = 0
			print("transition " + str(curr_state) + " " + str(3) + " " + str(next_west) + " " + str(rwest) + " " + str(p + (1-p)/num_valid))
			if p != 1.0:
				if nvalid:
					print("transition " + str(curr_state) + " " + str(3) + " " + str(next_north) + " " + str(rwest) + " " + str((1-p)/num_valid))
				if evalid:
					print("transition " + str(curr_state) + " " + str(3) + " " + str(next_east) + " " + str(rwest) + " " + str((1-p)/num_valid))
				if svalid:
					print("transition " + str(curr_state) + " " + str(3) + " " + str(next_south) + " " + str(rwest) + " " + str((1-p)/num_valid))
		else:
			print("transition " + str(curr_state) + " " + str(3) + " " + str(curr_state) + " " + str(0) + " " + str(1.0))

print("discount " + " " + str(0.9))
