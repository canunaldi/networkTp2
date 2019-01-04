# ceng435 Term Project Part 2
## By:
### Ozan Incesulu, 2099711
### Can Duran Unaldi, 2036523

This project consists of 3 python scripts:
* broker.py
* destination.py
* source.py

The detailed explanations for each script can be found in comments.

The project was uploaded to GENI slices we created. The running order of the slices in order to minimize the packet loss to 0 is:
* destination.py from d 
* broker.py from b
* source.py from s

It is important to start the script for the machine s as the final step.

For the r1 and r2 we've used the following terminal commands:

R1:

```bash
sudo route add -net 10.10.3.2 netmask
255.255.255.255 gw 10.10.3.2
```

```bash
sudo route add -net 10.10.2.1 netmask
255.255.255.255 gw 10.10.2.1
```

R2:

```bash
sudo route add -net 10.10.5.2 netmask
255.255.255.255 gw 10.10.5.2
```

```bash
sudo route add -net 10.10.4.1 netmask
255.255.255.255 gw 10.10.4.1
```

The purpose of the scripts are explained below:

### source.py

The source file connects to the "s" node in our slice. The main object of this script is to send the packet to the broker(aim = is to send to the destination). Just sends all the packets without waiting acknowledge.

### broker.py

This file connects to the "b" node in our slice. The main object of this file is to send the packet coming from the source (get the packet) and by choosing between r1 and r2 send the incoming packet to one of them. By using the window, base,checksum,timeout and nextseqnum, broker creates a reliable transfer that uses multihoming and pipelining.

### destination.py

This file connects to the "destination" node in our slice. By using threading, gets the packet from the r1 and r2 and calculates the checksum. It checks the corruption of the packet and if not sends the corresponding acknowledgement.


# EXPERIMENTS

We take tc qdisc change dev eth0 root netem delay 20ms 5ms distribution normal code as a base for our experiments.

The eth0 changes in each link. We found which eth can be used by using ifconfig.

## Experiment 1

In this experiment we used the following commands:

At b:
```bash
sudo tc qdisc add dev eth1 root netem delay 1ms 5ms distribution normal
sudo tc qdisc add dev eth2 root netem delay 1ms 5ms distribution normal
```
At r1:
```bash
sudo tc qdisc add dev eth2 root netem delay 1ms 5ms distribution normal
```
At r2:
```bash
sudo tc qdisc add dev eth2 root netem delay 1ms 5ms distribution normal
```
Note: You can use change command instead of add if you already have tc at the slices.

The experiment results comming from the d stored at results.csv

## Experiment 2

In this experiment we used the following commands:

At b:
```bash
sudo tc qdisc change dev eth1 root netem delay 20ms 5ms distribution normal
sudo tc qdisc change dev eth2 root netem delay 20ms 5ms distribution normal
```
At r1:
```bash
sudo tc qdisc change dev eth2 root netem delay 20ms 5ms distribution normal
```
At r2:
```bash
sudo tc qdisc change dev eth2 root netem delay 20ms 5ms distribution normal
```
Note: change command used since we've already added tc to the slices.


## Experiment 3

In this experiment we used the following commands:

At b:
```bash
sudo tc qdisc change dev eth1 root netem delay 60ms 5ms distribution normal
sudo tc qdisc change dev eth2 root netem delay 60ms 5ms distribution normal
```
At r1:
```bash
sudo tc qdisc change dev eth2 root netem delay 60ms 5ms distribution normal
```
At r2:
```bash
sudo tc qdisc change dev eth2 root netem delay 60ms 5ms distribution normal
```
Note: change command used since we've already added tc to the slices.


# Useful Commands

* To close the running python script. (The Ctrl+C does not work for scripts using threads)
```bash
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9 
```
* To ensure the closing
```bash
pkill python
```
