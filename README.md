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

We have created multiple slices and we have observed that we only need to change the broker's eth1 and eth3 interfaces (which route to r1 and r2), eth1 interface on r1 and eth2 interface on r2.
The commands executed to provide that are: 

On broker:
```bash
sudo tc qdisc add dev eth1 root netem loss {LOSS}% corrupt {CORRUPT}% duplicate 0% delay 3ms reorder {REORDER}
sudo tc qdisc add dev eth3 root netem loss {LOSS}%  corrupt {CORRUPT}% duplicate 0% delay 3 ms reorder {REORDER}
```
On r1:
```bash
sudo tc qdisc add dev eth1 root netem loss {LOSS}% corrupt {CORRUPT}% duplicate 0% delay 3ms reorder {REORDER}
```
On r2:
```bash
sudo tc qdisc add dev eth2 root netem loss {LOSS}% corrupt {CORRUPT}% duplicate 0% delay 3ms reorder {REORDER}
```

In these commands `{LOSS}`, `{CORRUPT}` and `{REORDER}` are values that are given in homework text and that change based on experiment
If these commands are applied with `change` instead of `add` as 3rd argument sometimes the interface configuration doesn't exist, which results with an error.
# Useful Commands

* To close the running python script. (The Ctrl+C does not work for scripts using threads)
```bash
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9 
```
* To ensure the closing
```bash
pkill python
```
