from datetime import datetime
import socket
import threading

class Server():

    def __init__(self, exit_event):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), 5000))
        self.bot_connected = False
        self.hunt_connected = False
        self.ss_exists = False
        self.shiny_found = "False"
        self.hunt = ""
        self.game = ""
        self.method = ""
        self.encounters = 0
        self.phase = 0
        now = datetime.now()
        self.start_date = str(now.date())
        self.start_time = str(now.strftime("%H:%M"))
        self.find_date = ""
        self.find_time = ""
        self.connections = []
        self.exit_event = exit_event

    def generate_log_file(self):
        file = open(f"{self.hunt}.hunt", 'w')
        file.write("---SHINE.AI Shiny Hunt Log---\n")
        file.write(f"Hunt: {self.hunt}\n")
        file.write(f"Game: {self.game}\n")
        file.write(f"Method: {self.method}\n")
        file.write(f"Encounters: {self.encounters}\n")
        file.write(f"Phase: {self.phase}\n")
        file.write(f"Start Date: {self.start_date}\n")
        file.write(f"Start Time: {self.start_time}\n")
        if self.shiny_found:
            file.write(f"Shiny found on {self.find_date} at {self.find_time}")
        else:
            file.write("Shiny has not been found")
        file.close()

    def reset_data(self):
        self.bot_connected = False
        self.hunt_connected = False
        self.ss_exists = False
        self.shiny_found = "False"
        self.hunt = ""
        self.game = ""
        self.method = ""
        self.encounters = 0
        self.phase = 0
        now = datetime.now()
        self.start_date = str(now.date())
        self.start_time = str(now.strftime("%H:%M"))
        self.find_date = ""
        self.find_time = ""

    def handle_client(self, client_socket, address):
        print(f"[CONNECTION] {address}")

        connected = True
        valid = False

        while connected:
            try:
                msg = client_socket.recv(2048)
                msg = msg.decode()
            except ConnectionResetError:
                return
            
            cmds = []
            while msg.find("SA.") != -1:
                valid = True
                cmd = msg[msg.find("SA.") + 3 : msg.find("\n")]
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
                            self.shiny_found = "Found"
                            now = datetime.now()
                            self.find_date = str(now.date())
                            self.find_time = str(now.strftime("%H:%M"))
                            print("[SERVER ACTION] The shiny has been found.")
                        elif cmd[3:] == "found":
                            client_socket.send(self.shiny_found.encode())

                    if cmd[0:2] == 'ss': # screenshot commands
                        if cmd[3:] == "exists":
                            client_socket.send(str(self.ss_exists).encode())
                        elif cmd[3:] == "add":
                            self.ss_exists = True
                            print("[SERVER ACTION] A screenshot currently exists.")
                        elif cmd[3:] == "del":
                            self.ss_exists = False
                            print("[SERVER ACTION] The screenshot has been processed.")

                    if cmd[0:4] == 'util': # utility commands
                        if cmd.find('hunt') != -1:
                            self.hunt = cmd[cmd.find(' ') + 1:]
                            print(f"[SERVER ACTION] Hunt has been set to {self.hunt}")
                        elif cmd.find('game') != -1:
                            self.game = cmd[cmd.find(' ') + 1:]
                            print(f"[SERVER ACTION] Game has been set to {self.game}")
                        elif cmd.find('method') != -1:
                            self.method = cmd[cmd.find(' ') + 1:]
                            print(f"[SERVER ACTION] Method has been set to {self.method}")
                        elif cmd.find('encounters') != -1:
                            self.encounters = int(cmd[cmd.find(' ') + 1:])
                            print(f"[SERVER ACTION] Encounters has been set to {self.encounters}")
                        elif cmd.find('phase') != -1:
                            self.phase = int(cmd[cmd.find(' ') + 1:])
                            print(f"[SERVER ACTION] Phase has been set to {self.phase}")
                        elif cmd.find('reset') != -1:
                            self.reset_data()
                            print(f"[SERVER ACTION] The server data has been reset to its intial values.")
                        elif cmd[5:] == "log":
                            self.generate_log_file()
                            print(f"[SERVER ACTION] A log file was generated.")
                        elif cmd[5:] == "disconnect":
                            print(f"[DISCONNECTION] {address} has disconnected.")
                            connected = False

            valid = False
        client_socket.close()
     
    def start(self):
        self.server.listen()
        print("[START] The server has started.")
        while True:
            if len(self.connections) != 2:
                client_socket, address = self.server.accept()
                self.connections.append(client_socket)
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {len(self.connections)}")
            else:
                if self.exit_event.is_set():
                    exit()

def run_server(exit_event):  
    s = Server(exit_event)
    s.start()