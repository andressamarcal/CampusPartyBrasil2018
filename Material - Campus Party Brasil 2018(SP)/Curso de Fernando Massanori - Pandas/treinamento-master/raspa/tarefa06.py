import requests
from bs4 import BeautifulSoup as bs

prefix = "https://www.cinemark.com.br"
url_pagina = prefix + "/sao-jose-dos-campos/filmes/em-cartaz?pagina="
filmes = set()
for npagina in (1, 2):    
    p = requests.get(url_pagina+str(npagina))
    s = bs(p.content, "html.parser")
    for filme in s.findAll('a',
                {'class':'movie-image'}):                     
        filmes.add(filme['title'][6:])

for f in filmes:
    print (f)
        
