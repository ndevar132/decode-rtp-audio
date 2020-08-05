import dpkt
import pcap
import os
import socket
import time
import argparse
from collections import defaultdict

payload_dict = defaultdict(list)

def decode_audio(pc, out_dir):
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
    
                # rtp payload starts at bytes 13 (offset 12 bytes for rtp header)
                rtp_payload = udp_payload[12:]
                payload_dict[(src, dst, sport, dport)].append(rtp_payload)
                number_rtppackets += 1

    for [src, dst, sport, dport], payload_list in payload_dict.items():
        all_payloads = b''.join(payload_list)
        src_addr = socket.inet_ntoa(src)
        dst_addr = socket.inet_ntoa(dst)

        reverse_src, reverse_dst, reverse_sport, reverse_dport = dst, src, dport, sport
        
        # if there is a pair of rtp communication, consider valid audio
        number_singlertp = 0
        if (reverse_src, reverse_dst, reverse_sport, reverse_dport) not in payload_dict:
            number_singlertp += 1
            continue

        out_dir += '/'

        try:
            os.mkdir(out_dir)
        except:
            pass

        with open(out_dir + src_addr + '-' + dst_addr + '_' + str(sport) + '-' + str(dport) + '.raw', 'wb') as f:
            f.write(all_payloads)
