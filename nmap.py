import os
import argparse

def get_nmap(options, ip):
    num = [0, 0, 0]
    # [22port, 23port, 80port]
    # 0-closed, 1-open

    command = "nmap " +options + " "+ ip
    process = os.popen(command)
    results = str(process.read())
    r=results.split()
    del r[0:28:1]
    del r[-12:-1:1]
    r.pop()

    #for group in chunker(r, 3):
    #    print(group)
    #IP PORT SCAN INFORMATION
    
    if '22/tcp' in r:
        num[0] = 1
    elif '23/tcp' in r:
        num[1] = 1
    elif '80/tcp' in r:
        num[1] = 1
    
    return num


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

#print(get_nmap(' -F', '172.30.1.40'))

parser = argparse.ArgumentParser()
parser.add_argument("-foo",help="python3 nmap.py -f <target IP>", required=True)
args = parser.parse_args()
foo = args.foo

#if args.ip:
print(get_nmap(' -F', foo))
