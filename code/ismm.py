import hg
import networkx as nx
import os.path
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt') 


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english',strip_accents='unicode',max_df=0.75,min_df=0.4)

equivalentFile='equivalent.list'

import matplotlib.pylab as plt

def readEquivalent(fname):
    equivalent=dict()
    f=open(fname,'r')
    for line in f:
        vals=[x.strip() for x in line.split('\t')]
        equivalent[vals[0]]=vals[1]
    f.close()
    return(equivalent)

def writeEquivalent(equivalent,fname):
    with open(fname,'w') as f:
        for k in equivalent.keys():
            f.write('{0}\t{1}\n'.format(k,equivalent[k]))
        

def authorSimilarity(a1,a2):
    if (len(a1)<len(a2)):
        s=a1
        b=a2
    else:
        s=a2
        b=a1
    c=0
    for i in range(len(s)):
        if (s[i] in b):
            c+=1
    ln1=s.split(' ')[-1]
    ln2=b.split(' ')[-1]
    if (len(ln1)<len(ln2)):
        lnS=ln1
        lnB=ln2
    else:
        lnS=ln2
        lnB=ln1
        
    cln=0
    for i in range(len(lnS)):
        if (lnS[i] in lnB):
            cln+=1
    
    return((float(c)/len(s))*(float(cln)/len(lnS)))
        


with open('ismm.tsv','r') as f:
    data=[x.split('\t') for x in f.read().split('\n')]

headers=data[0]
data=data[1:]

authorPaper=[x[1].replace(' and ',', ').strip().split(',') for x in data]

papersByAuthor=dict()

authors=[]
for i in range(len(authorPaper)):
    for author in authorPaper[i]:
        val=''.join([x for x in author if (x.isalpha() or x==' ' or x==',' or x=='-')]).strip()
        if (val==''):
            continue
        authors.append(val)
        if (val not in papersByAuthor):
            papersByAuthor[val]=[]
        papersByAuthor[val].append(i)

if (os.path.exists(equivalentFile)):
    with open(equivalentFile, 'rb') as f:
        equivalent = readEquivalent(equivalentFile)
else:
    equivalent=dict()


    
done=False
while not done:
    authors=sorted(set(authors))
    changed=False
    for a in authors:
        if (a in equivalent):
            changed=True
            if equivalent[a] not in authors:
                authors.append(equivalent[a])
            if equivalent[a] not in papersByAuthor:
                papersByAuthor[equivalent[a]]=[]
            if (a in papersByAuthor):
                papersByAuthor[equivalent[a]].extend(papersByAuthor[a])
                del(papersByAuthor[a])
            if (a in authors):
                authors.remove(a)

    if (changed==True):
        continue
    else:
        done=False
        key=input('done?')
        if (key=='s' or key=='S' or key==''):
            break

    
    G=nx.Graph()
    G.add_nodes_from(authors)    
    for a1 in authors:
        for a2 in authors:
            if (a1==a2):
                continue
            sim=authorSimilarity(a1,a2)
            if (sim>0.8):
                G.add_edge(a1,a2,weight=sim)

    edges=sorted(G.edges(data=True),key=lambda x: x[-1]['weight'],reverse=True)

    for e in edges:
        print('1 - {0}\n2 - {1}\n'.format(e[0],e[1]))
        key=input()
        if (key!=''):
            changed=True
        if (key=='-'):
            done=True
            break

        if (key=='1'):
            equivalent[e[1]]=e[0]
            authors.remove(e[1])
            papersByAuthor[e[0]].extend(papersByAuthor[e[1]])
            del(papersByAuthor[e[1]])
        if (key=='2'):
            equivalent[e[0]]=e[1]
            authors.remove(e[0])
            papersByAuthor[e[1]].extend(papersByAuthor[e[0]])
            del(papersByAuthor[e[0]])


writeEquivalent(equivalent,equivalentFile)

p2a=dict()
for author in papersByAuthor:
    for paper in papersByAuthor[author]:
        if paper not in p2a:
            p2a[paper]=[]
        p2a[paper].append(author)

G=hg.HyperGraph(mode='text')

corpus=[]
for i in range(len(data)):
    corpus.append(data[i][3])
tfidf = vectorizer.fit_transform(corpus)
    

for i in range(len(data)):
#    if (data[i][2].strip()!=''):
    G.add_edge(i,p2a[i],0)
    G.edge[i]['name']=data[i][0]
    G.edge[i]['keywords']=data[i][2]
    G.edge[i]['fv']=tfidf[i,:]
    corpus.append(data[i][3])
              
for n in G.nodes():
    G.node[n]['name']=n

# to save level X, we need the labels of level X+1, otherwise group=1
print('authors: {0}'.format(len(G.nodes())))
G.saveJson(0,'lorig.json', onlyBorderNodes=False, allEdges=True)

for X in range(6):
    G.cluster(X,X+1)
    print('\n\nLevel {1}  n edges after clustering {0}'.format(len(G.edges(X)),X))
    G.saveJson(X,'l{0}.json'.format(X), onlyBorderNodes=False, allEdges=False)
    
