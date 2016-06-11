import snap
from pulp import *
from pprint import pprint

def randomGraph(n,edges):
	UGraph = snap.GenRndGnm(snap.PUNGraph, n, edges)
	adj = [[0 for x in range(n)] for y in range(n)]
	for EI in UGraph.Edges():
		adj[EI.GetSrcNId()][EI.GetDstNId()] = 1
		adj[EI.GetDstNId()][EI.GetSrcNId()] = 1
	'''for x in range(h):
					for y in range(w):
						print adj[x][y],
					print'''

N, M = 10, 30
adj = randomGraph(N, M)
L,k = 3,4

# declare your variables
cen = dict(zip([i for i in range(N)],[0 for i in range(N)]))		
cen = LpVariable.dicts("cen",cen, 0, 1,LpInteger)

assignments = {}
for i in range(N):
	for j in range(N):
		assignments[(i,j)] = i == j
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

# Non - negativity constraints
for i in xrange(N):
	prob += cen[i] >= 0
for i in xrange(N):
	for j in xrange(N):
		prob += assignments[(i,j)] >= 0

# solve the problem
status = prob.solve()
print LpStatus[prob.status]
for v in prob.variables():
    print(v.name, "=", v.varValue)
