#!/usr/bin/env python

from scapy.all import *
import base64

secret_message = "TopSecretInfo:MeetAtNoon"
encoded_message = base64.b64encode(secret_message.encode()).decode().replace("=", "")

packets = []
chunk_size = 10
for i in range(0, len(encoded_message), chunk_size):
    chunk = encoded_message[i:i+chunk_size]
    domain = f"{chunk}.example.com"
    packet = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=domain))
    packets.append(packet)

wrpcap("dns.pcap", packets)
print("dns.pcap generated.")
