import socket
from typing import Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Request:
    method: str
    path: str
    http_version: str
    headers: Dict[str, str]
    body: str

@dataclass
class Response:
    status_code: int
    status_text: str
    headers: Dict[str, str]
    body: str

    def encode(self) -> bytes:
        status_line = f"HTTP/1.1 {self.status_code} {self.status_text}"
        headers = [f"{k}: {v}" for k, v in self.headers.items()]
        response = "\r\n".join([status_line, "\r\n".join(headers), "", self.body])
        return response.encode()

class RequestHandler(ABC):
    @abstractmethod
    def handle(self, request: Request) -> Response:
        pass

class EchoHandler(RequestHandler):
    def handle(self, request: Request) -> Response:
        content = request.path.split("/")[2]
        return Response(
            status_code=200,
            status_text="OK",
            headers={
                "Content-Type": "text/plain",
                "Content-Length": str(len(content))
            },
            body=content
        )

class GetUserAgentHandler(RequestHandler):
    def handle(self, request: Request) -> Response:
        content = request.headers["User-Agent"]
        return Response(
            status_code=200,
            status_text="OK",
            headers={
                "Content-Type": "text/plain",
                "Content-Length": str(len(content))
            },
            body=content
        )

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
    
    def run(self):
        print(f"Starting TCP server on {self.host}:{self.port}...")
        server_socket = socket.create_server((self.host, self.port), reuse_port=True)
        print("TCP server started")
        
        while True:
            client, address = server_socket.accept()
            with client:
                data = client.recv(1024)
                request: Request = self.parse_request(data)
                response: Response = self.router.route(request)
                client.send(response.encode())

def main():
    server = HTTPServer("localhost", 4221)
    server.router.add_route("GET", "/echo/", EchoHandler())
    server.router.add_route("GET", "/user-agent", GetUserAgentHandler())
    server.run()

if __name__ == "__main__":
    main()
