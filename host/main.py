import time
import readRawData as r, sendEmail as e, readConfig as c, getRawNodes as g
import json
import datetime
from collections import deque

#todo: rendering app

#rendering configurations
config = c.readConfig('config.txt','all')

#getRawNodes parameters initializing
alloc_hist,idle_hist,down_hist,label_hist = deque(),deque(),deque(),deque()
list_hist=[]
frequency=0
th_enable=datetime.datetime.now()-datetime.timedelta(seconds=10)

#emailing parameters
#flag_ping,flag_down=0,0

while True:
	now = datetime.datetime.now()

	#do every 5 seconds
	if now-th_enable>datetime.timedelta(seconds=5):
		th_enable=datetime.datetime.now()
		frequency+=1

		#reading general information
		general_dict = r.readRaw(config['raw_files'],config['raw_files_email'],config['path_raw'],config['path_data'])

		#handling raw data to get information about the nodes grid, nodes hist and nodes grid
		list_dic, stats_dic, tsv_concat = g.getRawNodes()
		json_data = json.dumps(list_dic).replace('{','\n{')
		json_stats = json.dumps(stats_dic)
		list_hist=[alloc_hist,idle_hist,down_hist,label_hist]
		g.writeOutNodeData(json_data,json_stats,tsv_concat,list_hist)

	#do every 5 minutes
	if frequency>=60:#1 to test, 60 to real
		frequency=0

		#managing data of nodes hist
		alloc_hist.append(stats_dic['allocs'])
		idle_hist.append(stats_dic['idles'])
		down_hist.append(stats_dic['downs'])
		label_hist.append(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
		#clean hist to use only 576 elements (nodes hist)
		if len(alloc_hist)>576:
			alloc_hist.popleft()
			idle_hist.popleft()
			down_hist.popleft()
			label_hist.popleft()




	#Sending email if something goes wrong - TO UPDATE
	'''
	downnodes = general_dict['email_dictionary'].get('ssupervisor_sinfo3',0)
	pingbool = general_dict['email_dictionary'].get('ssupervisor_ping',None)
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
	'''
