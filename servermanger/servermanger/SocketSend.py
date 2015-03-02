__author__ = 'Administrator'
import socket
def socket_send(ip,command):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip,1003))
    sock.send(command)
    data = ""
    count = 1
    End = "#zbcyh#"
    total_data = []
    while True:
        data = sock.recv(8192)
        count = count + 1
        print count
        if not len(data):
            break
        if End in data:
            total_data.append(data[:data.find(End)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            last_pair = total_data[-2] + total_data[-1]
            if End in last_pair:
                total_data[-2] = last_pair[:last_pair.find(End)]
                total_data.pop()
                break
    recv_data = ''.join(total_data)
    sock.close()
    return recv_data