import os
import argparse

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
    for f in os.listdir(in_dir):
        infile = os.path.join(in_dir, f)
        outfile = os.path.join(out_dir, os.path.splitext(f)[0] + '.wav')


        os.system('sox -c 1 -t raw -r 8000 -e u-law {} {}'.format(infile, outfile))
   

    