from abc import ABC,abstractmethod
import os

from app.models import Request, Response


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

class GetFileHandler(RequestHandler):
    def __init__(self, filedir: str) -> None:
        super().__init__()
        self.file_dir = filedir

    def handle(self, request: Request) -> Response:
        # if file not exists
        path_and_vars = request.path.split("/")
        filename = path_and_vars[2]
        file_path = os.path.join(self.file_dir, filename)
        if os.path.exists(file_path):
            # simple case: no streaming read full file
            content: str = ""
            with open(file_path, "r") as f:
                content = f.read()
            return Response(
                status_code=200,
                status_text="OK",
                headers={
                    "Content-Type": "application/octet-stream",
                    "Content-Length": len(content)
                },
                body=content
            )
            
        else:
            return Response(
                status_code=404,
                status_text="Not Found",
                headers={},
                body=""
            )