import socket
from typing import Dict
import threading
from app.models import Request, Response
from app.requestHandler import EchoHandler, GetUserAgentHandler, RequestHandler


class Router:
    def __init__(self):
        self.routes: Dict[str, RequestHandler] = {}
    
    def add_route(self, method: str, path: str, handler: RequestHandler):
        self.routes[(method, path)] = handler
    
    def route(self, request: Request) -> Response:
        # Basic path matching (could be improved with regex)
        if (request.method, request.path) == ("GET", "/"):
            return Response(200, "OK", {}, "")
        
        for method_path, handler in self.routes.items():
            if (request.method==method_path[0] and request.path.startswith(method_path[1])):
                return handler.handle(request)
        
        return Response(404, "Not Found", {}, "")

class HTTPServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.router = Router()
    
    def parse_request(self, data: bytes) -> Request:
        s = data.decode()
        lines = s.split("\r\n")
        request_line = lines[0]
        method, path, http_version = request_line.split(" ")
        header_lines = lines[1:-2]
        headers = {}
        for line in header_lines:
            if line:
                key, value = line.split(": ", 1)
                headers[key] = value
        
        return Request(
            method=method,
            path=path,
            http_version=http_version,
            headers=headers,
            body=lines[-1]
        )
    
    def handle_client(self, client):
       with client:
                data = client.recv(1024)
                request: Request = self.parse_request(data)
                response: Response = self.router.route(request)
                client.send(response.encode())

    def run(self):
        print(f"Starting TCP server on {self.host}:{self.port}...")
        server_socket = socket.create_server((self.host, self.port), reuse_port=True)
        print("TCP server started")
        
        while True:
            client, address = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()
            
def main():
    server = HTTPServer("localhost", 4221)
    server.router.add_route("GET", "/echo/", EchoHandler())
    server.router.add_route("GET", "/user-agent", GetUserAgentHandler())
    server.run()

if __name__ == "__main__":
    main()
