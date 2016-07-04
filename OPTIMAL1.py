import snap
from pulp import *
from unitSquare import UnitSquareGraph

def randomGraph(n):
	edges=input("No. of edges:")
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
	return adj

N = input("No. of vertices (n<4039):")
# adj = randomGraph(N)
p = 3
W = 0.5
adj = UnitSquareGraph(N,p,W).adj
edges = (sum([val for key, val in adj.iteritems()]) - N)/2
L = N/10

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
list_var=prob.variables()
list_cen=list_var[(len(list_var)-N):]
count=0
for v in list_cen:
    if(v.varValue==1.0):
    	count+= 1
print N,edges,count
