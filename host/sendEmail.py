'''
Function to send email
Issue: point the server smtp and port
'''

def sendEmail(email_to, subject, message):
	import smtplib
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText 

	with open('config.txt') as config:
		lines = config.readlines()
	for line in lines:
		if line[0:21]=='#Email configuration:':
			index = lines.index(line)
			email_login = lines[index+1]
			password = lines[index+2]

	fromaddr = email_login
	toaddr = email_to
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject

	body = message
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
