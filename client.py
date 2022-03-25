import socket
import sys
import threading
import select
import os 

MSG_SIZE = 1024
ENCODING = 'utf-8'
server_terminated = False

if __name__ == "__main__":
    server_ip, server_port = sys.argv[1:3]

    sock_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
    sock_to_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # handle error for reconnect on same port
    sock_to_server.connect((server_ip, int(server_port))) # connect to server port

    try:
        user_amount_in_server = sock_to_server.recv(MSG_SIZE).decode(encoding=ENCODING) #receive the number of users in server from server
        print(f"> Connected to the chat server ({user_amount_in_server} user{'s' if int(user_amount_in_server)>1 else ''} online)")

        while True:
            read_socket, write_socket, error_socket = select.select([sock_to_server, sys.stdin], [], [])
            for s in read_socket:
                ############################
                # read from sock_to_server #
                ############################
                if s == sock_to_server:
                    msg_from_server = sock_to_server.recv(MSG_SIZE).decode() # receive a message from the server
                    if msg_from_server == "!exit":
                        # when the message is "!exit", this means server will be terminated
                        # so terminate the program
                        server_terminated = True
                        raise KeyboardInterrupt
                    print(msg_from_server.strip(), end="\n")
                #########################
                # read from sys.stdin   #
                #########################
                else:
                    # read from sys.stdin
                    msg_to_server = sys.stdin.readline()
                    if msg_to_server == "!exit\n":
                        sock_to_server.sendall(msg_to_server.encode(encoding=ENCODING))
                        raise KeyboardInterrupt
                    ###############
                    # file upload #
                    ###############
                    if msg_to_server.split()[0] == "#upload":
                        # upload a file
                        file_name = msg_to_server.strip().split()[1].replace("'","")
                        if not os.path.isfile(file_name):
                            # when file does not exit
                            print("ERROR : file does not exist")
                            continue
                        file_size = os.path.getsize(file_name) # check file size
                        
                        # send command, file name, file size
                        sock_to_server.sendall(f"#upload {file_name} {file_size}".encode(encoding=ENCODING))
                        f = open(file_name, "rb")
                        fb = f.read(MSG_SIZE)
                        # send fragments of the file
                        while fb:
                            sock_to_server.sendall(fb)
                            fb = f.read(MSG_SIZE)

                        # print a message when uploading is finished
                        upload_message = f"\033[F> File '{file_name}’ has uploaded"
                        print(upload_message)
                        
                    else:
                        # print message this user has written
                        print(f'\033[F[You] {msg_to_server.strip()}')
                        sock_to_server.sendall(msg_to_server.encode(encoding=ENCODING))
    except KeyboardInterrupt:
        # when keyboard interrupt is detected,
        # let server know this user is goint to exit
        # and close sock_to_server and terminate the program
        if not server_terminated:
            sock_to_server.sendall("!exit".encode(encoding=ENCODING))
        sock_to_server.close()
        print("\nexit")

    