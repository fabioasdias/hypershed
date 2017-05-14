import hg
import numpy as np
import csv
from scipy.spatial import distance
import time
import json
import matplotlib.pylab as plt
import networkx as nx

def makeEdgeName(G,e,edgeNames,featNames):
    if (G.edgeLevel(e)==0):
        return(edgeNames[int(e)])
    return(', '.join(reversed([ featNames[x]+'({0:.3f}) '.format(G.edge[e]['fv'][x]) for x in (G.edge[e]['fv'].argsort()[-5:]) if (G.edge[e]['fv'][x]>0)])))

G=hg.HyperGraph()

fin=open('hg.csv','r')
fcsv=csv.reader(fin, delimiter=',', quotechar='|')

for row in fcsv:
    id=int(row[0])
    nodes=[int(x) for x in row[1].replace('[','').replace(']','').split(',')]
    fv=[float (x) for x in row[2].replace('[','').replace(']','').split(',')]
    G.add_edge(id,nodes,0)
    G.edge[id]['fv']=np.array(fv)/np.sum(np.array(fv))
fin.close()


fn=open('cast.csv','r')
ncsv=csv.reader(fn, delimiter=',', quotechar='|')
for row in ncsv:
    id=int(row[0])
    G.node[id]['name']=row[1]
fn.close()


fe=open('movie.csv','r')
edgecsv=csv.reader(fe,delimiter=',', quotechar='|')
for row in edgecsv:
    id=int(row[0])
    G.edge[id]['name']=row[1]
fe.close()


t=time.time()
G.kmeans(0,K=17)
print('kmeans time {0}'.format(time.time()-t))
G.computeScore(0)
G.saveJson(0,'kmeans.json')

t=time.time()
G.cluster(0,1)
print('hypershed time {0}'.format(time.time()-t))
G.computeScore(0,metric='cosine')
G.saveJson(0,'l0.json')#,onlyBorderNodes=True)

#G.projFeatureVectors('a.svg',0)
exit()
if (False):
    GG=G.toGraph(0)
    nodelist=GG.nodes()
    cmap=np.array([[0x1F,0x77,0xB4],
                   [0xAE,0xC7,0xE8],
                   [0xFF,0x7F,0x0E],
                   [0xFF,0xBB,0x78],
                   [0x2C,0xA0,0x2C],
                   [0x98,0xDF,0x8A],
                   [0xD6,0x27,0x28],
                   [0xFF,0x98,0x86],
                   [0x94,0x67,0xBD],
                   [0xC5,0xB0,0xD5],
                   [0x8C,0x56,0x4B],
                   [0xC4,0x9C,0x94],
                   [0xE3,0x77,0xC2],
                   [0xF7,0xB6,0xD2],
                   [0x7F,0x7F,0x7F],
                   [0xC7,0xC7,0xC7],
                   [0xBC,0xBD,0x22]])/float(0xFF)
    colors=[cmap[GG.node[n]['class']-1,:].tolist() for n in nodelist]
    
    plt.ioff()
    pos=nx.spring_layout(GG,iterations=2000,weight=1,k=0.2)
    
    
    nx.draw(GG,pos=pos,node_list=nodelist,node_color=colors)
    plt.savefig('g.svg')
    plt.show()


G.cluster(1,2)
G.saveJson(1,'l1.json',onlyBorderNodes=True)

G.cluster(2,3)
G.saveJson(2,'l2.json',onlyBorderNodes=True)

G.cluster(3,4)
G.saveJson(3,'l3.json',onlyBorderNodes=True)




exit()
featNames=dict()
ff=open('words.csv','r')
featcsv=csv.reader(ff, delimiter=',', quotechar='|')
for row in featcsv:
    id=int(row[0])
    featNames[id]=row[1]
ff.close()
