import socket

from struct import*
host = ''
port = 12345

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print (host, port)
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True :
    try :
        data = conn.recv(1024)
        if not data : break
        print( "Client Says : ", data)
        print(unpack('fff', data))

    except socket.error:
        print("ERROR OCCURED.")
        break
conn.close()

