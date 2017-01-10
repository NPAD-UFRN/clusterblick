path = './raw/'
path_out = './data/'

raw_list = ['ssupervisor_dfh1.txt','ssupervisor_sinfo1.txt','ssupervisor_sinfo2.txt','ssupervisor_squeue1.txt']
raw_list_email = ['ssupervisor_ping.txt','ssupervisor_sinfo3.txt']

def readRaw(raw_list,path,path_out):
	import os,re,json
	for item in range(0,len(raw_list)):
	#Para cada item em raw_list
		raw_name = raw_list[item][0:raw_list[item].find('.')]
		FILEPATH = os.path.join(path, raw_list[item])
		OUTFILEPATH = os.path.join(path_out, raw_name+'.js')

		with open(FILEPATH) as f:
			lines = f.readlines()
		q_date, q_title, keys= [], [], []
		dic = {}
		dic_data = []

		counter=0
		for line in lines:
			if line[2]=='/' and line[5]=='/':
				q_date.append(line)
				counter += 1

			elif line[0]=='[':
				q_title.append(line)
				counter +=1

			elif counter>=2:
				if line[0]=='#':
					break
				elif counter==2:
					keys = line.split()
					counter +=1
				else:
					if line[0:14]=='Not responding':
						line = line.replace('Not responding', 'Not_responding')
					values = line.split()
					for i in range(0,len(values)):
						dic.update({keys[i]:values[i]})
					dic_data.append(dic)
					dic={}
					counter+=1
		json_data = json.dumps(dic_data)

		#write into json
		with open(OUTFILEPATH,'w+') as outfile:
			outfile.write('var '+raw_name+' = ')
			outfile.write(json_data)
			outfile.write(';')

readRaw(raw_list,path,path_out)			
	

		