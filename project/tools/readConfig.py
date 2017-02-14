#It reads config.txt and return a dictionary
def readConfig(file,string):
	with open(file) as config:
		lines = config.readlines()
	for line in lines:
		if line[0:21]=='#Email configuration:':
			fromaddr = lines[lines.index(line)+1].strip()
			password = lines[lines.index(line)+2].strip()
		elif line[0:15]=='#Email clients:':
			toaddr = lines[lines.index(line)+1].split(',')
			toaddr = [item.strip() for item in toaddr]
		elif line[0:20]=='#Path configuration:':
			raw = lines[lines.index(line)+1].split('::')[1].strip()
			data = lines[lines.index(line)+2].split('::')[1].strip()
			appindex = lines[lines.index(line)+3].split('::')[1].strip()
			cluster = lines[lines.index(line)+4].split('::')[1].strip()
			server = lines[lines.index(line)+5].split('::')[1].strip()
		elif line[0:11]=='#Raw files:':
			raw_files = lines[lines.index(line)+1].split(',')
			raw_files = [item.strip() for item in raw_files]
		elif line[0:20]=='#Raw files to email:':
			raw_files_email = lines[lines.index(line)+1].split(',')
			raw_files_email = [item.strip() for item in raw_files_email]
		elif line[0:20]=='#Node names allowed:':
			nn_allowed = lines[lines.index(line)+1].split(',')
			nn_allowed = [item.strip() for item in nn_allowed]
		elif line[0:21]=='#Cluster information:':
			ip = lines[lines.index(line)+1].split(':')[1][0:-1]
			port = lines[lines.index(line)+2].split(':')[1][0:-1]
			user = lines[lines.index(line)+3].split(':')[1][0:-1]


	config_dic={'fromaddr':fromaddr,'password':password,'list_clients':toaddr,'path_raw':raw,'path_data':data,'appindex':appindex,'path_cluster':cluster,'path_server':server,'raw_files':raw_files,'raw_files_email':raw_files_email,'nn_allowed':nn_allowed,'ip':ip,'port':port,'user':user}

	if string=='all':
		return config_dic
	else:
		try:
			return config_dic[string]
		except:
			print 'ERROR: config.txt does not have this configuration item available'
