import socket
import sys

s = socket.socket()
s.connect(("10.172.97.82", 9999))
with open("filettt.zip", "rb") as f:
    l = f.read(4096)
    while (l):
        s.send(l)
        l = f.read(4096)
    s.close()