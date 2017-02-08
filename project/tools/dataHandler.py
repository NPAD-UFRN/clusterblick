import os,re,json
import readConfig as c

#(after readRaw)
#It reads sinfo1.js to return a list of node's information
def getNodeInfo():

	#Path and configurations
	PATH = c.readConfig('config.txt','path_data')
	NODE_NAMES_ALLOWED = c.readConfig('config.txt','nn_allowed')
	FILEPATH = os.path.join(PATH[1:-1], 'sinfo1.js')

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
				states.append(line[s_start:s_end])

	#splitting nodes names
	aux=[]
	list_dic = []
	for item in nodes:
		#splitting first step: separate node interval
		#ex: "r1i0n[1-3],r1i0n[5-6]" to "r1i0n[1-3]","r1i0n[5-6]"
		splitted = item.split(',r')
		for i in range(0,len(splitted)):
			if ','+NODE_NAMES_ALLOWED[1][0:-1] in splitted[i]: #if service in splitted[i]
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
			for iiitem in full_names:
				if NODE_NAMES_ALLOWED[1][1:-2] in iiitem: #if service in iiitem
					r = NODE_NAMES_ALLOWED[1][1:-2]
					i = NODE_NAMES_ALLOWED[1][1:-2]
					n = iiitem[iiitem.find(NODE_NAMES_ALLOWED[1][-5:-2])+3:]
				else:
					r = iiitem[iiitem.find('r')+1:iiitem.find('i')]
					i = iiitem[iiitem.find('i')+1:iiitem.find('n')]
					n = iiitem[iiitem.find('n')+1:]

				dic={}
				dic['name']=iiitem
				dic['r']=r
				dic['i']=i
				dic['n']=n
				dic['state']=stat
				list_dic.append(dic)

	#getting stats_dic and tsv_concat
	allocs,idles,downs=0,0,0
	tsv_concat = 'nnn\tiii\tvalue\n'
	for d in list_dic:
		if d['state']=='alloc':
			allocs+=1
			value=2
		elif d['state']=='idle':
			idles+=1
			value=1
		else:
			downs+=1
			value=0
		if d['i']==NODE_NAMES_ALLOWED[1][1:-2]:
			tsv_concat+=str(int(d['n'])+1)+'\t'+str(5)+'\t'+str(value)+'\n'
			tsv_concat+=''
		else:
			tsv_concat+=str(int(d['n'])+1)+'\t'+str(int(d['i'])+1)+'\t'+str(value)+'\n'

	stats_dic={'allocs':allocs,'idles':idles,'downs':downs}

	return [list_dic,stats_dic,tsv_concat]



#(after readRaw)
#It reads squeue1.js to return a list of numbers about jobsPD[1] and nodesPD[0]
def getQueueInfo():
	import ast
	#Path and configurations
	PATH = c.readConfig('config.txt','path_data')
	NODE_NAMES_ALLOWED = c.readConfig('config.txt','nn_allowed')
	FILEPATH = os.path.join(PATH[1:-1], 'squeue1.js')

	sumnodepd=0
	sumjobspd=0

	with open(FILEPATH) as f:
		lines = f.readlines()
		raw=str(lines)
		raw = raw.replace('{','\n{').replace('];','  \n];')
		lines = raw.split('\n')
	for line in lines:
		if line==lines[0]:
			continue
		if '];' in line:
			break
		else:
			dictionary = ast.literal_eval(line[:-2])
			if dictionary['ST']=='PD':
				sumjobspd+=1
				sumnodepd+=int(dictionary['NODES'])
	queueinfo=[sumnodepd,sumjobspd]

	return queueinfo



#(after getNodeInfo and getQueueInfo)
#It uses information from previous gets to write its result into files
def writeOutInfo(json_data,json_stats,tsv_concat,list_hist):
	OUTFILEPATHsinfo = 'app/js/nodes_sinfo.js'
	OUTFILEPATHstats = 'app/js/nodes_stats.js'
	OUTFILEPATHtsv = 'app/nodes.tsv'
	OUTFILEPATHsinfohist = 'app/js/sinfohist.js'
	OUTFILEPATHqueuehist = 'app/js/queuehist.js'

	with open(OUTFILEPATHsinfo,'w+') as outfile:
		outfile.write('var nodes = ')
		outfile.write(json_data)
		outfile.write(';')
	with open(OUTFILEPATHstats,'w+') as outfile:
		outfile.write('var stats = ')
		outfile.write(json_stats)
		outfile.write(';')
	with open(OUTFILEPATHtsv,'w+') as outfile:
		outfile.write(tsv_concat)
	with open(OUTFILEPATHsinfohist,'w+') as outfile:
		outfile.write('var alloc_hist = ')
		outfile.write(str(list(list_hist[0])))
		outfile.write(';\n')
		outfile.write('var idle_hist = ')
		outfile.write(str(list(list_hist[1])))
		outfile.write(';\n')
		outfile.write('var down_hist = ')
		outfile.write(str(list(list_hist[2])))
		outfile.write(';\n')
		outfile.write('var label_hist = ')
		outfile.write(str(list(list_hist[3])))
		outfile.write(';\n')
	with open(OUTFILEPATHqueuehist,'w+') as outfile:
		outfile.write('var sumnodepd = ')
		outfile.write(str(list(list_hist[4])))
		outfile.write(';\n')
		outfile.write('var sumjobspd = ')
		outfile.write(str(list(list_hist[5])))
		outfile.write(';\n')
		outfile.write('var label_hist = ')
		outfile.write(str(list(list_hist[3])))
		outfile.write(';\n')
