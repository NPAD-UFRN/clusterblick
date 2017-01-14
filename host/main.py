path = './raw/'
path_out = './data/'
raw_list = ['ssupervisor_ping.txt', 'ssupervisor_sinfo3.txt','ssupervisor_dfh1.txt','ssupervisor_sinfo1.txt','ssupervisor_sinfo2.txt','ssupervisor_squeue1.txt']
raw_list_email = ['ssupervisor_ping.txt', 'ssupervisor_sinfo3.txt']
			
global_nodes_down = -1

while True:
	readRaw(raw_list,raw_list_email,path,path_out)	