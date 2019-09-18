import sys

assert len(sys.argv) == 2
filename = sys.argv[1]

f = open(filename,"r")

ed_list = []
for line in f:
	line = line.rstrip()
	line = line.split(" ")
	if line[0] == "numStates":
		S = int(line[1])
		trans = [{} for i in range(S)]
	elif line[0] == "numActions":
		A = int(line[1])
	elif line[0] == "start":
		st = int(line[1])
	elif line[0] == "end":
		for j in range(len(line[1:])):
			ed_list.append(int(line[1+j]))
	elif line[0] == "transition":
		s1 = int(line[1])
		ac = int(line[2])
		s2 = int(line[3])
		r = float(line[4])
		p = float(line[5])
		if ac in trans[s1]:
			trans[s1][ac].append((s2, r, p))
		else:
			trans[s1][ac] = [(s2, r, p)]
	elif line[0] == "discount":
		gamma = float(line[2])
	else:
		print("Not matched in file")

#Algorithm begins

V = [0.0  for i in range(S)]
t = 0
while True:
	V_new = []
	actions = []
	for i in range(S):
		if i in ed_list:
			V_new.append(0.0)
			actions.append(-1)
			continue
		local_ac_v = []
		local_ac = []
		for ac in trans[i]:
			num_possible = len(trans[i][ac])
			total = 0
			for j in range(num_possible):
				next_tuple = trans[i][ac][j]
				total += next_tuple[2] * (next_tuple[1] + (gamma * V[next_tuple[0]]))
			local_ac_v.append(total)
			local_ac.append(ac)
		max_index = local_ac_v.index(max(local_ac_v))
		V_new.append(local_ac_v[max_index])
		actions.append(local_ac[max_index])
	t += 1
	converged = True
	for i in range(S):
		if abs(V_new[i] - V[i]) > 10e-16:
			converged = False
	V = V_new
	if converged:
		break

for i in range(S):
	print(str(V[i]) + " " + str(actions[i]))
print("iterations " + str(t))
f.close()