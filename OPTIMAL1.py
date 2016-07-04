import snap
from pulp import *
from unitSquare import UnitSquareGraph
from random import randint, uniform
from LocalSearchAlgorithm.ls import main as localSearch

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

def integerProgram(N,p,W):
	# adj = randomGraph(N)
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
	list_var=prob.variables()
	list_cen=list_var[(len(list_var)-N):]
	count=0
	for v in list_cen:
	    if(v.varValue==1.0):
	    	count+= 1
	result = '{}\t{}\t{}\t{}'.format(N,edges, LpStatus[prob.status], count)
	return result, adj

def main():
	header = '\t'.join(['Nodes','Edges','Status','K','P','Local Search'])
	print header
	p = 1
	RAND_GRAPH_COUNT = 10
	P_LIMIT = 1 << 10
	NODE_LIMIT = 80
	W_LOW, W_HIGH = 0.2, 0.4
	res = [header]
	try:
		while p <= P_LIMIT:
			for _ in xrange(RAND_GRAPH_COUNT):
				N = randint(20,NODE_LIMIT)
				W = uniform(W_LOW, W_HIGH)
				opt, adj = integerProgram(N,p,W)
				ls = localSearch(N,adj,int(opt.split('\t')[-1]),N/10)
				result = opt + '\t' + str(p) + '\t' + ls
				print result
				res.append(result)
			p <<= 1
	except KeyboardInterrupt:
		raise
	with open('results','w') as f:
		f.write('\n'.join(res))

if __name__ == '__main__':
	main()