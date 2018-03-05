from urllib.request import urlopen
import json

p = urlopen('http://educacao.dadosabertosbr.com/api/escolas/buscaavancada?situacaoFuncionamento=1&energiaInexistente=on&aguaInexistente=on&esgotoInexistente=on')
resp = json.loads(p.read().decode('utf-8'))
print ('Número:', resp[0])

for e in resp[1]:
    print (e['nome'])
    print (e['estado'], e['regiao'])
    
