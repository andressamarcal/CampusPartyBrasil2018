import requests
from bs4 import BeautifulSoup

html = requests.get('https://sismpconsultapublica.mpsp.mp.br/ConsultarDistribuicao/ObterFiltrosPorMembro')

s = BeautifulSoup(html.content, 'html.parser')
nameList = s.findAll('option')
for name in nameList[1:-5]:
    print (name.string, name['value'])
