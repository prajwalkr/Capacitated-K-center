import networkx as nx
import snap
from random import shuffle
from collections import defaultdict, namedtuple
from graphgen import Graph

#Obtaining a random set S of initial k centers
def getS(G,k):
	nodes = G.nodes()
	shuffle(nodes)
	return nodes[:k]

#making FG a directed flowgraph to give as input to max flow functions ( s-->V-->S-->t )
def getFlowGraph(G, S, L):
	FG = nx.DiGraph()
	N = len(G.nodes())
	#for common nodes in V and S make separate keys for S
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

#Obtaining the set Vmax with one swap from S to get the max flow value set
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

#changing S and Vmax by one swaps so as to achieve the max flow possible after each obtained S
def doOneSwaps(G, S, L):
	Vmax = getVmax(G, S, L)
	while nx.maximum_flow_value(getFlowGraph(G, Vmax, L), 's', 't') > nx.maximum_flow_value(getFlowGraph(G, S, L), 's', 't'):
		S = Vmax
		Vmax = getVmax(G, S, L)
	return S

k, L, p = 5, 3, 0.3
N = k*L
starSpec = namedtuple('specs', 'struct k l p')
specs = starSpec('stars', k, L, p)
graph = Graph(specs)
G = graph.nxGraph
S = getS(G,k)
S = doOneSwaps(G, S, L)
H = defaultdict(list)
#max flow value cannot be greater than the number of nodes in the graph or set V
if nx.maximum_flow_value(getFlowGraph(G, S, L), 's', 't') == N:
	_,flows = nx.maximum_flow(getFlowGraph(G, S, L), 's', 't')
	edges = set(G.edges())
        #if a flow exists along a particular path assigning v to that vertex in S
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
