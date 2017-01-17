#Author: Adelson Araujo Junior (NPAD/UFRN)

#commentary1: this function only works if your cluster is named 'rAiBnC' mixed with 'service' named nodes
#commentary2: you can change serviceX name to other if you want in NODE_NAMES_ALLOWEDS. If you want to change 'rAiBnC', please go though the code.
NODE_NAMES_ALLOWEDS = ['rAiBnC','serviceX']

import os,re,json

path = './data/'
js_file = 'ssupervisor_sinfo1.js'

FILEPATH = os.path.join(path, js_file)
OUTFILEPATH = os.path.join(path, 'nodes_sinfo.js')



nodes, states = [], []
with open(FILEPATH) as f:
	lines = f.readlines()
	raw=str(lines)
	raw = raw.replace('{','\n{')
	lines = raw.split('\n')
	
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
		
		nodes.append(line[n_start:n_end])
		states.append(line[s_start:s_end])
	

#splitting nodes names
aux=[]
list_dic = []
for item in nodes:
	#splitting first step: separate node interval
	#ex: "r1i0n[1-3],r1i0n[5-6]" to "r1i0n[1-3]","r1i0n[5-6]" 
	splitted = item.split(',r')
	for i in range(0,len(splitted)):
		if ','+NODE_NAMES_ALLOWEDS[1][0:-1] in splitted[i]:
			oversplit = splitted[i].split(','+NODE_NAMES_ALLOWEDS[1][0])
			for j in range(0,len(oversplit)):
				if oversplit[j][0:6]==NODE_NAMES_ALLOWEDS[1][1:-1]:
					oversplit[j] = NODE_NAMES_ALLOWEDS[1][0]+oversplit[j]
				splitted.append(oversplit[j])
			splitted.remove(splitted[i])
		if splitted[i][0].isdigit(): 
			splitted[i] = "r"+splitted[i]
		
		#splitting second step: separate each node
		#ex: "r1i0n[1-3]","r1i0n[5-6]" to "r1i0n1","r1i0n2","r1i0n3","r1i0n5","r1i0n6"
		if '[' in splitted[i]:
			_names = splitted[i][0:splitted[i].find("[")]
			_numbers = splitted[i][splitted[i].find("[")+1:splitted[i].find("]")]
			_numbers = _numbers.split(',')
			full_names = []
			for num in _numbers:
				if '-' in num:
					nu = num.split('-')
					for k in range(int(nu[0]),int(nu[1])+1):
						full_names.append(_names+str(k))
				else:
					full_names.append(_names+num)
			#adding it to a dictionary and the respective node' state
			for ii in full_names:
				dic = {}
				dic['name']=ii
				dic['state']=states[nodes.index(item)]
				if dic not in list_dic:
					list_dic.append(dic)
		
		
json_data = json.dumps(list_dic).replace('{','\n{')
with open(OUTFILEPATH,'w+') as outfile:
	outfile.write('var nodes = ')
	outfile.write(json_data)
	outfile.write(';')
