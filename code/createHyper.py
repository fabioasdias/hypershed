import csv
from scipy.sparse import lil_matrix

def bagOfWords( fileMovies, fileKeys, fileGenres, outHg, outWords ):
    movies   = {}
    keywords = {}
    genres   = {}    
    
    with open(fileMovies, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',',quotechar='|')
        for row in spamreader:
            
            directors = []
            if not row[5] == '':
                aux = row[5].split(',')
                directors = [int(r) for r in aux]
            
            gen = []
            if not row[3] == '':
                aux = row[3].split(',')
                gen = [int(r) for r in aux]
                        
            movies[int(row[0])] = {'title':row[1], 'date':row[2], 
                                   'genre':gen,
                                   'keywords':[int(r) for r in row[4].split(',')],
                                   'director':directors,
                                   'cast':[int(r) for r in row[6].split(',')],
                                   'overview':row[7],
                                   'imdb':row[8],
                                   'tmdb':int(row[9]),
                                   'budget':int(row[10])}
            
    
    with open(fileKeys, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',',quotechar='|')
        for row in spamreader:
            keywords[int(row[0])] = row[1]
    
    
    with open(fileGenres, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',',quotechar='|')
        for row in spamreader:
            genres[int(row[0])] = row[1]
    
    nKeys   = len(keywords.keys())
    nGenres = len(genres.keys())
    nWords  = nKeys + nGenres
    nMovies = len(movies.keys())
    
    print('Matrix dimension: {0}x{1}'.format(nWords, nMovies))
    
    # genres + keywords  x nMovies
    # first nLines are genres...
    
    bow = lil_matrix((nWords,nMovies))    
    
    hg  = open(outHg, 'w')
    wHg = csv.writer(hg, delimiter=',',
                         quotechar='|', quoting=csv.QUOTE_ALL, lineterminator='\n')
    
    wordF  = open(outWords, 'w')
    wWord = csv.writer(wordF, delimiter=',',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    
    for idx in range(0,nWords):
        if idx < len(genres.keys()):            
            wWord.writerow([idx,genres[idx+1]])
        else:
            wWord.writerow([idx,keywords[idx - nGenres+1]])
    
    for id in movies:
        
        val = [id]
        
        idM = id - 1
        movie = movies[id]
        
        val.append(movie['cast'])
                        
        #looking the genre
        fv = [0]*nWords
        for g in movie['genre']:
            idx = g - 1
            bow[idx,idM] = 1
            fv[idx] = 1
        
        #looking the keyword
        for k in movie['keywords']:
            idx = nGenres + k - 1
            bow[idx,idM] = 1
            fv[idx] = 1
            
            
        val.append(fv)    
        wHg.writerow(val)
    
    return bow 



bok = bagOfWords( 'movie.csv', 
                 'keywords.csv', 
                 'genres.csv', 
                 'hg.csv', 
                 'words.csv')



def check_data(data, strs):
    s = "\n".join(data);
    for k in strs:
        if k in s:
            return True

    return False

def check_string(name, keys):
    for k in keys:
        if k.lower() == name:
            return True
    
    return False


