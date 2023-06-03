import socket
import re
from http import HTTPStatus


def run_server():
    HOST = 'localhost'
    PORT = 22225
    end_of_stream = '\r\n\r\n'
    test_socket = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM
    )
    path = "/"
    method = ""
    headers = ""
    host_port = (HOST, PORT)
    test_socket.bind(host_port)
    test_socket.listen(1)
    conn, addr = test_socket.accept()
    data = conn.recv(1024)
    decode_data = data.decode("utf-8")
    info_string = re.search(r"(POST|GET|PUT|DELETE|HEAD|OPTIONS)\ \/.*\ HTTP.?\/\d\.\d", decode_data)
    if info_string is not None:
        method, path, protocol = info_string.group().split()

    if path[:9] == "/?status=":
        status_code = path[9:12]
    else:
        status_code = "200"

    headers_match = re.findall(r"[a-zA-Z-]*:\ [a-zA-Z0-9\/. ();_:]+", decode_data)
    if headers_match is not None:
        for match in headers_match:
            headers += (match + "\n" + "<br>")

    output = f"Request Method: {method} \n<br>" \
        f"Request Source: {addr}\n<br>" \
        f"Response Status: {status_code} {HTTPStatus(int(status_code)).phrase}\n<br>" \
        f"{headers}\n" \
        f"\r\n"

    response = f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><h1>{output}</h1></body></html>'
    conn.send(response.encode())
    test_socket.close()


if __name__ == "__main__":
    run_server()
