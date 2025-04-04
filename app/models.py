from dataclasses import dataclass
from typing import Dict

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
    body: str = ""

    def encode(self) -> bytes:
        status_line = f"HTTP/1.1 {self.status_code} {self.status_text}"
        headers = [f"{k}: {v}" for k, v in self.headers.items()]
        response = "\r\n".join([status_line, "\r\n".join(headers), "", self.body])
        return response.encode()
