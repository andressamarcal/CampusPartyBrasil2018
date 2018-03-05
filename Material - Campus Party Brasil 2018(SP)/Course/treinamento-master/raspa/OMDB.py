import json
import requests
import pandas as pd
url = 'http://www.omdbapi.com/?t=Stranger Things&Season=2&apikey=e25dd5fa'
data = requests.get(url).content
data = json.loads(data)
print (data['Episodes'])
df = pd.DataFrame.from_dict(data['Episodes'])
print (df)
