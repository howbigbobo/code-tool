import socket
import sys
import os
s = socket.socket()
s.bind(("10.172.97.82", 9999))
s.listen(10)  # Accepts up to 10 connections.

while True:
    sc, address = s.accept()

    print(address)
    i = 1

    with open('file_' + str(i) + ".zip", 'wb') as f:  #open in binary
        i = i + 1
        l = 1
        total = 0
        while (l):
            l = sc.recv(4096)
            while (l):
                total += 4
                print('receive {}k'.format(total), end='\r', flush=True)
                f.write(l)
                l = sc.recv(4096)
        print('receive complete, total {}k'.format(total))
    sc.close()

s.close()