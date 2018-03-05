import locale
locale.setlocale(locale.LC_ALL, '')
valor = 1003353635.34
valor = locale.currency(valor, grouping=True, symbol=None)
print (valor, type(valor))
valor = locale.atof(valor)
print (valor, type(valor))
