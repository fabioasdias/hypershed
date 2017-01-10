from scipy.spatial import distance
from collections import deque
import numpy as np
from numpy.linalg import norm
import json
#from pyemd import emd
from scipy.signal import gaussian
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import networkx as nx


class HyperGraph:    
    def __init__(self):
        self.edge=dict()#data structures
        self.node=dict()
        self._nodesOfEdge=dict() #links
        self._edgesOfNode=dict()
        self._edgeLevel=dict() # level of edges
        self._parentEdge=dict()
        self._childrenEdges=dict()
        self._psi=dict() #edge group in the next level
        self._costMatrix=None
        self._distCache=dict() #distance cache (e1,e2)
        self._FminCache=dict() # Fminus cache (e)
        self._nId=dict() # nodes -> ids (to keep consisten across saves)


    def _fg(self,t,c):
        w=gaussian(t,t/3)
        t2=np.floor(t/2)
        w=np.concatenate((w[-(t2):],w[:t-t2]))
        w=2-np.concatenate((w[-c:],w[:-c]))
        return(w)


    def _buildCostMatrix(self,n,m):
        distance_matrix=np.zeros((n,m))
        for i in range(m):
            distance_matrix[i]=self._fg(n,i)
        return(distance_matrix)


    def edgeLevel(self,e):
        if (e in self._edgeLevel):
            return(self._edgeLevel[e])
    def edges(self,level):
        return(sorted(list([x for x in self.edge.keys() if self._edgeLevel[x]==level])))
    
    def nodes(self):
        return(sorted(list(self.node.keys())))
    
    def add_node(self,n):
        if (n not in self.node):
            self.node[n]=dict()
        if (n not in self._edgesOfNode):
            self._edgesOfNode[n]=[]
            
    def add_edge(self,id,nodes,level):        
        self._edgeLevel[id]=level
        
        if id not in self.edge:
            self.edge[id]=dict()
            
        if id not in self._nodesOfEdge:
            self._nodesOfEdge[id]=nodes
        else:
            self._nodesOfEdge[id].extend(nodes)
            
        for n in nodes:
            self.add_node(n)
            self._edgesOfNode[n].append(id)

    def edgesOfNode(self,n,level=False):
        if (n in self._edgesOfNode):
            if (level==False) and (level!=0):
                return(self._edgesOfNode[n])
            else:
                return([x for x in self._edgesOfNode[n] if (self._edgeLevel[x]==level)])
        else:
            return(None)
        
    def nodesOfEdge(self,e):
        if (e in self._nodesOfEdge):
            return(self._nodesOfEdge[e])
        else:
            return(None)
        
    def neighborsEdge(self,e,level=False):
        res=[]
        for n in self.nodesOfEdge(e):
            res.extend(self.edgesOfNode(n,level))
        res=set(res)
        res.remove(e)
        if (level!=False) or (level==0):
            res=[x for x in res if self._edgeLevel[x]==level]
        return(sorted(res))
    
    def neighborsNode(self,n,level):
        res=[]
        for e in self.edgesOfNode(n,level):
            res.extend(self.nodesOfEdge(e))
        res=set(res)
        res.remove(n)
        return(res)

    def _Fminus(self,x,level):
        if (x in self._FminCache):
            return(self._FminCache[x])
        
        neigh=self.neighborsEdge(x,level)
        minval=float('inf')
        for e in neigh:
            d=self._wdist(x,e)
            minval=min((minval,d))
        self._FminCache[x]=minval
        return(minval)

    def _kernel(self,e1,e2):
        return(np.exp(-np.power(norm(self.edge[e1]['fv']-self.edge[e2]['fv']),2)/len(self.edge[e1]['fv'])))
    
    def _wdist(self,e1,e2):
        if (e1 in self._distCache):
            if (e2 in self._distCache[e1]):
                return(self._distCache[e1][e2])
        else:
            self._distCache[e1]=dict()

        #if (self._costMatrix is None):
        #    self._costMatrix=self._buildCostMatrix(len(self.edge[e1]['fv']),len(self.edge[e2]['fv']))
        #cdist=emd(self.edge[e1]['fv'],self.edge[e2]['fv'],self._costMatrix)

        v1=np.array(self.edge[e1]['fv'],dtype=float)
        s1=np.sum(v1)
        if (s1<1E-6):
            s1=1
        v2=np.array(self.edge[e2]['fv'],dtype=float)
        s2=np.sum(v2)
        if (s2<1E-6):
            s2=1
        cdist=distance.cosine(v1/s1,v2/s2)
        self._distCache[e1][e2]=cdist
        return(cdist)
                
        #return(distance.euclidean(self.edge[e1]['fv'],self.edge[e2]['fv']))

        #
            
        #return()

        #kii=self._kernel(e1,e1)
        #kij=self._kernel(e1,e2)
        #kjj=self._kernel(e2,e2)
        #return(np.sqrt(kii-2*kij+kjj))
    
    def _stream(self,psi,x,level):
        L=[x,]
        lp=deque([x,])
        while (len(lp)>0):
            y=lp.popleft()
            breadth_first=True
            allZ=[z for z in self.neighborsEdge(y,level) if (z not in L) and self._wdist(y,z)==self._Fminus(y,level)]
            if (not allZ):
                break
            for z in allZ:
                if (not breadth_first):
                    break
                if (psi[z]>=0):
                    return([L,psi[z]])
                elif self._Fminus(z,level)<self._Fminus(y,level):
                    L.append(z)
                    lp.clear()
                    lp.append(z)
                    breadth_first=False
                else:
                    L.append(z)
                    lp.append(z)
        return (L,-1)

    
    def watershed(self,level):
        psi=dict()
        for e in self.edges(level):
            psi[e]=-1
        nb_labs=0
        for x in self.edges(level):
            if (psi[x]==-1):
                L,lab=self._stream(psi,x,level)
                if (lab==-1):
                    nb_labs+=1
                    for e in L:
                        psi[e]=nb_labs
                else:
                    for e in L:
                        psi[e]=lab                
        return(psi)

    def cluster(self,levelin,levelout):
        psi=self.watershed(levelin)
        for e in psi:
            self._psi[e]=psi[e]

            
        fv=dict()
        for e in self.edges(levelin):
            if (psi[e] not in fv):
                fv[psi[e]]=[]
            fv[psi[e]].append(self.edge[e]['fv'])

            
            
        nOfE=dict()        
        for n in self.nodes():
            cls=set([psi[e] for e in self.edgesOfNode(n,levelin)])
            if True:#(len(cls)>1): #more than one cluster around this node
                for p in cls:
                    if (p not in nOfE):
                        nOfE[p]=[]
                    nOfE[p].append(n)
            

        for e in nOfE:
            ename='{0}_{1:02d}'.format(levelout,e)
            self.add_edge(ename,nOfE[e],levelout)
            self.edge[ename]['name']=ename
            
            if (len(fv[e])<=2):
                self.edge[ename]['fv']=fv[e][0]
            else:
                #fv corresponding to the element with smallest distance to all others
                #self.edge[ename]['fv']=fv[e][np.argmin(np.sum(distance.squareform(distance.pdist(np.array(fv[e]),'cosine')),axis=0))]
                self.edge[ename]['fv']=np.sum(fv[e],0)
                s=np.sum(self.edge[ename]['fv'])
                if (s>1E-6):
                    self.edge[ename]['fv']=self.edge[ename]['fv']/s
                

    def toGraph(self,layer):
        G=nx.Graph()
        allE=self.edges(layer)
        for e1 in allE:
            for e2 in allE:
                if (e1!=e2):
                    s1=set(self.nodesOfEdge(e1))
                    s2=set(self.nodesOfEdge(e2))
                    if (len(s1&s2)>0):
                        G.add_edge(e1,e2)
                        G.node[e1]['class']=self._psi[e1]
                        G.node[e2]['class']=self._psi[e2]
                        G.node[e1]['name']=self.edge[e1]['name']
                        G.node[e2]['name']=self.edge[e2]['name']
                        G.edge[e1][e2]['weight']=self._wdist(e1,e2)
                        
        return(G)
        

    def projFeatureVectors(self,fname,layer):
        allE=self.edges(layer)
        X=np.zeros((len(allE),len(self.edge[allE[0]]['fv'])))
        colors=[]
        for i in range(len(allE)):
            e=allE[i]
            X[i,:]=self.edge[e]['fv']
            colors.append(self._psi[e])
        if (len(set(colors))==17):
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
            colors=[cmap[x-1,:].tolist() for x in colors]

            
        model = TSNE(n_components=2, random_state=0, metric='cosine', perplexity=3)
        Y=model.fit_transform(X)
        plt.ioff()
        plt.scatter(Y[:,0],Y[:,1],s=40,c=colors)
        plt.axis('equal')
        plt.savefig(fname)
        plt.show()

        
        
        
    def saveJson(self,level,fname,onlyBorderNodes=False):
        res=dict()
        res['nodes']=[]
        res['links']=[]
        nUsed=[]
        border=dict()
        i=0
        for e in self.edges(level):
            allE=self.nodesOfEdge(e)
            todo=[]
            if (onlyBorderNodes):
                for n in allE:
                    if (n not in border):
                        border[n]=len( set([self._psi[e] for e in self.edgesOfNode(n,level)]))>1
                    if (border[n]):
                        todo.append(n)
                allE=todo
                    
            for n in allE:
                if n not in self._nId:
                    self._nId[n]=i
                if n not in nUsed:
                    res['nodes'].append({'id':self._nId[n],"name":self.node[n]['name']})
                    i+=1
            if (e in self._psi):
                res['links'].append({'name':self.edge[e]['name'],'group':self._psi[e],'children':[self._nId[allE[i]] for i in range(len(allE))]})
            else:
                res['links'].append({'name':self.edge[e]['name'],'group':0,'children':[self._nId[allE[i]] for i in range(len(allE))]})
                        
        with open(fname, 'w') as outfile:
            json.dump(res, outfile)
            
            






        
