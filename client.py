#!/usr/bin/python3
import socket
import pickle

#send a Python object over socket, as long as the object is supported by pickle
def reliable_send(sk:socket.socket, msg):
    msg_b = pickle.dumps(msg,-1)
    msg_len = len(msg_b)
    msg_len_l = []
    while True:
        this_part = msg_len & 0x7fffffff
        msg_len >>= 31
        if msg_len != 0:
            this_part |= 0x80000000
        msg_len_l.append(this_part.to_bytes(4, byteorder = 'big'))
        if msg_len == 0:
            break
    msg_len_b = b''.join(msg_len_l)
    sk.sendall(msg_len_b)
    sk.sendall(msg_b)
#recv a Python object from socket, as long as the object is supported by pickle
def reliable_recv(sk:socket.socket):
    msg_len = 0
    msg_len_recv_cnt = 0
    msg_len_recvd = False
    all_l = []
    b_recved = 0
    while not msg_len_recvd or b_recved < msg_len + msg_len_recvd * 4:
        if not msg_len_recvd:
            this_b = sk.recv(1)
        else:
            this_b = sk.recv(msg_len + msg_len_recvd * 4 - b_recved)
        
        b_recved += len(this_b)
        all_l.append(this_b)
        print(str(all_l))
        if not msg_len_recvd and b_recved >= (msg_len_recv_cnt + 1) * 4:
            all_b = b''.join(all_l)

            while not msg_len_recvd and b_recved >= (msg_len_recv_cnt + 1) * 4:
                this_int = int.from_bytes(all_b[msg_len_recv_cnt * 4 : msg_len_recv_cnt * 4 + 4],byteorder='big')
                msg_len |= (this_int & 0x7fffffff) << (31 * msg_len_recv_cnt)

                if not (this_int & 0x80000000):
                    msg_len_recvd = True
                    print("Got len = "+str(msg_len))
                
                msg_len_recv_cnt += 1
    all_b = b''.join(all_l)
    return pickle.loads(all_b[msg_len_recv_cnt*4:])


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('127.0.0.1',1137))
    msg = reliable_recv(s)
    print(str(msg))
    msg = reliable_recv(s)
    print(str(msg))
    reliable_send(s,"Goodbye World")
    reliable_send(s,"Goodbye World Again")
    s.close()

    
        
            