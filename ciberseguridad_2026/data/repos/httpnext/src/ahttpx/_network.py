import ssl
import types
import typing

import trio
import truststore

from ._streams import Stream


__all__ = ["NetworkBackend", "NetworkStream", "timeout"]


class NetworkStream(Stream):
    def __init__(
        self, trio_stream: trio.abc.Stream, address: str = ''
    ) -> None:
        self._trio_stream = trio_stream
        self._address = address
        self._closed = False

    async def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = 64 * 1024
        return await self._trio_stream.receive_some(size)

    async def write(self, buffer: bytes) -> None:
        await self._trio_stream.send_all(buffer)

    async def close(self) -> None:
        # Close the NetworkStream.
        # If the stream is already closed this is a checkpointed no-op.
        try:
            await self._trio_stream.aclose()
        finally:
            self._closed = True

    def __repr__(self):
        description = ""
        description += " CLOSED" if self._closed else ""
        return f"<NetworkStream [{self._address}{description}]>"

    def __del__(self):
        if not self._closed:
            import warnings
            warnings.warn(f"{self!r} was garbage collected without being closed.")

    # Context managed usage...
    async def __aenter__(self) -> "NetworkStream":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: types.TracebackType | None = None,
    ):
        await self.close()


class NetworkServer:
    def __init__(self, host: str, port: int, handler, listeners: list[trio.SocketListener]):
        self.host = host
        self.port = port
        self._handler = handler
        self._listeners = listeners

    # Context managed usage...
    async def __aenter__(self) -> "NetworkServer":
        self._nursery_manager = trio.open_nursery()
        self._nursery = await self._nursery_manager.__aenter__()
        self._nursery.start_soon(trio.serve_listeners, self._handler, self._listeners)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: types.TracebackType | None = None,
    ):
        self._nursery.cancel_scope.cancel()
        await self._nursery_manager.__aexit__(exc_type, exc_value, traceback)


class NetworkBackend:
    def __init__(self, ssl_ctx: ssl.SSLContext | None = None):
        self._ssl_ctx = self.create_default_context() if ssl_ctx is None else ssl_ctx

    def create_default_context(self) -> ssl.SSLContext:
        return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    async def connect(self, host: str, port: int) -> NetworkStream:
        """
        Connect to the given address, returning a Stream instance.
        """
        # Create the TCP stream
        address = f"{host}:{port}"
        trio_stream = await trio.open_tcp_stream(host, port)
        return NetworkStream(trio_stream, address=address)

    async def connect_tls(self, host: str, port: int, hostname: str = '') -> NetworkStream:
        """
        Connect to the given address, returning a Stream instance.
        """
        # Create the TCP stream
        address = f"{host}:{port}"
        trio_stream = await trio.open_tcp_stream(host, port)

        # Establish SSL over TCP
        hostname = hostname or host
        ssl_stream = trio.SSLStream(trio_stream, ssl_context=self._ssl_ctx, server_hostname=hostname)
        await ssl_stream.do_handshake()

        return NetworkStream(ssl_stream, address=address)

    async def serve(self, host: str, port: int, handler: typing.Callable[[NetworkStream], None]) -> NetworkServer:
        async def callback(trio_stream):
            stream = NetworkStream(trio_stream, address=f"{host}:{port}")
            try:
                await handler(stream)
            finally:
                await stream.close()

        listeners = await trio.open_tcp_listeners(port=port, host=host)
        return NetworkServer(host, port, callback, listeners)

    def __repr__(self):
        return f"<NetworkBackend [trio]>"


Semaphore = trio.Semaphore
Lock = trio.Lock
timeout = trio.move_on_after
sleep = trio.sleep
