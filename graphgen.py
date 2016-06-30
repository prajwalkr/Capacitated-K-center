import snap
import random
import networkx as nx
from collections import namedtuple

class Graph(object):
	def __init__(self, specs):
		self.k = specs.k
		self.l = specs.l

		if specs.struct == 'stars':
			self.N = self.k*self.l
			self.p = specs.p	# supplementary edge probability
			self.starGraph()

		elif specs.struct == 'random':
			self.N = specs.N 
			self.edges = specs.M
			self.randomGraph()

		else:
			raise ValueError('Invalid specifications!')

		self.nxGraph = self.NXify()

	def initAdj(self):
		self.adj = dict()
		for x in range(self.N):
			for y in range(self.N):
				self.adj[(x,y)] = 0
		for i in xrange(self.N):
			self.adj[(i,i)] = 1

	def randomGraph(self):
		UGraph = snap.GenRndGnm(snap.PUNGraph, self.N, self.edges)
		self.initAdj()

		for EI in UGraph.Edges():
			self.adj[(EI.GetSrcNId(),EI.GetDstNId())] = 1
			self.adj[(EI.GetDstNId(), EI.GetSrcNId())] = 1

	def starGraph(self):
		self.initAdj()
		non_centers = set([x for x in xrange(self.N)])
		star_centers = random.sample(list(non_centers), self.k)
		for x in star_centers: non_centers.remove(x)
		non_centers = list(non_centers)
		random.shuffle(non_centers)
		star_clients = [non_centers[i:i + self.l - 1] for i in xrange(0, len(non_centers), self.l - 1)]

		for center, clients in zip(star_centers, star_clients):
			for client in clients:
				self.adj[(center,client)] = self.adj[(client, center)] = 1

		for x in range(self.N):
			for y in range(x + 1,self.N):
				if self.adj[(x,y)] != 1:
					self.adj[(x,y)] = int(random.random() < self.p)
					self.adj[(y,x)] = int(random.random() < self.p)


	#Storing the random graph in G
	def NXify(self):
		G = nx.Graph()
		G.add_nodes_from([x for x in xrange(self.N)])
		for i in xrange(self.N):
			for j in xrange(i,self.N):
				if self.adj[(i,j)]:
					G.add_edge(i,j)
		return G
