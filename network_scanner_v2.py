#!/usr/bin/env python

import scapy.all as scapy
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')
network = str(parser.get('main', 'network'))

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast = broadcast/arp_request   # Combine the ARP and Ehter packets-
    answered_list = scapy.srp(arp_broadcast, timeout = 1, verbose = False)[0]  # Send and a recieve a packet with a custom Ether. Timeout on 1 second

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list


def print_result(result_list):
    print('IP\t\t\tMAC Address')
    print('-'*40)

    for client in result_list:
        print('%s\t\t%s' % (client['ip'], client['mac']))

scan_result = scan(network)
print_result(scan_result)
