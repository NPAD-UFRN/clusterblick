import time
import sys
sys.path.insert(0, './tools/')
import readRawData as r, sendEmail as e, readConfig as c, dataHandler as handler
import json
import datetime
from collections import deque
import subprocess


#todo: rendering index

#rendering configurations
config = c.readConfig('config.txt','all')

#main parameters
alloc_hist,idle_hist,resvmant_hist,down_hist,other_hist,label_hist,nodepd_hist,jobspd_hist = deque(),deque(),deque(),deque(),deque(),deque(),deque(),deque()
list_hist=[]
frequency=0
th_enable=datetime.datetime.now()-datetime.timedelta(seconds=10)

#command to run slurmblick bash exec
slurmblick = 'echo nothing'

print '----------------------------------\nClusterBlick on\n----------------------------------\n\n'
try:
	while True:
		now = datetime.datetime.now()

		#do every 10 seconds
		if now-th_enable>datetime.timedelta(seconds=10):
			#time controllers
			th_enable=datetime.datetime.now()
			frequency+=1
			print '\n',th_enable

			try:
				process = subprocess.Popen(slurmblick.split(), stdout=subprocess.PIPE)
				output, error = process.communicate()
				print '0 - slurmblick sucessfuly run in the cluster'
			except:
				print ">>except: slurmblick does not sucessfuly attend cluster report"

			#reading general information
			general_dict = r.readRaw(config['raw_files'],config['raw_files_email'],config['path_raw'],config['path_data'])
			print '1 - Raw data available: ',general_dict.keys()

			#handling raw data to get information about the nodes grid, nodes hist and nodes grid
			list_dic, stats_dic, tsv_concat = handler.getNodeInfo()
			print '2 - Node information was processed'

			#queueinfo is a list of numbers: [0] of nodepd and [1] of jobsppd
			queueinfo = handler.getQueueInfo()
			print '3 - Queue information was processed'

			json_data = json.dumps(list_dic).replace('{','\n{')
			json_stats = json.dumps(stats_dic)
			list_hist=[alloc_hist,idle_hist,resvmant_hist,down_hist,other_hist,label_hist,nodepd_hist,jobspd_hist]
			handler.writeOutInfo(json_data,json_stats,tsv_concat,list_hist)
			print '4 - All data was stored in js objects'

			print '\n'

		#do every 5 minutes
		if frequency>=1:#1 to test, 60 to real
			frequency=0

			#appending new data
			alloc_hist.append(stats_dic['allocs'])
			idle_hist.append(stats_dic['idles'])
			resvmant_hist.append(stats_dic['resvmants'])
			down_hist.append(stats_dic['downs'])
			other_hist.append(stats_dic['others'])
			label_hist.append(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
			nodepd_hist.append(queueinfo[0])
			jobspd_hist.append(queueinfo[1])
			#clean hist to use only 576 elements
			if len(alloc_hist)>288:
				alloc_hist.popleft()
				idle_hist.popleft()
				resvmant_hist.popleft()
				down_hist.popleft()
				other_hist.popleft()
				label_hist.popleft()
				nodepd_hist.popleft()
				jobspd_hist.popleft()

			#Sending email if something unexpected happens
			e.emailControl(general_dict,stats_dic)









except KeyboardInterrupt:
	print '--------------------------------\nClusterBlick off\n----------------------------------\n\n'
