import types

from ._body import ResponseContent
from ._content import Content
from ._headers import Headers
from ._network import Lock, NetworkBackend
from ._parsers import HTTPParser
from ._response import Response
from ._request import Method, Request
from ._streams import Stream
from ._urls import URL


__all__ = [
    "Connection",
    "Transport",
    "open_connection",
]


class Transport:
    async def send(self, request: Request) -> Response:
        raise NotImplementedError()

    async def close(self):
        pass

    async def request(
        self,
        method: Method | str,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ) -> Response:
        request = Request(method, url, headers=headers, content=content)
        async with await self.send(request) as stream:
            body = await stream.read()
        return Response(stream.status_code, headers=stream.headers, content=body)

    async def stream(
        self,
        method: Method | str,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ) -> Response:
        request = Request(method, url, headers=headers, content=content)
        return await self.send(request)


class Connection(Transport):
    def __init__(self, stream: Stream, origin: URL | str):
        self._stream = stream
        self._origin = URL(origin) if not isinstance(origin, URL) else origin
        self._request_lock = Lock()
        self._parser = HTTPParser(stream, mode='CLIENT')

    # API for connection pool management...
    def origin(self) -> URL:
        return self._origin

    def is_idle(self) -> bool:
        return self._parser.is_idle()

    def is_expired(self) -> bool:
        return self._parser.is_idle() and self._parser.keepalive_expired()

    def is_closed(self) -> bool:
        return self._parser.is_closed()

    def description(self) -> str:
        return self._parser.description()

    # API entry points...
    async def send(self, request: Request) -> Response:
        #async with self._request_lock:
        #    try:
        await self._send_head(request)
        await self._send_body(request)
        code, headers = await self._recv_head()
        content = ResponseContent(self._parser)
        return Response(code, headers=headers, content=content)

    async def close(self) -> None:
        async with self._request_lock:
            await self._close()

    # Top-level API for working directly with a connection.
    async def request(
        self,
        method: Method | str,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ) -> Response:
        url = self._origin.join(url)
        request = Request(method, url, headers=headers, content=content)
        async with await self.send(request) as stream:
            body = await stream.read()
        return Response(stream.status_code, headers=stream.headers, content=body)

    async def stream(
        self,
        method: Method | str,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ) -> Response:
        url = self._origin.join(url)
        request = Request(method, url, headers=headers, content=content)
        return await self.send(request)

    # Send the request...
    async def _send_head(self, request: Request) -> None:
        method = bytes(request.method)
        target = request.url.target.encode('ascii')
        protocol = b'HTTP/1.1'
        await self._parser.send_method_line(method, target, protocol)
        headers = request.headers.as_byte_pairs()
        await self._parser.send_headers(headers)

    async def _send_body(self, request: Request) -> None:
        async with request as stream:
            while data := await stream.read(64 * 1024):
                await self._parser.send_body(data)
            await self._parser.send_body(b'')

    # Receive the response...
    async def _recv_head(self) -> tuple[int, Headers]:
        _, code, _ = await self._parser.recv_status_line()
        h = await self._parser.recv_headers()
        headers = Headers([
            (k.decode('ascii'), v.decode('ascii'))
            for k, v in h
        ])
        return code, headers

    async def _recv_body(self) -> bytes:
        return await self._parser.recv_body()

    # Request/response cycle complete...
    async def _close(self) -> None:
        await self._parser.close()

    # Builtins...
    def __repr__(self) -> str:
        return f"<Connection [{self._origin} {self.description()}]>"

    async def __aenter__(self) -> "Connection":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: types.TracebackType | None = None,
    ):
        await self.close()


async def open_connection(
        url: URL | str,
        hostname: str = '',
        backend: NetworkBackend | None = None,
    ) -> Connection:

    if isinstance(url, str):
        url = URL(url)

    if url.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be 'http://' or 'https://'.")
    if backend is None:
        backend = NetworkBackend()

    host = url.host
    port = url.port or {"http": 80, "https": 443}[url.scheme]

    if url.scheme == "https":
        stream = await backend.connect_tls(host, port, hostname)
    else:
        stream = await backend.connect(host, port)

    return Connection(stream, url)
