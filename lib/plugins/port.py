from linker import *

def connect(host,port,output):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2)
    try:
        sock.connect((host, port))
        output[port] = True
    except Exception as e:
        output[port] = False

def chkports(host,ports):
    if ports == None: ports = '443,80,8080,8081,9000,3306,3389,2222,21,22,445'
    threader  = Threader(len(ports)/2,name='PRTSCN')
    output = {}
    for port in ports.split(','): threader.put(connect, [host,int(port),output])
    threader.finish_all()
    return ' '.join([Fore.GREEN + str(k) for k,v in output.items() if v == True])