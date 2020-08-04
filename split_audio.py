from rtp.decode import decode_audio
import dpkt
import pcap
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--interface', help="network interface")
    group.add_argument('-f', '--file', help="pcap file")

    ap.add_argument("-o", "--out", required=True,
                    help="output directory")

    args = vars(ap.parse_args())

    if args['interface']:
        iface = args['interface']
        pc = pcap.pcap(iface)
    elif args['file']:
        pcap_file = args['file']
        pc = dpkt.pcap.Reader(open(pcap_file, 'rb'))
        trafficfilter = 'rtp'
        pc.setfilter(trafficfilter)

    out_dir = args['out']

    decode_audio(pc, out_dir)