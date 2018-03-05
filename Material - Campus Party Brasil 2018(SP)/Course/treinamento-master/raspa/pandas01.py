import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# mhfsilveira
df = pd.read_csv('http://assets.datacamp.com/course/intermediate_python/gapminder.csv', index_col = 0)
gdp_cap = list(df.gdp_cap)
life_exp = list(df.life_exp)
pop = list(df['population']/1e6)
cont = list(df.cont)
lut = {
    'Asia':'red',
    'Europe':'green',
    'Africa':'blue',
    'Americas':'yellow',
    'Oceania':'black'
}
col = [lut[x] for x in cont]

# Scatter plot
plt.scatter(x = gdp_cap, y = life_exp, s = np.array(pop) * 2, c = col, alpha = 0.8)

# Customizations
plt.xscale('log') 
plt.xlabel('PIB per Capita [em USD]')
plt.ylabel('Expectativa de Vida [em anos]')
plt.title('World Development 2007')
plt.xticks([1000,10000,100000], ['1k','10k','100k'])


plt.text(1550, 70, 'Índia')
plt.text(5700, 78, 'China')
plt.text(42951, 78, 'EUA')
plt.text(9065,72, 'Brasil')


plt.grid(True)
plt.show()
