from urllib.request import urlopen
from bs4 import BeautifulSoup

p = urlopen('https://sismpconsultapublica.mpsp.mp.br/ConsultarDistribuicao/ObterFiltrosPorMembro')
s = BeautifulSoup(p, "html.parser")
promotores = s.findAll('option')

for p in promotores[1:-5]:
    print (p.string, p['value'])
