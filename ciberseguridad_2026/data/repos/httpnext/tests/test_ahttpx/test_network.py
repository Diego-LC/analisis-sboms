import ahttpx
import pytest


async def echo(stream):
    while buffer := await stream.read():
        await stream.write(buffer)


@pytest.fixture
async def server():
    net = ahttpx.NetworkBackend()
    async with await net.serve("127.0.0.1", 8080, echo) as server:
        yield server


def test_network_backend():
    net = ahttpx.NetworkBackend()
    assert repr(net) in ["<NetworkBackend [trio]>", "<NetworkBackend [threaded]>"]


@pytest.mark.trio
async def test_network_backend_connect(server):
    net = ahttpx.NetworkBackend()
    stream = await net.connect(server.host, server.port)
    try:
        assert repr(stream) == f"<NetworkStream [{server.host}:{server.port}]>"
        await stream.write(b"Hello, world.")
        content = await stream.read()
        assert content == b"Hello, world."
    finally:
        await stream.close()


@pytest.mark.trio
async def test_network_backend_context_managed(server):
    net = ahttpx.NetworkBackend()
    async with await net.connect(server.host, server.port) as stream:
        await stream.write(b"Hello, world.")
        content = await stream.read()
        assert content == b"Hello, world."
    assert repr(stream) == f"<NetworkStream [{server.host}:{server.port} CLOSED]>"


@pytest.mark.trio
async def test_network_backend_timeout(server):
    net = ahttpx.NetworkBackend()
    with ahttpx.timeout(0.0):
        with pytest.raises(TimeoutError):
            async with await net.connect(server.host, server.port) as stream:
                pass

    with ahttpx.timeout(10.0):
        async with await net.connect(server.host, server.port) as stream:
            pass


# >>> net = httpx.NetworkBackend()
# >>> stream = net.connect("dev.encode.io", 80)
# >>> try:
# >>>     ...
# >>> finally:
# >>>     stream.close()
# >>> stream
# <NetworkStream ["168.0.0.1:80" CLOSED]>

# import httpx
# import ssl
# import truststore

# net = httpx.NetworkBackend()
# ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# req = b'\r\n'.join([
#     b'GET / HTTP/1.1',
#     b'Host: www.example.com',
#     b'User-Agent: python/dev',
#     b'Connection: close',
#     b'',
# ])

# # Use a 10 second overall timeout for the entire request/response.
# with timeout(10.0):
#     # Use a 3 second timeout for the initial connection.
#     with timeout(3.0) as t:
#         # Open the connection & establish SSL.
#         with net.open_stream("www.example.com", 443) as stream:
#             stream.start_tls(ctx, hostname="www.example.com")
#             t.cancel()
#             # Send the request & read the response.
#             stream.write(req)
#             buffer = []
#             while part := stream.read():
#                 buffer.append(part)
#             resp = b''.join(buffer)


# def test_fixture(tcp_echo_server):
#     host, port = (tcp_echo_server.host, tcp_echo_server.port)

#     net = httpx.NetworkBackend()
#     with net.connect(host, port) as stream:
#         stream.write(b"123")
#         buffer = stream.read()
#         assert buffer == b"123"
