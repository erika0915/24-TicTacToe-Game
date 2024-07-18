import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg
    

if __name__ == '__main__':
    SERVER_IP = '127.0.0.1' # 서버 IP 주소 설정 
    MY_IP = '127.0.0.1' # 클라이언트 IP 주소 설정 
    SERVER_PORT = 12000 # 서버 포트 번호 설정 
    SIZE = 1024 # 버퍼 크기 설정 
    SERVER_ADDR = (SERVER_IP, SERVER_PORT) # 서버 주소 설정 

    # 클라이언트 소켓 생성 및 서버에 연결 
    with socket(AF_INET, SOCK_STREAM) as client_socket: 
        client_socket.connect(SERVER_ADDR)
        
        ##############################################################
    
        # 서버로부터 누가 먼저 시작할 것이지에 대한 정보를 수신 
        # 서버로부터 메시지 수신 
        start_msg=client_socket.recv(SIZE).decode()

        #받은 메시지를 '\r\n'기준으로 나눔
        split_msg=start_msg.split('\r\n') 

        #split_msg의 3번째 원소를 ': '기준으로 나누고 2번째 원소를 player에 저장
        player=split_msg[2].split(':')[1] 

    
        # 받은 메시지의 유효성 검사 
        msg_info = check_msg(start_msg, SERVER_IP)

        if msg_info == True:
           # player 값에 따라 start 값을 설정 
            if player=="ME":
                # 서버 선
                start=0 
                starter="YOU"
            else:
                # 클라이언트 선
                start=1 
                starter="ME"
        elif msg_info == False:
             client_socket.close()

        ##############################################################
        
        # ACK 전송 

        ack=f"ACK ETTTP/1.0 \r\nHost:{MY_IP}\r\nFirst-Move:{starter}\r\n\r\n"
        client_socket.send(ack.encode())    
            
        ##############################################################
        
        # 게임 시작

        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start) # 게임 시작, 선 플레이어 설정 
        root.mainloop() # GUI 이벤트 루프 실행 
        
        client_socket.close() # 클라이언트 소켓 종료 