import socket
import datetime


def process_request(req: bytes):
    s = req.decode()
    # <req_method> <path> <HTTPversion>\r\nHeader1: value1\r\n..\r\n\r\n
    recv_data = s.split("\r\n\r\n")
    other = recv_data[0].split("\r\n")
    req_details = other[0]
    req_method, req_path, http_ver = req_details.split(" ")
    headers = other[1:]
    body = recv_data[1]
    
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
