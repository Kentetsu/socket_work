import socket
from http import HTTPStatus
import re


end_of_stream = '\r\n\r\n'

HOST = 'localhost'
PORT = 22222


def handle_client(connection, addr):
    client_data = ''
    headers = ""
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            client_data += data.decode()
            if end_of_stream in client_data:
                break

        info_string = re.search(r"(POST|GET|PUT|DELETE|HEAD|OPTIONS)\ \/.*\ HTTP.?\/\d\.\d", client_data)
        if info_string is not None:
            method, path, protocol = info_string.group().split()
        status_re = re.search(r"\/?status=.*[^\s]", path)
        if status_re is not None:
            status_code = status_re.group()[7:]
        else:
            status_code = "200"

        headers_match = re.findall(r"[a-zA-Z-]*:\ [a-zA-Z0-9\/. ();_:]+", client_data)
        if headers_match is not None:
            for match in headers_match:
                headers += (match + "\n" + "<br>")
        if status_code.isdigit():
            result_phrase = HTTPStatus(int(status_code)).phrase
        else:
            result_phrase = 200

        output = f"Request Method: {method} \n<br>" \
                 f"Request Source: {addr}\n<br>" \
                 f"Response Status: {status_code} {result_phrase}\n<br>" \
                 f"{headers}\n" \
                 f"\r\n"
        http_response = (
            f"HTTP/1.0 {status_code} {status_code}\r\n"
            f"Content-Type: text/html; charset=UTF-8\r\n"
            f"\r\n"
        )

        connection.send(http_response.encode()
                        + output.encode()
                        + f"\r\n".encode())


def run_server():
    with socket.socket() as serverSocket:
        serverSocket.bind((HOST, PORT))
        serverSocket.listen()
        while (True):
            (clientConnection, clientAddress) = serverSocket.accept()
            handle_client(clientConnection, clientAddress)


if __name__ == "__main__":
    run_server()
