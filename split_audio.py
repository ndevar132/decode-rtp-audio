from rtp.decode import decode_audio
import dpkt

if __name__ == '__main__':
    pcap_file = 'test_180s.pcap'
    pc = dpkt.pcap.Reader(open(pcap_file, 'rb'))
    trafficfilter = 'rtp'
    pc.setfilter(trafficfilter)

    decode_audio(pc)