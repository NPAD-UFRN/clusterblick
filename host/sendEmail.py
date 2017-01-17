'''
Function to send email
Issue: point the server smtp and port
'''

def sendEmail(message):
	import smtplib
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText 

	fromaddr=''
	toaddr=[]
	
	with open('config.txt') as config:
		lines = config.readlines()
	for line in lines:
		if line[0:21]=='#Email configuration:':
			fromaddr = lines[lines.index(line)+1]
			password = lines[lines.index(line)+2]
		if line[0:15]=='#Email clients:':
			toaddr = lines[lines.index(line)+1].split(',')
			
	for email in toaddr:		
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = email
		SUBJECT = 'Cluster Supervisor'

		msg.attach(MIMEText(message, 'plain'))

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, password)
		text = 'Subject: %s\n\n%s' % (SUBJECT, message)
		server.sendmail(fromaddr, email, text)
		server.quit()
