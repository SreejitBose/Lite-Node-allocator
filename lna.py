import time
import threading
import os
import sys
import re
lock = threading.Lock()

class threadtester (threading.Thread):
    def __init__(self, st,en):
       threading.Thread.__init__(self)
       self.st = st
       self.en=en
    def run(self):
       thread_test(self.st,self.en)
       

def thread_test(st,en):
    global count
    for i in range(st,en):
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
            lock.acquire()
            count=count+1
            nodes.append(a)
            sys.stdout.write('\r')
            sys.stdout.write("[+]Node added csews{} ".format(i))
            sys.stdout.flush()
            lock.release()


if (len(sys.argv)<2 or len(sys.argv)>3):
    print("[-] Usage: python3 check2.py <no. of nodes> <ppn>")
    exit(0)
if os.path.isfile('host_file'):
    os.system('rm host_file')
nodes=[]
count=0
threadarr=[]
numthreads=os.popen("nproc").read()
numthreads=int(numthreads)
chunk=int(121/numthreads)
for i in range(1,numthreads+1):
    if (i==numthreads):
        thr = threadtester((chunk*(i-1)+1),122)
    else:
        thr = threadtester((chunk*(i-1)+1),(chunk*i)+1)
    threadarr.append(thr)
    
for i in range(numthreads):
    threadarr[i].start()

for i in range(numthreads):
    threadarr[i].join()
if (len(nodes)<int(sys.argv[1])):
    print("\n[-]"+str(len(nodes))+" nodes have cores "+sys.argv[2]+", try with less number of nodes")
    exit(0)
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

