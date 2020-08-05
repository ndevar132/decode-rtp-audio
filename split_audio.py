from rtp.decode import decode_audio
import dpkt
import pcap
import argparse
import time

def parse_arguments(ap):
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--interface', help="network interface")
    group.add_argument('-f', '--file', help="pcap file")

    ap.add_argument("-o", "--out", required=True,
                    help="output directory")
    ap.add_argument("-d", "--duration", type=float, 
                help="duration of capture from network iface (in seconds)")

    args = vars(ap.parse_args())

    is_iface = False # is using network interface?
    duration = -1

    if args['interface']:
        if args['duration'] is None:
            ap.error("--interface requires --duration.")
        duration = args['duration']
        iface = args['interface']
        pc = pcap.pcap(iface)
        is_iface = True
    elif args['file']:
        pcap_file = args['file']
        pc = dpkt.pcap.Reader(open(pcap_file, 'rb'))
        trafficfilter = 'rtp'
        pc.setfilter(trafficfilter)

    out_dir = args['out']

    return pc, out_dir, duration, is_iface

def main():
    ap = argparse.ArgumentParser()
    pc, out_dir, duration, is_iface = parse_arguments(ap)
    

    start = time.time()
    decode_audio(pc, out_dir, start, duration, is_iface)
    print(time.time() - start)

if __name__ == '__main__':
    main()
    