import socket
import time
import logging

if __name__ == "__main__":
    port = 9966  # 端口号
    while True:
        try:
            Robot_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            Robot_rec.settimeout(10)
            Robot_rec.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            Robot_rec.bind(('', port))
            print('the port is:', port)
            print('in connect...')
            try:
                while True:
                    Robot_send = socket.socket(
                        socket.AF_INET, socket.SOCK_DGRAM)
                    data, addr = Robot_rec.recvfrom(1024)
                    ip = addr[0]
                    data = data.decode('UTF-8')
                    if (data == 'hans'):
                        #time.sleep(1)
                        Robot_send.connect((ip, port))
                        my_ip = Robot_send.getsockname()[0]
                        Robot_send.send(my_ip.encode('utf-8'))
                        print("sending success")
                        Robot_send.close
            except:
                Robot_rec.close
                Robot_send.close
        except:
            continue