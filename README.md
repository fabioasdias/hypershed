# Watershed on hypergraphs for data clustering

Fabio Dias, Moussa R. Mansour, Paola Valdivia, Jean Cousty and Laurent Najman

This implementation relates to the article presented in the 13th ISMM, available [at this link](https://link.springer.com/chapter/10.1007/978-3-319-57240-6_17).


The file hg.py is the base library that implements the hypergraph class, following networkx syntax. The files smalltest.py and movies.py run the method for the small synthetic hypergraph and the TMDB datasets.

There are several datasets, with different number of edges, on the data folder. The results folder contain our prototype interface. To reuse with other results, just replace the file l0.json in the data folder, inside of the results folder (not the data in the root folder).

Live results available at: http://alphasite.zapto.org/wshed/


Acknowledgments

Grants 2016/04391-2, 2014/12815-1, 2015/14426-5, 2013/21779-6,
2013/14089-3, 2011/22749-8 São Paulo Research Foundation (FAPESP). The
views expressed are those of the authors and do not reflect the
official policy or position of the São Paulo Research Foundation.