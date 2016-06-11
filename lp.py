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
L,k=3,4

# declare your variables
cen = dict(zip([i for i in range(N)],[1 for i in range(N)]))		
cen_dict = LpVariable.dicts("cen",cen, 0, 1,LpInteger)

res = {}
for i in range(N):
	for j in range(N):
		res[(i,j)] = adj[i][j]
res_dict = LpVariable.dicts("res",res,0,1)

# defines the problem
prob = LpProblem("problem", LpMinimize)

# defines the objective function to minimize
prob += lpSum([cen_dict[i] for i in range(10)])

# solve the problem
status = prob.solve(GLPK(msg=0))
LpStatus[status]
print "Centres:-"
# print the results x1 = 20, x2 = 60
print cen_dict
print "Result:-"
for x in range(h):
	for y in range(w):
		print res_dict[x,y],
	print 
