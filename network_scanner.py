#!/usr/bin/env python

import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast = broadcast/arp_request   # Combine the ARP and Ehter packets-
    answered_list = scapy.srp(arp_broadcast, timeout = 1, verbose = False)[0]  # Send and a recieve a packet with a custom Ether. Timeout on 1 second

    print('IP\t\t\tMAC Address')
    print('-'*40)

    for element in answered_list:
        print(element[1].psrc + "\t\t" + element[1].hwsrc)

    # print(answered_list.summary())
    # print(arp_broadcast.show())
    # print(arp_request.summary())
    # scapy.ls(scapy.ARP())

scan('10.10.100.0/24')
