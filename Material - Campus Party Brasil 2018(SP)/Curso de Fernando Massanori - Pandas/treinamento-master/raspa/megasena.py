import requests
from bs4 import BeautifulSoup as bs

url = 'http://www1.caixa.gov.br/loterias/loterias/megasena/megasena_pesquisa_new.asp'
p = requests.get(url)
s = bs(p.content, 'html.parser')
lista = s.find('ul')
números = lista.findAll('li')
for n in números: print (n.getText())
