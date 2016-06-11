import snap
from pulp import *
from pprint import pprint

UGraph = snap.GenRndGnm(snap.PUNGraph, 10, 30)
w,h=10,10
Adj = [[0 for x in range(w)] for y in range(h)]
for EI in UGraph.Edges():
	Adj[EI.GetSrcNId()][EI.GetDstNId()]=1
	Adj[EI.GetDstNId()][EI.GetSrcNId()]=1
for x in range(h):
	for y in range(w):
		print Adj[x][y],
	print

L,k=3,4

# declare your variables
cen = dict(zip([i for i in range(h)],[1 for i in range(h)]))		
cen_dict=LpVariable.dicts("cen_dicts",cen, 0, 1,LpInteger)  
res={}
for i in range(h):
	for j in range(w):
		res[(i,j)]=Adj[i][j]
res_dict=LpVariable.dicts("res_dicts",res,0,1)


# defines the problem
prob = LpProblem("problem", LpMinimize)


# defines the constraints
prob += sum(cen) <= k


# defines the objective function to minimize
prob += lpSum(cen)

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
