import random
import re
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-01-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"YOU"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"ME"}   
        else:
            self.myID = 0
            self.title('34743-01-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        # 소켓을 사용하여 메시지 수신
        recv_msg = self.socket.recv(SIZE).decode() 

        # ETTTP 형식 확인
        msg_valid_check = check_msg(recv_msg, self.recv_ip) 
        
        # 메시지가 유효하지 않으면 소켓을 닫고 종료 
        if msg_valid_check == False:
            self.socket.close()   
            self.quit()
            return
        
        else: 
            # 메시지가 유효하면 ACK 메시지를 보내고, 보드를 업데이트하고, 턴을 변경한다. 
            # 받은 메시지에서 좌표값을 추출하여 ROW와 COL에 저장한다. 
            line=recv_msg.split('\r\n')
            move=line[2].split(':')[1]
            row=int(move[1])
            col=int(move[3])

            # ACK 메시지 생성    
            ack_msg = f"ACK ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n" 

            # ACK 메시지 전송 
            self.socket.send(ack_msg.encode())
            
            # 받은 좌표를 이용하여 위치 계산 
            loc = int(row) * 3 + int(col) 

            ######################################################   
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''
        # 현재 사용자의 턴이 아니면 메시지를 보내지 않고 텍스트 박스를 비움. 
        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        
        # 텍스트 박스에서 메시지를 가져온다. 
        d_msg = self.t_debug.get(1.0,"end")

        # 메시지를 보낼 때 줄 바꿈 문자가 올바르게 변환되도록 처리 
        d_msg = d_msg.replace("\\r\\n","\r\n")   
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        # 입력된 메시지에서 좌표값 찾기 
        line=d_msg.split('\r\n')
        move=line[2].split(':')[1]
        row=int(move[1])
        col=int(move[3])
        user_move = int(row) * 3 + int(col)

        # 선택된 위치가 이미 차 있으면 함수를 종료 
        if self.board[user_move] != 0:
            return

        '''
        Send message to peer 
        '''
        # 생성한 메시지를 소켓을 통해 전송 
        self.socket.send(d_msg.encode()) 
        '''
        Get ack
        '''
        # 피어로부터 ACK 메시지 수신 
        ack_msg = self.socket.recv(SIZE).decode()
        # 수신한 ACK 메시지의 유효성 검사 
        ack_valid = check_msg(ack_msg, self.recv_ip)

        # ACK 메시지가 유효하지 않으면 게임을 종료 
        if ack_valid == False:
            self.socket.close()
            self.quit()
        else:
            # ACK 메시지가 유효하면 좌표를 이용하여 위치 계산 
            loc = int(row) * 3 + int(col)

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)
        ###################  Fill Out  #######################
        # 메시지 전송 및 ACK 확인 

        # 선택된 버튼의 위치를 포함한 메시지를 생성 
        message = f"SEND ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"

        # 생성한 메시지를 소켓을 통해 전송 
        self.socket.send(message.encode())

        # 피어로부터 ACK 메시지를 수신
        ack = self.socket.recv(SIZE).decode()
    
        # 수신한 ACK 메시지의 유효성을 검사하고 결과를 반환 
        return check_msg(ack, self.recv_ip)
        ######################################################  

    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        # get 파라미터가 True 일 때, 상대방의 결과 메시지를 먼저 수신하고, 그 후 자신의 결과 메시지를 전송
        if get: 
            winner = "YOU"
            
            # 상대방으로부터 결과 메시지 수신 
            result_recv = self.socket.recv(SIZE).decode()

            # 받은 결과 메시지가 유효성 검사 
            result_valid = check_msg(result_recv, self.recv_ip)

            # 자신의 결과 메시지 생성 및 전송 
            result_msg =  f"RESULT ETTTP/1.0\r\nHost:{self.send_ip}\r\nWinner:{winner}\r\n\r\n" 
            self.socket.send(result_msg.encode())
            
            # 받은 결과 메시지에서 승자 정보 추출 
            recv_winner = result_recv.split('\r\n')[2].split(':')[1]

            # 유효성 체크하고 누가 승자인지 확인 
            if result_valid and recv_winner == 'ME':
                return True
            else:
                return False

        # get 파라미터가 False일 때: 자신의 결과 메시지를 먼저 전송하고, 그 후 상대방의 결과 메시지를 수신    
        else: 
            winner = "ME"
            # 자신의 결과 메시지 생성 및 전송 
            result_msg = f"RESULT ETTTP/1.0\r\nHost:{self.send_ip}\r\nWinner:{winner}\r\n\r\n"
            self.socket.send(result_msg.encode())
            
        
            # 상대방으로부터 결과 메시지 수신 
            result_recv = self.socket.recv(SIZE).decode()

            # 받은 결과 메시지의 유효성 검사
            result_valid = check_msg(result_recv, self.recv_ip) 

            # 받은 결과 메시지에서 승자 정보 추출 
            recv_winner = result_recv.split('\r\n')[2].split(':')[1]

            # 유효성 체크하고 누가 승자인지 확인 
            if result_valid and recv_winner == 'YOU' :
                return True 
            else: 
                return False
             
        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):
    '''
    Function that checks if received message is ETTTP format
    '''
    # 메시지를 줄 단위로 나눈다. 
    lines = msg.split('\r\n')

    # 줄 길이가 5가 아니면 False 반환 
    if len(lines) != 5: 
        return False
    
    # 각 줄을 분할하여 변수에 저장 
    type = lines[0].split(" ")[0] # 메시지 TYPE을 저장한다 (SEND/ACK/RESULT)
    version = lines[0].split(" ")[1] # ETTTP 버전 저장한다
    host_ip = lines[1].split(":")[1].strip() # 호스트 ip를 저장한다. 
    
    # 프로토콜 버전 체크
    if version != "ETTTP/1.0":
        return False
    # 호스트 ip 체크
    elif host_ip != recv_ip:
        return False
    
    # 메시지 타입이 SEND일 경우
    if type == "SEND" :
        # 3번째 줄에서 New-Move 또는 First-Move 인지 확인 
        if lines[2].split(":")[0].strip() == "New-Move" or lines[2].split(":")[0].strip() == "First-Move" :
            return True
        else :
            return False

    # 메시지 타입이 ACK인 경우     
    elif type == "ACK" : 
        # 3번째 줄에서 New-Move 또는 First-Move 인지 확인
        if lines[2].split(":")[0].strip() == "New-Move" or lines[2].split(":")[0].strip() == "First-Move" :
            return True
        else :
            return False

    # 메시지 타입이 RESULT인 경우
    elif type == "RESULT": 
        return True
    
    # 매치되는 타입이 없으면 False 반환 
    else:  
        return False

    ######################################################  