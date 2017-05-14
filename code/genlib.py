import json

def makeEdgeName(G,e,edgeNames,featNames):
    if (G.edgeLevel(e)==0):
        return(edgeNames[int(e)])
    return(', '.join(reversed([ featNames[x]+'({0:.3f}) '.format(G.edge[e]['fv'][x]) for x in (G.edge[e]['fv'].argsort()[-5:]) if (G.edge[e]['fv'][x]>0)])))
        
def saveJson(G,level,fname,nodeInfo,edgeNames,featNames):
    res=dict()
    nId=dict()
    res['nodes']=[]
    res['links']=[]
    
    i=0
    for e in G.edges(level):
        allE=G.nodesOfEdge(e)
        for n in allE:
            if n not in nId:
                nId[n]=i
                i+=1
                res['nodes'].append({'name':nodeInfo[n],'group':1})
                
        if (len(allE)>2):
            res['nodes'].append({'name':'fake_{0}'.format(e),'group':0})
            fake=i;
            i+=1
        if (len(allE)==1):
            pass #cant draw self loops atm
        elif (len(allE)==2):
            res['links'].append({'source':nId[allE[0]],'target':nId[allE[1]],'edgeid':makeEdgeName(G,e,edgeNames,featNames)})
        else:
            for n in allE:
                res['links'].append({'source':fake,'target':nId[n],'edgeid':makeEdgeName(G,e,edgeNames,featNames)})
            
    with open(fname, 'w') as outfile:
        json.dump(res, outfile)

