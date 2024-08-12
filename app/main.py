import socket

def create_response(data: bytes):
    status_line = "HTTP/1.1 200 OK"
    header = ""
    body = ""

    response = status_line + "\r\n"+header+"\r\n"+body
    return response.encode()

def process_request(client: socket.socket):
    with client:
        data = client.recv(1024)
        response = create_response(data)
        print("\nRequest: ", data) 
        print("\nResponse: ", response)
        client.send(response)

def main():
    print("Starting TCP server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("TCP server started")
    while True:
        print("\nWaiting for client request...")
        client, address = server_socket.accept() # wait for client
        process_request(client=client)


if __name__ == "__main__":
    main()
