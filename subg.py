import snap
Graph = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1, ' ')
snap.PrintInfo(Graph, "Facebook Data Set")
SubGraph = snap.GetRndSubGraph(Graph,10)
SubGraph.Dump()