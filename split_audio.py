from rtp.decode import decode_audio
import dpkt
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument('-f', '--file', required=True, help="pcap file")
    
    args = vars(ap.parse_args())

    pcap_file = args['file']
    pc = dpkt.pcap.Reader(open(pcap_file, 'rb'))
    trafficfilter = 'rtp'
    pc.setfilter(trafficfilter)

    decode_audio(pc)