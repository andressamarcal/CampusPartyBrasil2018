from bs4 import BeautifulSoup as bs
import requests
import locale
locale.setlocale(locale.LC_ALL, '')

u = 'https://uspdigital.usp.br/portaltransparencia/portaltransparenciaListar?paginar=s&dtainictc=01%2F10%2F2017&nompes=&nomundorg=&nomdepset=&tipcon=&tipcla=&nomabvfnc=&Submit=Solicitar+pesquisa&reload=buscar&imagem=S&print=true&chars=4b9k&pag='
teto = 21631.05
for k in range(1, 856):
  print (f'Página {k}')
  saida = open('SálariosUSP.txt', 'a')
  p = requests.get(u+str(k))
  s = bs(p.content, 'html.parser')
  t = s.find('table', {'class':'table_list'})
  f = t.findAll('tr')
  for x in f[1:]:
    tds = x.findAll('td')
    nome = tds[0].string
    função = tds[-6].string
    tempoUsp = tds[-4].string
    salário = tds[-2].string
    salário = locale.atof(salário)
    if salário > teto:
      saida.write(','.join([nome, função, tempoUsp, str(salário)]) + '\n')
  saida.close()
