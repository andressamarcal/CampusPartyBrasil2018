import requests
from bs4 import BeautifulSoup as bs

b = 'https://www.buzzfeed.com/trending'
p = requests.get(b)
s = bs(p.content, 'html.parser')

hot = s.findAll('div', {'class':'hot-item'})
for h in hot:
  head = h.find('a', {'class':'hot-headline'})
  texto = head.get_text().strip()
  k = texto.find('\n')
  print (texto[:k])
  print ()
  
