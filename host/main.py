import time
import readRawData as r, sendEmail as e, readConfig as c

flag_ping,flag_down=0,0

while True:
	
	config = c.readConfig('config.txt')
	data_dictionary = r.readRaw(config['raw_files'],config['raw_files_email'],config['path_raw'],config['path_data'])	
	
	#Sending email if something goes wrong
	downnodes = data_dictionary['email_dictionary'].get('ssupervisor_sinfo3',0)
	pingbool = data_dictionary['email_dictionary'].get('ssupervisor_ping',None)
	if pingbool==0 and flag_ping==0:
		message = '\nWARNING:\n\nPing is not returning any package, please check if the cluster\' service is available and working normally.'
		print message
		e.sendEmail(message)
		flag_ping=1
	elif pingbool==1 and flag_ping==1:
		flag_ping=0
	if downnodes>=4 and flag_down==0:
		message = '\nWARNING:\n\nThere are {} down nodes. Please check if something unexpected happened.'.format(downnodes)
		print message
		e.sendEmail(message)
		flag_down=1
	elif downnodes<4 and flag_down==1:
		flag_down=0
		
	time.sleep(5)