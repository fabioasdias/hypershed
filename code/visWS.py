import hg
import numpy as np
import csv
from scipy.spatial import distance
import time
import json
from genlib import makeEdgeName, saveJson
        
G=hg.HyperGraph()

fin=open('hgVis.csv','r')
fcsv=csv.reader(fin, delimiter=',', quotechar='|')



for row in fcsv:
    id=int(row[0])
    nodes=[int(x) for x in row[1].split(',')]
    fv=[float (x) for x in row[2].split(',')]
    G.add_edge(id,nodes,0)
    G.edge[id]['fv']=np.array(fv)
    s=np.sum(np.array(fv))
    if (s>0):
        G.edge[id]['fv']=G.edge[id]['fv']/s
fin.close()


nodeInfo=dict()
fn=open('researchers.csv','r')
ncsv=csv.reader(fn, delimiter=',', quotechar='|')
for row in ncsv:
    nodeInfo[int(row[0])]=row[1]
fn.close()

featNames=dict()
ff=open('bigrams.csv','r')
featcsv=csv.reader(ff, delimiter=',', quotechar='|')
for row in featcsv:
    featNames[int(row[0])]=row[1]
ff.close()

edgeNames=dict()
fe=open('papers.csv','r')
edgecsv=csv.reader(fe,delimiter=',', quotechar='|')
for row in edgecsv:
    edgeNames[int(row[0])]=row[1]
fe.close()

    
#saveJson(G,0,'l0.json',nodeInfo,edgeNames,featNames)

t=time.time()

G.cluster(0,1)
saveJson(G,1,'l1.json',nodeInfo,edgeNames,featNames)
print(time.time()-t)


if (False):
    clelem=dict()
    
    for e in G.edges(0):
        p=G._psi[e]
        if (p not in clelem):
            clelem[p]=[]
        clelem[p].append(edgeNames[int(e)])
            
    for p in clelem:
        f=open('cl_{0}.txt'.format(p),'w')
        f.write('\n'.join(clelem[p]))
        f.close()

        
if True:
    for e in G.edges(1):
        f=open('au_{0}.txt'.format(e),'w')
        f.write(makeEdgeName(G,e,edgeNames,featNames)+'\n')

        for n in G.nodesOfEdge(e):
            if (len(list(set([G._psi[e] for e in G.edgesOfNode(n,0)])))==1):
                f.write(nodeInfo[n]+'\n')            

        f.close()
            
#exit()















G.cluster(1,2)
saveJson(G,2,'l2.json',nodeInfo,edgeNames,featNames)
print(time.time()-t)

G.cluster(2,3)
saveJson(G,3,'l3.json',nodeInfo,edgeNames,featNames)
print(time.time()-t)

G.cluster(3,4)
saveJson(G,4,'l4.json',nodeInfo,edgeNames,featNames)
print(time.time()-t)

G.cluster(4,5)
saveJson(G,5,'l5.json',nodeInfo,edgeNames,featNames)
print(time.time()-t)





exit()
fout=open('resVis.csv','w')
outcsv=csv.writer(fout)

for k in sorted(psi.keys()):
    outcsv.writerow([k,psi[k]])

fout.close()
    
