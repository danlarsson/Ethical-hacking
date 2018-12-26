#!/usr/bin/python

# Capture and print packets going thrue this computerself.
# Run with arp-spoof
#
# To be able to listen to local traffic we need anoter IP-tables filter
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0
#
# Flush, remove the config from iptables with
# iptables --flush

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)  # Bind the queue to the queue number assigned in the iptables command
                               # And a callback function called process_packet
queue.run()  # Start the queue
