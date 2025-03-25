from abc import ABC,abstractmethod

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