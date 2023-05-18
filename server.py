import socket
import threading

class Server():

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), 5000))
        self.bot_connected = False
        self.hunt_connected = False
        self.ss_exists = False
        self.shiny_found = False
        self.encounters = 0

    def handle_client(self, client_socket, address):
        print(f"[CONNECTION] {address}")

        connected = True
        valid = False

        while connected:
            msg = client_socket.recv(2048)
            msg = msg.decode()
            
            cmds = []
            while msg.find("SA.") != -1:
                valid = True
                cmd = msg[msg.find("SA.") + 3 : msg.find("\n")]
                print(cmd)
                cmds.append(cmd)
                msg = msg.replace("SA." + cmd + "\n", "", 1)

            if valid:
                for cmd in cmds:
                    if cmd[0] == 'b': # bot commands
                        if cmd[2:] == "connect":
                            self.bot_connected = True
                            print("[SERVER ACTION] Bot has connected.")
                        elif cmd[2:] == "status":
                            client_socket.send(str(self.bot_connected).encode())

                    if cmd[0] == 'h': # hunt commands
                        if cmd[2:] == "connect":
                            self.hunt_connected = True
                            print("[SERVER ACTION] Hunt script has connected.")
                        elif cmd[2:] == "status":
                            client_socket.send(str(self.hunt_connected).encode())

                    if cmd[0] == 'e': # encounter commands
                        if cmd[2:] == "incr":
                            self.encounters += 1
                            print(f"[SERVER ACTION] The encounters has been incremented to {self.encounters}.")
                        elif cmd[2:] == "check":
                            client_socket.send(str(self.encounters).encode())

                    if cmd[0:2] == 'sh': # shiny commands
                        if cmd[3:] == "on_screen":
                            self.shiny_found = True
                            print("[SERVER ACTION] The shiny has been found.")
                        elif cmd[3:] == "found":
                            client_socket.send(str(self.shiny_found).encode())

                    if cmd[0:2] == 'ss': # screenshot commands
                        if cmd[3:] == "exists":
                            client_socket.send(str(self.ss_exists).encode())
                        elif cmd[3:] == "add":
                            self.ss_exists = True
                            print("[SERVER ACTION] A screenshot currently exists.")
                        elif cmd[3:] == "del":
                            self.ss_exists = False
                            print("[SERVER ACTION] The screenshot has been deleted.")

                    if cmd == "disconnect":
                        print(f"[DISCONNECTION] {address} has disconnected.")
                        connected = False
            valid = False
        client_socket.close()
     
    def start(self):
        self.server.listen()
        print("[START] The server has started.")
        while True:
            client_socket, address = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        
s = Server()
s.start()