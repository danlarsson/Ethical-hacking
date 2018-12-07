#!/usr/bin/env python

import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast = broadcast/arp_request   # Combine the ARP and Ehter packets-
    answered, unaswered = scapy.srp(arp_broadcast, timeout = 1)  # Send and a recieve a packet with a custom Ether. Timeout on 1 second
    print(answered.summary())

    # print(arp_broadcast.show())
    # print(arp_request.summary())
    # scapy.ls(scapy.ARP())

scan('143.237.100.0/24')



