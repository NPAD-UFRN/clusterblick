# cluster-supervisor

This project is a supervisor web application for Slurm scheduled clusters to monitor reports about queue and nodes' state and allocation. It also monitors login's node memory allocation and pings it to check availability. It has the functionality of emailing: in demo version, it sends an email if pings goes wrong or if a setpoint number of nodes goes down.


###cluster
Contain shell scripts to run in cluster login's node. It basically run sinfo, squeue, df -h and ping commands and send its result to host.

###host
The host is the computer that maintain the supervisor application. It receives cluster report files and manipulate it into JSON objects to use in web application.

####App demo

![Demo](https://raw.githubusercontent.com/adelsondias/cluster-supervisor/master/host/app/print.png)

