# -*- coding utf-8 -*-
import sys
import socket

def get_args():
    args=sys.argv[1:]
    try:
        host_index=args.index('--host')
        port_index=args.index('--port')

        host_temp=args[host_index+1]
        port_temp=args[port_index+1]

        if len(host_temp.split('.'))!=4:
            print('Parameter Error')
            exit(-1)
        else:
            host=host_temp

        if '-' in port_temp:
            port=port_temp.split('-')
        else:
            port=[port_temp,port_temp]
        return host,port
    except (ValueError,IndexError):
        print('Parameter Error')
        exit(-1)

def scan():
    host=get_args()[0]
    port=get_args()[1]
    open_list=[]

    for i in range(int(port[0]),int(port[1])+1):
        s=socket.socket()

        s.settimeout(0.1)
        if s.connect_ex((host,i))==0:
            open_list.append(i)
            print(i,'open')
        else:
            print(i,'closed')
        s.close()
    print(f'Completed scan.Opening ports at {open_list}')
if __name__=='__main__':
    scan()