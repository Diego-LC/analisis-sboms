import types
import typing

from ._content import Content, JSON, HTML, Text, Binary, select_media
from ._headers import Headers
from ._pool import ConnectionPool, Transport
from ._request import Method, Request
from ._response import Response
from ._urls import URL

__all__ = ["Client"]


class Client:
    def __init__(
        self,
        url: URL | str | None = None,
        headers: Headers | typing.Mapping[str, str] | None = None,
        transport: Transport | None = None,
    ):
        if url is None:
            url = ""
        if headers is None:
            headers = {"User-Agent": "dev"}
        if transport is None:
            transport = ConnectionPool()

        self.url = URL(url)
        self.headers = Headers(headers)
        self.transport = transport
        self.via = RedirectMiddleware(self.transport)
        self.media = {
            'application/json': JSON,
            'text/html': HTML,
            'text/*': Text,
            '*/*': Binary,
        }

    def build_request(
        self,
        method: Method | str,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ) -> Request:
        return Request(
            method=method,
            url=self.url.join(url),
            headers=self.headers.copy_update(headers),
            content=content,
        )

    async def request(
        self,
        method: Method | str,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ) -> Response:
        request = self.build_request(method, url, headers=headers, content=content)
        async with await self.via.send(request) as stream:
            ct = stream.headers.get('Content-Type', 'application/octet-stream')
            cls = select_media(self.media, ct)
            content = await cls.parse(stream)
        return Response(
            status_code=stream.status_code,
            headers=stream.headers,
            content=content,
        )

    async def stream(
        self,
        method: Method | str,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ) -> Response:
        request = self.build_request(method, url, headers=headers, content=content)
        return await self.via.send(request)

    async def get(
        self,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
    ):
        return await self.request("GET", url, headers=headers)

    async def post(
        self,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ):
        return await self.request("POST", url, headers=headers, content=content)

    async def put(
        self,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ):
        return await self.request("PUT", url, headers=headers, content=content)

    async def patch(
        self,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
        content: Content | bytes | None = None,
    ):
        return await self.request("PATCH", url, headers=headers, content=content)

    async def delete(
        self,
        url: URL | str,
        headers: Headers | dict[str, str] | None = None,
    ):
        return await self.request("DELETE", url, headers=headers)

    async def close(self):
        await self.transport.close()

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: types.TracebackType | None = None
    ):
        await self.close()

    def __repr__(self):
        return f"<Client [{self.transport.description()}]>"


class RedirectMiddleware(Transport):
    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def build_redirect_request(self, request: Request, response: Response) -> Request | None:
        # Redirect status codes...
        if response.status_code not in (301, 302, 303, 307, 308):
            return None

        # Redirects need a valid location header...
        try:
            location = URL(response.headers['Location'])
        except (KeyError, ValueError):
            return None

        # Instantiate a redirect request...
        method = request.method
        url = request.url.join(location)
        headers = request.headers
        content = request.content

        return Request(method, url, headers, content)

    async def send(self, request: Request) -> Response:
        while True:
            response = await self._transport.send(request)

            # Determine if we have a redirect or not.
            redirect = self.build_redirect_request(request, response)

            # If we don't have a redirect, we're done.
            if redirect is None:
                return response

            # If we have a redirect, then we read the body of the response.
            # Ensures that the HTTP connection is available for a new
            # request/response cycle.
            async with response as stream:
                await stream.read()

            # Make the next request
            request = redirect

    async def close(self):
        pass
