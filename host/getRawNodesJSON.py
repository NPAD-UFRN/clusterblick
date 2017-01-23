#It reads ssupervisor_sinfo1.js and get nodes and their respective state to write into nodes_sinfo.js
def getRawNodesJSON():
	import os,re,json
	import readConfig as c

	#Path and configurations
	PATH = c.readConfig('config.txt','path_data')
	NODE_NAMES_ALLOWED = c.readConfig('config.txt','nn_allowed')
	FILEPATH = os.path.join(PATH[1:-1], 'ssupervisor_sinfo1.js')
	OUTFILEPATH = os.path.join(PATH[1:-1], 'nodes_sinfo.js')

	with open(FILEPATH) as f:
		lines = f.readlines()
		raw=str(lines)
		raw = raw.replace('{','\n{')
		lines = raw.split('\n')
	nodes, states = [], []
	for line in lines:
		n_flag, s_flag=0, 0
		n_start, n_end, s_start, s_end= 0, 0, 0, 0
		if line[0]=='{':

			for i in range(0,len(line)):
				#
				if line[i:i+8]=='NODELIST':
					n_flag=1
				elif line[i]==':' and n_flag==1:
					n_start=i+3
				elif line[i-2:i]=='",' and n_flag==1:
					n_flag=0
					n_end=i-2
				#
				if line[i:i+5]=='STATE':
					s_flag=1
				elif line[i]==':' and s_flag==1:
					s_start=i+3
				elif line[i-2:i]=='",' and s_flag==1:
					s_flag=0
					s_end=i-2
			if line[n_start:n_end] not in nodes:
				nodes.append(line[n_start:n_end])
			if line[s_start:s_end] not in states:
				states.append(line[s_start:s_end])

	#splitting nodes names
	aux=[]
	list_dic = []
	for item in nodes:
		#splitting first step: separate node interval
		#ex: "r1i0n[1-3],r1i0n[5-6]" to "r1i0n[1-3]","r1i0n[5-6]" 
		splitted = item.split(',r')
		for i in range(0,len(splitted)):
			if ','+NODE_NAMES_ALLOWED[1][0:-1] in splitted[i]:
				oversplit = splitted[i].split(','+NODE_NAMES_ALLOWED[1][0])
				for j in range(0,len(oversplit)):
					if oversplit[j][0:6]==NODE_NAMES_ALLOWED[1][1:-1]:
						oversplit[j] = NODE_NAMES_ALLOWED[1][0]+oversplit[j]
					splitted.append(oversplit[j])
				splitted.remove(splitted[i])

			if splitted[i][0].isdigit(): 
				splitted[i] = "r"+splitted[i]	
			#splitting second step: separate each node
			#ex: "r1i0n[1-3]","r1i0n[5-6]" to "r1i0n1","r1i0n2","r1i0n3","r1i0n5","r1i0n6"
		for iitem in splitted:
			stat = states[nodes.index(item)]
			full_names=[]
			if '[' in iitem:
				_names = iitem[0:iitem.find("[")]
				_numbers = iitem[iitem.find("[")+1:iitem.find("]")].split(',')
				for num in _numbers:
					if '-' in num:
						nu = num.split('-')
						for k in range(int(nu[0]),int(nu[1])+1):
							full_names.append(_names+str(k))
					else:
						full_names.append(_names+num)
			else:
				full_names.append(iitem)
			print full_names
			for iiitem in full_names:
				dic={}
				dic['name']=iiitem
				dic['state']=stat
				list_dic.append(dic)


	json_data = json.dumps(list_dic).replace('{','\n{')
	with open(OUTFILEPATH,'w+') as outfile:
		outfile.write('var nodes = ')
		outfile.write(json_data)
		outfile.write(';')
