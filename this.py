import os

def get_nmap(options, ip):
    #num = [1, 1]
    #port, close //

    command = "nmap " +options + " "+ ip
    process = os.popen(command)
    results = str(process.read())
    r=results.split()
    del r[0:28:1]
    del r[-12:-1:1]
    r.pop()

    for group in chunker(r, 3):
        print group
        #if group[0]=='22/tcp':
            #print "22 port/ssh open"
         #   print "22.1"
         #   if group[0]=='80/tcp':
         #       print "80.1"

          #      if group[0]=='23/tcp':
            #        print "23.1"
           #     else :
             #       print "23.0"
            #else :
             #   print "80.0"
       # else :
       #     print "22.0"


#if group[0]=='80/tcp':
       #     #print "80 port/http open"
         #   print "80.1"
#
      #  else:
      #      print "80.0"
##
      #  if group[0]=='23/tcp':
      #      #print "23 port/telnet open"
      #      print "23.1"
      #  else:
      #      print "23.0"


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

print(get_nmap(' -F', '192.168.0.51'))


