title: Networking problems while cloning Ubuntu VM
date: 2011-12-03 00:00
author: Chris Stucchio
tags: ubuntu, networking, ec2




I've run into a curious error while cloning Ubuntu VM hard drives. After cloning, the network card no longer works. However, if I clone the VM completely (including the mac address), there is no problem. 
The reason for this is that Ubuntu, upon installation, stores the mac address of the network card. This ensures the same network card will always be mapped to eth0, and future network cards will be eth1, etc.

However, this behavior is not desirable when cloning a VM.

One solution is to delete the stored mac address upon booting, which can be done with this script (add it to /etc/rc.local ):

<script src="https://gist.github.com/1427698.js"> </script>

This will fail horribly if your VM has multiple network interfaces.

