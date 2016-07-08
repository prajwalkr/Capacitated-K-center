from random import random
import networkx as nx

class UnitSquareGraph(object):
	def __init__(self, N, P, W):
		self.N = N
		self.P = P
		self.W = W
		points = [[random(),random()] for _ in xrange(self.N)]
		self.dist = [[None for _ in xrange(self.N)] for _ in xrange(self.N)
		for i in xrange(self.N):
			for j in xrange(self.N):
				self.dist[i][j] = self.dist[j][i] = self.lpNorm(points[i], points[j], self.P)
		self.adj = self.getAdj()
		self.nxGraph = self.NXify()

	def lpNorm(self,A,B,p):
		x1, y1 = A
		x2, y2 = B
		return ((abs(x2 - x1)**p + abs(y2 - y1)**p)**(1.00/p))

	def getAdj(self):
		adj = dict()
		for i in xrange(self.N):
			for j in xrange(self.N):
				adj[(i,j)] = adj[(j,i)] = self.dist[i][j] <= self.W

		return adj

	def NXify(self):
		G = nx.Graph()
		G.add_nodes_from([x for x in xrange(self.N)])
		for i in xrange(self.N):
			for j in xrange(i,self.N):
				if self.adj[(i,j)]:
					G.add_edge(i,j)
		return G
