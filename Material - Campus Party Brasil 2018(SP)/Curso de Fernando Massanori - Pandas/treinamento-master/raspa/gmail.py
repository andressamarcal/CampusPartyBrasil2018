import smtplib
#https://omadson.wordpress.com/2016/04/22/enviando-emails-com-python/ 
emitte = 'fmasanori@gmail.com'
passwd = 'qX8reOwL49AL'
 
recip = 'fmasanori@fatec.sp.gov.br'
subje = 'Confirmação do workshop'.encode('utf-8')
texto = 'Estamos a uma semana do workshop. Ainda temos uma lista de espera.'.encode('utf-8')
 
msg = '\r\n'.join([
  'From: %s' % emitte,
  'To: %s' % recip,
  'Subject: %s' % subje,
  '',
  '%s' % texto
  ])
 
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.ehlo()
server.login(emitte, passwd)
server.sendmail(emitte, recip, msg)
server.quit()
