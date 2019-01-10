import optparse
from socket import *
from threading import Thread

# Make a Connection
def ConnScan(Target_Host, Target_Port):
    try:
        connskt = socket(AF_INET, SOCK_STREAM)
        # Make a Socket Connection (TCP)
        connskt.connect((Target_Host, Target_Port))
        # Try to connect
        connskt.send('Vionlent python\r\n')
        # Send Packet with message
        result = connskt.recv(1024)
        print "[+] %d / TCP OPEN" % Target_Port
        print "\n" + str(result)
        connskt.close()
        # Close the connection
    except:
        print "[-] %d TCP CLosed\n" % Target_Port

# Define Host and Port
def PortScan(Target_Host, Target_Port):
    try:
        Target_IP = gethostbyname(Target_Host)
    except:
        print "[-] Cannot Resolve '%s' : Unknown Host\n" % Target_Host
        return

    try:
        Target_Name = gethostbyname(Target_IP)
        print "\n[+] Scan Result For : " + Target_Name[0]
    except:
        print "\n[+] Scan Result For : " + Target_IP
    setdefaulttimeout(1)

    for port in Target_Port:
    # Target_Ports includes all ports that user input (List Type)
        print "Scanning Port \n" + port
        t = Thread (target=ConnScan, args=(Target_Host, int(port)))
        t.start()

# Main Function Area
def main():

    parser = optparse.OptionParser(usage='Usage %Prog -H <Target Host> # -p <Target Port>')
    parser.add_option('-H', dest = 'Target_Host', type ='string', help = 'Specify Target IP')
    #parser.add_option('-p', dest = 'Target_Port', type ='string', help = 'Specify Target Port')
    (options, args) = parser.parse_args()

    Target_Host = options.Target_Host
    Target_Port = str(options.Target_Port).split(',')

    if (Target_Host == None) | (Target_Port == None):
        print parser.usage
        exit (0)

    PortScan(Target_Host, Target_Port)

if __name__ == '__main__':
    main()
