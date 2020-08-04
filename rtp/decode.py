import dpkt
import pcap
import os
import time
import argparse
from collections import defaultdict

payload_dict = defaultdict(list)

def decode_audio(pc):
    number_rtppackets = 0
    for _, pkt in pc:
        eth = dpkt.ethernet.Ethernet(pkt)
        # check if ip packet
        if eth.type == dpkt.ethernet.ETH_TYPE_IP:
            ip = eth.data
            # check if udp
            if ip.p == dpkt.ip.IP_PROTO_UDP:
                udp = ip.data
                udp_payload = udp.data

                # get udp header attribute
                src, dst, sport, dport = ip.src, ip.dst, udp.sport, udp.dport

                # check if it is rtp
                if sport < 1024 or dport < 1024 or udp_payload[0] != 128:
                    continue

                print(udp_payload, '\n')
    
                # rtp payload starts at bytes 13 (offset 12 bytes for rtp header)
                rtp_payload = udp_payload[12:]
                payload_dict[(src, dst, sport, dport)].append(rtp_payload)
                number_rtppackets += 1

                if number_rtppackets >= 10:
                    break

                
    
    
        

                

