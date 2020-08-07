import os
import argparse
from collections import defaultdict

if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--in", required=True,
                    help="input directory")
    ap.add_argument("-o", "--out", required=True,
                    help="output directory")

    args = vars(ap.parse_args())

    in_dir = args['in']
    out_dir = args['out']

    try:
        os.mkdir(out_dir)
    except:
        pass
    
    wav_dict = defaultdict()
    for f in os.listdir(in_dir):
        infile = os.path.join(in_dir, f)
        outfile = os.path.join(out_dir, os.path.splitext(f)[0] + '.wav')

        _, port = str(os.path.splitext(f)[0]).split('_')
        
        sport, dport = port.split('-')
        os.system('sox -c 1 -t raw -r 8000 -e u-law {} {}'.format(infile, outfile))
        wav_dict[(sport, dport)] = outfile

    processed_port = []
    for sport, dport in wav_dict.keys():
        if (sport, dport) in processed_port:
            continue
        
        os.system('sox -m {} {} {}'.format(wav_dict[(sport, dport)], wav_dict[(dport, sport)], os.path.join(out_dir, sport+'-'+dport+'_merged.wav')))
        processed_port.append((sport, dport))
        processed_port.append((dport, sport))




    