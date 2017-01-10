import hg
import numpy as np
from scipy.spatial import distance
import csv

G=hg.HyperGraph()

edges=[['a','b','c'],['b'],['c','d','e'],['d','e'],['b','d'],['a','c']]
#fvs=[0,1,0,1,0.5]
fvs=[[3,3],
     [8,8],
     [-5,5],
     [3,-3],
     [7,-7],
     [-3,3]]

for ii in range(len(edges)):
    i=ii+1
    G.add_edge(i,edges[ii],0)
    G.edge[i]['name']=str(i)
    G.edge[i]['fv']=fvs[ii]
    
for n in G.nodes():
    G.node[n]['name']=str(n)

#for e1 in G.edges(0):
#    for e2 in G.edges(0):
#        if (e1!=e2):
#            print(e1,e2,G._wdist(e1,e2))

G.cluster(0,1)
G.saveJson(0,'l0.json')


