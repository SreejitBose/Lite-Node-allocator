import os
import re
import sys

if (len(sys.argv)<2 or len(sys.argv)>3):
    print("[-] Usage: python3 check2.py <no. of nodes> <ppn>")
    exit(0)
if os.path.isfile('host_file'):
        os.system('rm host_file')
nodes=[]
for i in range(1,89):
    res=os.system("ssh -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=yes csews{} uptime > /dev/null 2>&1".format(i))
    if(res==0):
        a=[]
        ppn=int(sys.argv[2])
        get_ppn=os.popen("ssh csews{} nproc".format(i)).read()
        if(get_ppn=='' or ppn> int(get_ppn)):
            continue
        resp=os.popen("ssh csews{} uptime".format(i)).read()
        match=re.findall(r"[-+]?\d*\.\d+|\d+", resp)
        load=float(match[7])
        a.append("csews{}".format(i))
        a.append(load)
        nodes.append(a)
        per=(i/88)*100
        sys.stdout.write('\r')
        #sys.stdout.write("Scanning node - {}\n".format(str(i)))
        sys.stdout.write("[+]Scanning for nodes........ complete - {:.2f}%".format(per))
        sys.stdout.flush()

print("\n[+]Making host file ......")
nodes.sort(key=lambda x: x[1])
if(len(sys.argv)==2):
    for j in range(int(sys.argv[1])):
        f=open("host_file","a")
        f.write(nodes[j][0]+"\n")
        f.close()
elif(len(sys.argv)==3):
    for j in range(int(sys.argv[1])):
        f=open("host_file","a")
        f.write(nodes[j][0]+":"+sys.argv[2]+"\n")
        f.close()   
else:
    print("Usage")
print("DONE")
