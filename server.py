import threading
import socket
import sys
import os

MSG_SIZE = 1024
ENCODING = 'utf-8'
user_list = []
lock = threading.Lock()
class User:
    def __init__(self, sock, addr):
        self.socket = sock
        self.ip = addr[0]
        self.port = addr[1]


def chat_thread(user):

    while True:
        # reveice message from client
        msg_from_client = user.socket.recv(MSG_SIZE)
        msg_from_client = msg_from_client.decode()
        ###############
        # user exit   #
        ###############
        if msg_from_client == "!exit":
            break
        #################
        # donwload file #
        #################
        if "#upload" == msg_from_client.split()[0]:
            file_name,file_size = msg_from_client.split()[1:3] # get file name and file size
            file_size = int(file_size)
            if not os.path.isdir("Server"):  # make server storage dir
                os.mkdir("Server")
            f = open(os.path.join("Server", file_name), "wb") # open a file for saveing received file
            fb = user.socket.recv(MSG_SIZE)
            while True:
                f.write(fb) # write received fragment of the file
                file_size -= len(fb) # count reveived file size
                if file_size <= 0:
                    break
                fb = user.socket.recv(MSG_SIZE) # receive next fragment
            f.close()
            # send file upload message
            upload_message = f"> User {user.ip}:{user.port} has uploaded a file"
            print(upload_message)
            lock.acquire()
            for u in user_list:
                if u != user:
                    u.socket.sendall(upload_message.encode(encoding=ENCODING)) # send upload message to all user
            lock.release()
            continue

        #######################
        # message from client #
        #######################
        msg_from_client = f'[{user.ip}:{user.port}] {msg_from_client}'
        print(msg_from_client, end="")
        lock.acquire()
        for u in user_list:
            if u != user:
                u.socket.sendall(msg_from_client.encode(encoding=ENCODING)) # send received message to all user
        lock.release()

    lock.acquire()
    user_list.remove(user) # delete user from user_list
    left_message = f"< The user {user.ip}:{user.port} left ({len(user_list)} user{'s'if len(user_list)>1 else ''} online)"
    for u in user_list:
        u.socket.sendall(left_message.encode(encoding=ENCODING)) # send left message to all user
    lock.release() # release lock
    print(left_message)
    user.socket.close() # close left user socket

if __name__ == "__main__":
    welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create welcome socket
    welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to handle error for overlapping address, port

    server_address, server_port = sys.argv[1:3] # read server address, port number from arguments
    welcome_socket.bind((server_address, int(server_port))) # set socket address, port number

    welcome_socket.listen(5) # max client queue to 5
    print(f"Chat server started on port {server_port}.")

    try:
        while True:
            client_socket, client_address = welcome_socket.accept() # accept client socket access request
            new_user = User(client_socket, client_address)
            user_list.append(new_user) # append new user to user_list
            new_user.socket.sendall(str(len(user_list)).encode()) # send user amount to all users
            new_user_message = f"> New user {new_user.ip}:{new_user.port} entered ({len(user_list)} user{'s' if len(user_list)>1 else ''} online)"
            print(new_user_message)
            for u in user_list:
                if u != new_user:
                    u.socket.sendall(new_user_message.encode())

            thread = threading.Thread(target=chat_thread, args=[new_user]) # new thread for new user
            thread.daemon = True
            thread.start() # thread start



    except KeyboardInterrupt: 
        # when keyboard interrupt detected make all users exit and close sockets
        # and terminate this program
        while len(user_list) != 0:
            u = user_list[-1]
            user_list.pop()
            u.socket.sendall("!exit".encode(encoding=ENCODING))
            u.socket.close()

        welcome_socket.close()
        print("\nexit")
