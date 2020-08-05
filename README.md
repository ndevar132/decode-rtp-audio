# split_audio

Script split_audio.py can be used to split rtp audio stream from pcap file or network interface.
The converted audio is in raw format. To convert raw audio to wav, you could use sox.
Script convert_wav.py in the source can be use to convert raw audio to wav.

## Requirement

To use this program you have to install several python package: dpkt, pypcap.
You can install it through pip package manager

```sh
pip install dpkt
pip install pypcap
```

## Usage

To split rtp audio from pcap file:

```sh
$ python split_audio.py  -f <pcap file> -o <output directory>
```

To split rtp audio from network interface you have to execute the program with root privelege.
To test this you could redirect rtp stream from pcap file to network interface, using tcpreplay:

```sh
tcpreplay -i <network iface> <pcap file>
```

```sh
python split_audio.py  -i <iface> -o <output directory> -d <duration in seconds>
```

help usage:

```sh
$ python split_audio.py -h
usage: split_audio.py [-h] (-i INTERFACE | -f FILE) -o OUT [-d DURATION]

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        network interface
  -f FILE, --file FILE  pcap file
  -o OUT, --out OUT     output directory
  -d DURATION, --duration DURATION
                        duration of capture from network iface (in seconds)
```

To convert raw audio into wav format:

```sh
$ python convert_wav.py -i <directory of raw files> -o <output directory>
```

## Test

\*Tested on AMD Quad-Core Ryzen 5 Processor, 6.8GB DDR4, 1TB Sata HDD

To parse pcap file of ~1.8GB, the script takes ~220 second
Add this to split_audio.py

```python
...
start = time.time()
decode_audio(pc, out_dir)
print(time.time() - start)
```

```sh
$ python split_audio.py  -f test_180s.pcap -o test-out-reg
219.80524063110352
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
