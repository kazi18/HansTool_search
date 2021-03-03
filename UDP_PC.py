import socket
import os


def broadcast_PC():
    port = 9966  # 端口号
    flag = 1
    Robot_num = []
    Robot_state = []
    try:
        PC_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        PC_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        PC_send.connect(('255.255.255.255', port))
        PC_send.send('hans'.encode('utf-8'))
        PC_send.close
        PC_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        PC_rec.settimeout(2)
        PC_rec.bind(('', port))
        while True:
            try:
                #data, addr = PC_rec.recvfrom(1024)
                ip = PC_rec.recv(1024).decode('UTF-8')
                #ip = addr[0]
                #print(ip)
                # if ip not in Robot_num:
                if ip not in Robot_num and ip != 'hans':
                    Robot_num.append('http://' + ip + '/dist')
                    Robot_state.append('连接')
            except:
                if not Robot_num:
                    Robot_num.append('Error')
                    Robot_num.append(10001)
                break
        PC_rec.close
        #print(Robot_num)
        return Robot_num, Robot_state
    except:
        Robot_num.append('Error')
        Robot_num.append(10000)
        return Robot_num, Robot_state
