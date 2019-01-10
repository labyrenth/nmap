import nmap
import optparse

def NmapScan(TargetHost, TargetPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(TargetHost, TargetPort)
    state = nmScan[TargetHost]['tcp'][int(TargetPort)]['state']
 
    print " [*] " + TargetHost + "TCP / " + TargetPort + " " + state
 
def main():
    parser = optparse.OptionParser(usage='usage %prog -H <TargetHost> -P <TargetPort>')
    parser.add_option('-H', dest = 'TargetHost', type='string', help ='Specify Target Hostname')
    parser.add_option('-P', dest = 'TargetPort', type='string', help = 'Sepcify Target Port')
    (options, args) = parser.parse_args()
 
    TargetHost = options.TargetHost
    TargetPort = str(options.TargetPort).split(',')
 
    if (TargetHost == None) | (TargetPort[0] == None):
        print parser.usage
        exit(0)
 
    for port in TargetPort:
        NmapScan(TargetHost, port)
 

if __name__ == '__main__':
    main()

