import snap
from pulp import *

def randomGraph(n,edges):
	UGraph = snap.GenRndGnm(snap.PUNGraph, n, edges)
	adj = dict()
	for x in range(n):
		for y in range(n):
			adj[(x,y)] = 0
	for EI in UGraph.Edges():
		adj[(EI.GetSrcNId(),EI.GetDstNId())] = 1
		adj[(EI.GetDstNId(), EI.GetSrcNId())] = 1
	for i in xrange(n):
		adj[(i,i)] = 1
	for x in range(n):
		for y in range(n):
			print adj[(x,y)],
		print
	return adj

N, M = 10, 10
adj = randomGraph(N, M)
L = 3

# declare your variables
cen = dict(zip([i for i in range(N)],[0 for i in range(N)]))		
cen = LpVariable.dicts("cen",cen, 0, 1,LpInteger)

assignments = {}
for i in range(N):
	for j in range(N):
		assignments[(i,j)] = adj[(i,j)]

assignments = LpVariable.dicts("assignments",assignments,0,1)

# defines the problem
prob = LpProblem("problem", LpMinimize)

# defines the objective function to minimize : sum(y)
prob += lpSum([cen[i] for i in range(N)])

############# Constraint definitions ###################

# sum(x_ij) <= L*y[i]
for i in xrange(N):
	prob += lpSum([assignments[(i,j)] for j in xrange(N)]) <= L*cen[i]

# sum(x_ij) = 1 for all j
for j in xrange(N):
	prob += lpSum([assignments[(i,j)] for i in xrange(N)]) == 1

# y_i >= x_ij for all i,j
for i in xrange(N):
	for j in xrange(N):
		prob += assignments[(i,j)] <= cen[i]
#the assignment can be done only when the edge is present
for i in xrange(N):
	for j in xrange(N):
		prob += assignments[(i,j)] <= adj[(i,j)]

# solve the problem using GLPK
status = prob.solve(GLPK(msg=0))
print LpStatus[prob.status]
for v in prob.variables():
    print(v.name, "=", v.varValue)
