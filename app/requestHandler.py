from abc import ABC,abstractmethod
import os
import traceback

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

class PostFileHandler(RequestHandler):
    def __init__(self, file_dir) -> None:
        super().__init__()
        self.file_dir = file_dir

    def handle(self, request: Request) -> Response:
        # validations
            # method should be post
            # path should be "files/{filename}"
            # headers should have conten-length and content-type
        
        # Main operation
        # get the filename
        try:
            filename = request.path.split("/")[-1]
            # save the body data into file
            filepath = os.path.join(self.file_dir, filename)
            content = request.body
            content_length = int(request.headers.get("Content-Length"))
            with open(filepath, 'w') as f:
                f.write(content[:content_length])
            status = 201
            status_msg = "Created"
            
        except Exception as e:
            print("Error occurred in posting file", traceback.print_exc())
            status = 500
            status_msg = "Internal Error"
        
        # send response back
        return Response(status, status_msg, {})