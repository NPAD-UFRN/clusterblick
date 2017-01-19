#Author: Adelson Araujo Junior (NPAD/UFRN)

'''
This script defines readRaw() function with these parameters:
	- raw_list: list of file names that contains raw data to be prepared into JSON
	- path: path of these files
	- path_out: path of JSONs output
'''

def readRaw(raw_list,raw_list_email,path,path_out):
	import os,re,json
	
	#outputs
	email_dic={}
	general_dic={}
	
	#external 'for' to travel raw_list
	for item in range(0,len(raw_list)):
		raw_name = raw_list[item][0:raw_list[item].find('.')] 	#name of the raw_list's item (input)
		FILEPATH = os.path.join(path[1:-1], raw_list[item])			#input file path
		OUTFILEPATH = os.path.join(path_out[1:-1], raw_name+'.js')	#output file path
		
		#internal variables
		q_date, q_title, keys= [], [], []
		dic = {}
		dic_data = []
		counter, flag_email, email_data=0, 0, 0

		#reading the file itself
		with open(FILEPATH) as f:
			lines = f.readlines()
		for line in lines:

			#collecting the query's date
			if counter==0:
				q_date.append(line)
				counter += 1
			#checking if it is an EMAIL information (files in raw_list_email have a line EMAIL meaning that its information will be sent via email if some trouble happens)
			elif line[0:5]=='EMAIL':
				flag_email=1
				counter +=1
			#getting query's title
			elif line[0]=='[':
				q_title.append(line)
				counter +=1
			#working on non-email input files
			elif counter>=2 and flag_email==0:
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
			#working on email input files
			elif counter>=2 and flag_email==1:
				
				if ' 0% packet loss' in line:
					email_data=1
				if line[0:5]=='NODES':
					email_data=lines[lines.index(line)+1]
				counter+=1
		
		#write into path_out/JSONs
		if (raw_name+'.txt') in raw_list_email:
			json_data = json.dumps(email_data).replace('{','\n{')
			email_dic[raw_name] = email_data
		else:
			json_data = json.dumps(dic_data)
			general_dic[raw_name] = dic_data
		with open(OUTFILEPATH,'w+') as outfile:
			outfile.write('var '+raw_name+' = ')
			outfile.write(json_data)
			outfile.write(';')
			
	return {'general_dictionary':general_dic,'email_dictionary':email_dic}

#Usage example:			
'''		
path = './raw/'
path_out = './data/'
raw_list = ['ssupervisor_ping.txt', 'ssupervisor_sinfo3.txt','ssupervisor_dfh1.txt','ssupervisor_sinfo1.txt','ssupervisor_sinfo2.txt','ssupervisor_squeue1.txt']
raw_list_email = ['ssupervisor_ping.txt', 'ssupervisor_sinfo3.txt']
			
dic = readRaw(raw_list,raw_list_email,path,path_out)	
'''


		
