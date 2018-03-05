import requests
from bs4 import BeautifulSoup as bs

u = 'http://www.portaldatransparencia.gov.br/servidores/OrgaoExercicio-ListaServidores.asp?CodOS=15000&DescOS=MINISTERIO%20DA%20EDUCACAO&CodOrg=26262&DescOrg=UNIVERSIDADE%20FEDERAL%20DE%20SAO%20PAULO&Pagina='
base = 'http://www.portaldatransparencia.gov.br/'

def extrai_valor(u):
    j = u.find('=') + 1
    k = u.find('&', j)
    id_servidor = u[j: k]
    u = base + 'servidores/Servidor-DetalhaRemuneracao.asp?Op=2&IdServidor=%s&CodOrgao=26262&CodOS=15000&bInformacaoFinanceira=True&Ano=2017&Mes=8' %id_servidor
    p = requests.get(u)
    s = bs(p.content, 'html.parser')
    if 'Total da Remuneração Após Deduções' not in str(s):
        return id_servidor, '0'
    x = s.findAll('tr', {'class':'remuneracaodetalhe'})
    valor = x[2].find('td', {'class':'colunaValor'})
    valor = valor.string.replace('.', '')
    valor = valor.replace(',', '.')
    return id_servidor, valor

for k in range(1, 481):  #checar se começa certo
    f = open('Unifesp.txt', 'a')
    url = u + str(k)
    p = requests.get(url)
    print ('Página:', k)
    s = bs(p.content, 'html.parser')
    x = s.findAll('table')
    profs = x[1].findAll('tr')
    for p in profs[1:]:
        a = p.find('a')
        nome = a.string.strip()
        id_servidor, valor = extrai_valor (a['href'])
        f.write(','.join([id_servidor, nome, valor]))
        f.write('\n')
    f.close()
                
