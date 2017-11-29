import socket
from TCP.C_Pack import DataStruct
from Data import C_StructSet
from Enemy.C_Enemy import Enemy1
from State import C_collision
import struct
_datastruct = DataStruct()
host = "127.0.0.1"
port = 12345
#PointStruct = {'pos_x': 0, 'pos_y': 0}
#pointXY = {'pos_x': Enemy1.returnx(), 'pos_y': Enemy1().returny()}
#print ( 'pointXY[0-1]', pointXY['pos_x'])
#butter = struct.pack("i i 6s",pointXY['pos_x'],pointXY['pos_y'], b'python')


s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(butter)
data = s.recv(1024)
s.close()
print('received!', repr(data))