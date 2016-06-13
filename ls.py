import networkx as nx
import snap
from random import shuffle
from collections import defaultdict

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

def getGraph(N,adj):
	G = nx.Graph()
	G.add_nodes_from([x for x in xrange(N)])
	for i in xrange(N):
		for j in xrange(i,N):
			if adj[(i,j)]:
				G.add_edge(i,j)
	return G

def getS(G,k):
	nodes = G.nodes()
	shuffle(nodes)
	return nodes[:k]

def getFlowGraph(G, S, L):
	FG = nx.DiGraph()
	N = len(G.nodes())
	for x in G.nodes():
		if x in S:
			FG.add_node(x + N)
		else:
			FG.add_node(x)

	FG.add_nodes_from(['s','t'])
	edges = set(G.edges())
	for s in S:
		for v in G.nodes():
			if (min(s,v),max(s,v)) in edges:
				FG.add_edge(v, s + N, capacity=1)
	for v in G.nodes():
		FG.add_edge('s',v,capacity=1)
	for s in S:
		FG.add_edge(s + N,'t',capacity=L)
	return FG

def getVmax(G, S, L):
	V = G.nodes()
	# flow[i][j] = max-flow in (S, V) when S[i] is swapped with V[j]
	flow = [[None for _ in xrange(len(V))] for _ in xrange(len(S))]
	setS = set(S)
	for i in xrange(len(S)):
		for j in xrange(len(V)):
			if V[j] not in setS:
				temp = S[i]
				S[i] = V[j]
				flow_graph = getFlowGraph(G, S, L)
				flow[i][j] = nx.maximum_flow_value(flow_graph, 's', 't')
				S[i] = temp

	max_value = 0
	swap_pair = None
	for i in xrange(len(S)):
		for j in xrange(len(V)):
			if max_value < flow[i][j]:
				swap_pair = (i,j)
				max_value = flow[i][j]
	i,j = swap_pair
	S[i] = V[j]
	return S

def doOneSwaps(G, S, L):
	Vmax = getVmax(G, S, L)
	while nx.maximum_flow_value(getFlowGraph(G, Vmax, L), 's', 't') > nx.maximum_flow_value(getFlowGraph(G, S, L), 's', 't'):
		S = Vmax
		Vmax = getVmax(G, S, L)
	return S

N, M = 10,30
adj = randomGraph(N,M)
k, L = 5,3
G = getGraph(N,adj)
S = getS(G,k)
S = doOneSwaps(G, S, L)
H = defaultdict(list)
if nx.maximum_flow_value(getFlowGraph(G, S, L), 's', 't') == N:
	_,flows = nx.maximum_flow(getFlowGraph(G, S, L), 's', 't')
	edges = set(G.edges())

	for v in G.nodes():
		for s in S:
			if (min(v,s),max(v,s)) in edges:
				unitflow = False
				try:
					if flows[max(v,s + N)][min(v,s + N)] == 1:
						unitflow = True
				except KeyError:
					try:
						if flows[min(v,s + N)][max(v,s + N)] == 1:
							unitflow = True
					except KeyError:
						pass
				if unitflow:
					H[s].append(v)
else:
	print "Failed!"
print S
print H