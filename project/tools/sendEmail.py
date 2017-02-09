# It send email to every client registered in config.txt
def sendEmail(message,subject):
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
		SUBJECT = subject

		msg.attach(MIMEText(message, 'plain'))

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, password)
		text = 'Subject: %s\n\n%s' % (SUBJECT, message)
		server.sendmail(fromaddr, email, text)
		server.quit()



# It controls general_dict information (from readRawData module)
# to send an warning to email registered people (config.txt) if
# something unexpected is going on
def emailControl(general_dict,stats_dic):

	#emailing parameters
	flag_ping=flag_down=flag_s0hd=flag_s0cpu=flag_lushd=0
	n_down,downbool=0,1
	service0_hdpct,s0hdbool=0,1
	service0_cpupct,s0cpubool=0,1
	lustre_hdpct,lushdbool=0,1


	#warning for unsucessfully ping
	pingbool = general_dict.get('ping',1)
	if pingbool==0 and flag_ping==0:
		message = '\nWARNING:\n\nPing in service0 is not returning any package, please check if it\'s working normally.\n'
		print message
		sendEmail(message,'ClusterBlick: Warning')
		flag_ping=1
	elif pingbool==1 and flag_ping==1:
		flag_ping=0

	#warning for each new down node
	if stats_dic['downs']>n_down:
		downbool = 0 #0 means it is going wrong
	if downbool==0 and flag_down==0:
		message = '\nWARNING:\n\nClusterBlick detects a new down node.\n'
		print message
		sendEmail(message,'ClusterBlick: Warning')
		flag_down=1
	elif downbool==1 and flag_down==1:
		flag_down=0
	n_down = stats_dic['downs']

	#warning for service0 hd overuse
	service0_hdpct = float(general_dict.get('dfh1')[0].get('Use%')[0:-1])
	if service0_hdpct > 80:
		s0hdbool=0 #0 means it is going wrong
	if s0hdbool==0 and flag_s0hd==0:
		message = '\nWARNING:\n\nClusterBlick detects service0 HD overuse.\n'
		print message
		sendEmail(message,'ClusterBlick: Warning')
		flag_s0hd=1
	elif s0hdbool==1 and flag_s0hd==1:
		flag_s0hd=0
	#warning for service0 cpu overuse
	service0_cpupct = float(general_dict.get('s0cpu'))
	if service0_cpupct > 80:
		s0cpubool=0 #0 means it is going wrong
	if s0cpubool==0 and flag_s0cpu==0:
		message = '\nWARNING:\n\nClusterBlick detects service0 CPU overuse.\n'
		print message
		sendEmail(message,'ClusterBlick: Warning')
		flag_s0cpu=1
	elif s0cpubool==1 and flag_s0cpu==1:
		flag_s0cpu=0

	#warning for lustre hd overused
	lustre_hdpct = float(general_dict.get('dfh1')[3].get('Use%')[0:-1])
	if lustre_hdpct > 90:
		lushdbool=0
	if lushdbool==0 and flag_lushd==0:
		message = '\nWARNING:\n\nClusterBlick detects lustre HD overuse.\n'
		print message
		sendEmail(message,'ClusterBlick: Warning')
		flag_lushd=1
	elif lushdbool==1 and flag_lushd==1:
		flag_lushd=0
