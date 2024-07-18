import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

if __name__ == '__main__':
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM) # 서버 소켓 생성
    server_socket.bind(('',SERVER_PORT)) # 서버 소켓을 지정된 포트에 바인딩
    server_socket.listen() # 서버 소켓을 리슨 상태로 설정 
    MY_IP = '127.0.0.1' # 서버 IP 주소 설정 

    while True:
        client_socket, client_addr = server_socket.accept() # 클라이언트 연결 수락 
    
        start = random.randrange(0,2)  # 선 플레이어를 랜덤으로 선택 (0 또는 1)
        
        ##############################################################
    
        # 선 플레이어 정보를 피어에게 전송 
        
        # start가 0이면 서버가 선, 1이면 클라이언트가 선
        if start==0:
            player='ME'
        else:
            player='YOU'

        # 선 플레이어 정보를 포함한 메시지 생성 
        start_msg=f'SEND ETTTP/1.0 \r\nHost:{MY_IP}\r\nFirst-Move:{player}\r\n\r\n'
        client_socket.send(start_msg.encode())  # 클라이언트한테 메시지 전송
        
        # 클라이언트로부터 ACK 메시지 수신 - ACK가 올바르면 게임을 시작
        # 클라이언트로부터 ACK 받음
        recv_ack=client_socket.recv(SIZE).decode() 

        # 받은 ACK가 옳지 않으면 종료
        if check_msg(recv_ack, MY_IP)==False:
            client_socket.close()
            continue # 루프의 다음 반복으로 건너뛰기 
            
        ##############################################################
        # 게임 시작 
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
            
        client_socket.close()
        break
    server_socket.close()