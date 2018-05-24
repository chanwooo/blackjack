import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IP/TCP로 소켓을 생성
server_address = ('127.0.0.1', 12345)  # 접속할 주소와 포트넘버
sock.connect(server_address)  # 생성한 소켓으로 해당 주소에 접속

recvdata = sock.recv(4096)
print (recvdata.decode())


# 이것 저것 작업 하면 됨
while True:
# time.sleep(0.001)
 sock.send(b'99') #베팅할 금액

 recvdata = sock.recv(4096)
 print(recvdata.decode())

 if (recvdata.decode().find('Hit[1]')) != -1:
     sock.send(b'2')
     recvdata = sock.recv(4096)
     print(recvdata.decode())
 if recvdata.decode().find('GAME OVER') != -1:
     break

recvdata = sock.recv(4096)
print(recvdata.decode())

sock.close()