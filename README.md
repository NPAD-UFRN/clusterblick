# cluster-supervisor

This project is a supervisor web application for Slurm scheduled clusters to monitoring reports about nodes state and allocation, queue. It also monitors login's node memory allocation and pings it to alert by e-mail if it's going down or it's memory overloads.


###cluster
Contain shell scripts to run in cluster login's node. It basically run sinfo, squeue, df -h and ping commands and send its result to the host.

###host
The host is the computer that maintain the supervisor application. It receives cluster report files and manipulate it into JSON objects to use in web application.
