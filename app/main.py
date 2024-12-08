import socket
import datetime


def process_request(req: bytes):
    s = req.decode()
    # <req_method> <path> <HTTPversion>\r\nHeader1: value1\r\n..\r\n\r\n
    req_data = s.split("\r\n")
    status_line = req_data[0]
    req_method, req_path, req_http_ver = status_line.split(" ")
    req_headers = req_data[1:-1]
    req_body = req_data[-1]
    
    if req_method=="GET":
        if req_path=="/":
            return b"HTTP/1.1 200 OK\r\n\r\n"
        # elif req_path.ma "/echo" TODO use pattern equivalent to "/echo/{string}"
        elif (req_path[:6]=="/echo/"):
            string = req_path.split("/")[2]
            res_headers = ["Content-Type: text/plain", f'Content-Length: {len(string)}']
            res_body = string
            res_status_line = "HTTP/1.1 200 OK"
            res: str = "\r\n".join([res_status_line, "\r\n".join(res_headers)+"\r\n", res_body])
            print("Response to send:", res)
            return res.encode()
            
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
