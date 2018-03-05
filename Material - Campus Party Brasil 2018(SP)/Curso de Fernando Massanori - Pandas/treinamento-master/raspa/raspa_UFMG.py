#
#  INCOMPLETO: não houve tempo para terminar!!
#

import requests
from bs4 import BeautifulSoup as bs

u = 'http://www.portaldatransparencia.gov.br/servidores/OrgaoExercicio-ListaServidores.asp?CodOS=15000&DescOS=MINISTERIO%20DA%20EDUCACAO&CodOrg=26238&DescOrg=UNIVERSIDADE%20FEDERAL%20DE%20MINAS%20GERAIS&Pagina='
base = 'http://www.portaldatransparencia.gov.br/'

def extrai_valor(u):
    j = u.find('=') + 1
    k = u.find('&', j)
    servidor = u[j: k]
    u = base + 'servidores/Servidor-DetalhaRemuneracao.asp?Op=2&IdServidor=%s&CodOrgao=26238&CodOS=15000&bInformacaoFinanceira=True' %servidor
    #print (u)
    p = requests.get(u)
    s = bs(p.content, 'html.parser')
    if 'Total da Remuneração Após Deduções' not in str(s):
        print ('Servidor %s sem informação de salário' %servidor)
        return
    x = s.find('tr', class_="remuneracaolinhatotalliquida")
    valor = x.find('td', class_="colunaValor")
    valor = valor.string.replace('.', '')
    valor = valor.replace(',', '.')
    print (valor)
    return float(valor)
    

valores_brutos = {}
for k in range(1, 555):
    url = u + str(k)
    print (url)
    p = requests.get(url)
    print ('Página:', k)
    s = bs(p.content, 'html.parser')
    x = s.findAll('table')
    profs = x[1].findAll('tr')
    for p in profs[1:]:
        a = p.find('a')
        nome = a.string.strip()
        valor = extrai_valor (a['href'])
        valores_brutos[nome] = valor

def segundo(a): return a[1]
maiores = sorted(key=segundo, reverse=True)
print (maiores[:30])
