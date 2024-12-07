import socket
import datetime


def process_request(req: bytes):
    s = req.decode()
    # <req_method> <path> <HTTPversion>\r\nHeader1: value1\r\n..\r\n\r\n
    req_data = s.split("\r\n")
    req_method, req_path, req_http_ver = req_data[0].split(" ")
    req_headers = req_data[1:-1]
    req_body = req_data[-1]
    
    if req_method=="GET":
        if req_path=="/":
            return b"HTTP/1.1 200 OK\r\n\r\n"
        else:
            return b"HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        return b"HTTP/1.1 404 Not Found\r\n\r\n"


def main():
    print("Starting TCP server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("TCP server started")
    while True:
        print("\nWait for client request...")
        client, address = server_socket.accept()
        with client:
            print("Request received")
            print("Client address:", address)
            data = client.recv(1024)
            print("Client data:", data)
            res = process_request(data)
            client.send(res)


if __name__ == "__main__":
    main()
