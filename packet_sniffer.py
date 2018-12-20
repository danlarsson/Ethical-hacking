#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http

from configparser import ConfigParser
parser = ConfigParser()
parser.read('config.ini')
interface = parser.get('main', 'interface')

def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
	if packet.haslayer(http.HTTPRequest):
		print(packet)

sniff(interface)
