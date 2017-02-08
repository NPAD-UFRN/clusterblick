# clusterblick

This project is a supervisor web static application for Slurm scheduled clusters to monitor reports about queue and nodes' state and allocation. It also monitors login's node memory allocation and pings it to check availability. It has the functionality of emailing when not expecting cluster behavior has been detected. The core functionalities are in Python, but visualization gadgets are Javascripts, from D3JS and ChartJS (see references below).

###cluster
Contain shell scripts to run in cluster login node. It basically run sinfo, squeue, df -h, ping and top and send its result to host.
TODO: cluster been executed from host ssh

###host
The host is the computer that maintain the supervisor static javascrip application. It receives cluster report files and manipulate it into js objects to use in web application.

####App demo

![Demo](https://raw.githubusercontent.com/adelsondias/cluster-supervisor/master/project/app/print.png)

###references

Gauges - http://bl.ocks.org/tomerd/1499279
Donut and line chart - http://www.chartjs.org/docs/
Node Grid - http://bl.ocks.org/tjdecke/5558084
