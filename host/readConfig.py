
def readConfig(file):
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
			raw = lines[lines.index(line)+1].split(':')[1].strip()
			data = lines[lines.index(line)+2].split(':')[1].strip()
		elif line[0:11]=='#Raw files:':
			raw_files = lines[lines.index(line)+1].split(',')
			raw_files = [item.strip() for item in raw_files]
		elif line[0:20]=='#Raw files to email:':
			raw_files_email = lines[lines.index(line)+1].split(',')
			raw_files_email = [item.strip() for item in raw_files_email]
		
	return {'fromaddr':fromaddr,'password':password,'list_clients':toaddr,'path_raw':raw,'path_data':data,'raw_files':raw_files,'raw_files_email':raw_files_email}