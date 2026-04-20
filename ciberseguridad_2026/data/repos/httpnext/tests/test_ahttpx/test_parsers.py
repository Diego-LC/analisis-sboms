import ahttpx
import pytest


class TrickleIO(ahttpx.Stream):
    def __init__(self, stream: ahttpx.Stream):
        self._stream = stream

    async def read(self, size) -> bytes:
        return await self._stream.read(1)

    async def write(self, data: bytes) -> None:
        await self._stream.write(data)
    
    async def close(self) -> None:
        await self._stream.close()


@pytest.mark.trio
async def test_parser():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 12\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"hello, world"
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"POST", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Content-Type", b"application/json"),
        (b"Content-Length", b"23"),
    ])
    await p.send_body(b'{"msg": "hello, world"}')
    await p.send_body(b'')

    assert stream.input_bytes() == (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 12\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"hello, world"
    )
    assert stream.output_bytes() == (
        b"POST / HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 23\r\n"
        b"\r\n"
        b'{"msg": "hello, world"}'
    )

    protocol, code, reason_phase = await p.recv_status_line()
    headers = await p.recv_headers()
    body = await p.recv_body()
    terminator = await p.recv_body()

    assert protocol == b'HTTP/1.1'
    assert code == 200
    assert reason_phase == b'OK'
    assert headers == [
        (b'Content-Length', b'12'),
        (b'Content-Type', b'text/plain'),
    ]
    assert body == b'hello, world'
    assert terminator == b''

    assert not p.is_idle()
    await p.complete()
    assert p.is_idle()


@pytest.mark.trio
async def test_parser_server():
    stream = ahttpx.DuplexStream(
        b"GET / HTTP/1.1\r\n"
        b"Host: www.example.com\r\n"
        b"\r\n"
    )

    p = ahttpx.HTTPParser(stream, mode='SERVER')
    method, target, protocol = await p.recv_method_line()
    headers = await p.recv_headers()
    body = await p.recv_body()

    assert method == b'GET'
    assert target == b'/'
    assert protocol == b'HTTP/1.1'
    assert headers == [
        (b'Host', b'www.example.com'),
    ]
    assert body == b''

    await p.send_status_line(b"HTTP/1.1", 200, b"OK")
    await p.send_headers([
        (b"Content-Type", b"application/json"),
        (b"Content-Length", b"23"),
    ])
    await p.send_body(b'{"msg": "hello, world"}')
    await p.send_body(b'')

    assert stream.input_bytes() == (
        b"GET / HTTP/1.1\r\n"
        b"Host: www.example.com\r\n"
        b"\r\n"
    )
    assert stream.output_bytes() == (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 23\r\n"
        b"\r\n"
        b'{"msg": "hello, world"}'
    )

    assert not p.is_idle()
    await p.complete()
    assert p.is_idle()


@pytest.mark.trio
async def test_parser_trickle():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 12\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"hello, world"
    )

    p = ahttpx.HTTPParser(TrickleIO(stream), mode='CLIENT')
    await p.send_method_line(b"POST", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Content-Type", b"application/json"),
        (b"Content-Length", b"23"),
    ])
    await p.send_body(b'{"msg": "hello, world"}')
    await p.send_body(b'')

    assert stream.input_bytes() == (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 12\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"hello, world"
    )
    assert stream.output_bytes() == (
        b"POST / HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 23\r\n"
        b"\r\n"
        b'{"msg": "hello, world"}'
    )

    protocol, code, reason_phase = await p.recv_status_line()
    headers = await p.recv_headers()
    body = await p.recv_body()
    terminator = await p.recv_body()

    assert protocol == b'HTTP/1.1'
    assert code == 200
    assert reason_phase == b'OK'
    assert headers == [
        (b'Content-Length', b'12'),
        (b'Content-Type', b'text/plain'),
    ]
    assert body == b'hello, world'
    assert terminator == b''


@pytest.mark.trio
async def test_parser_transfer_encoding_chunked():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"\r\n"
        b"c\r\n"
        b"hello, world\r\n"
        b"0\r\n\r\n"
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"POST", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Content-Type", b"application/json"),
        (b"Transfer-Encoding", b"chunked"),
    ])
    await p.send_body(b'{"msg": "hello, world"}')
    await p.send_body(b'')

    assert stream.input_bytes() == (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"\r\n"
        b"c\r\n"
        b"hello, world\r\n"
        b"0\r\n\r\n"
    )
    assert stream.output_bytes() == (
        b"POST / HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"Content-Type: application/json\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"\r\n"
        b'17\r\n'
        b'{"msg": "hello, world"}\r\n'
        b'0\r\n\r\n'
    )

    protocol, code, reason_phase = await p.recv_status_line()
    headers = await p.recv_headers()
    body = await p.recv_body()
    terminator = await p.recv_body()

    assert protocol == b'HTTP/1.1'
    assert code == 200
    assert reason_phase == b'OK'
    assert headers == [
        (b'Content-Type', b'text/plain'),
        (b'Transfer-Encoding', b'chunked'),
    ]
    assert body == b'hello, world'
    assert terminator == b''


@pytest.mark.trio
async def test_parser_transfer_encoding_chunked_trickle():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"\r\n"
        b"c\r\n"
        b"hello, world\r\n"
        b"0\r\n\r\n"
    )

    p = ahttpx.HTTPParser(TrickleIO(stream), mode='CLIENT')
    await p.send_method_line(b"POST", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Content-Type", b"application/json"),
        (b"Transfer-Encoding", b"chunked"),
    ])
    await p.send_body(b'{"msg": "hello, world"}')
    await p.send_body(b'')

    assert stream.input_bytes() == (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"\r\n"
        b"c\r\n"
        b"hello, world\r\n"
        b"0\r\n\r\n"
    )
    assert stream.output_bytes() == (
        b"POST / HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"Content-Type: application/json\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"\r\n"
        b'17\r\n'
        b'{"msg": "hello, world"}\r\n'
        b'0\r\n\r\n'
    )

    protocol, code, reason_phase = await p.recv_status_line()
    headers = await p.recv_headers()
    body = await p.recv_body()
    terminator = await p.recv_body()

    assert protocol == b'HTTP/1.1'
    assert code == 200
    assert reason_phase == b'OK'
    assert headers == [
        (b'Content-Type', b'text/plain'),
        (b'Transfer-Encoding', b'chunked'),
    ]
    assert body == b'hello, world'
    assert terminator == b''


@pytest.mark.trio
async def test_parser_repr():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 23\r\n"
        b"\r\n"
        b'{"msg": "hello, world"}'
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    assert repr(p) == "<HTTPParser [client SEND_METHOD_LINE, server WAIT]>"

    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    assert repr(p) == "<HTTPParser [client SEND_HEADERS, server RECV_STATUS_LINE]>"

    await p.send_headers([(b"Host", b"example.com")])
    assert repr(p) == "<HTTPParser [client SEND_BODY, server RECV_STATUS_LINE]>"

    await p.send_body(b'')
    assert repr(p) == "<HTTPParser [client DONE, server RECV_STATUS_LINE]>"

    await p.recv_status_line()
    assert repr(p) == "<HTTPParser [client DONE, server RECV_HEADERS]>"

    await p.recv_headers()
    assert repr(p) == "<HTTPParser [client DONE, server RECV_BODY]>"

    await p.recv_body()
    assert repr(p) == "<HTTPParser [client DONE, server RECV_BODY]>"

    await p.recv_body()
    assert repr(p) == "<HTTPParser [client DONE, server DONE]>"

    await p.complete()
    assert repr(p) == "<HTTPParser [client SEND_METHOD_LINE, server WAIT]>"


@pytest.mark.trio
async def test_parser_invalid_transitions():
    stream = ahttpx.DuplexStream()

    with pytest.raises(ahttpx.ProtocolError):
        p = ahttpx.HTTPParser(stream, mode='CLIENT')
        await p.send_method_line(b'GET', b'/', b'HTTP/1.1')
        await p.send_method_line(b'GET', b'/', b'HTTP/1.1')

    with pytest.raises(ahttpx.ProtocolError):
        p = ahttpx.HTTPParser(stream, mode='CLIENT')
        await p.send_headers([])

    with pytest.raises(ahttpx.ProtocolError):
        p = ahttpx.HTTPParser(stream, mode='CLIENT')
        await p.send_body(b'')

    with pytest.raises(ahttpx.ProtocolError):
        reader = ahttpx.ByteStream(b'HTTP/1.1 200 OK\r\n')
        p = ahttpx.HTTPParser(stream, mode='CLIENT')
        await p.recv_status_line()

    with pytest.raises(ahttpx.ProtocolError):
        p = ahttpx.HTTPParser(stream, mode='CLIENT')
        await p.recv_headers()

    with pytest.raises(ahttpx.ProtocolError):
        p = ahttpx.HTTPParser(stream, mode='CLIENT')
        await p.recv_body()


@pytest.mark.trio
async def test_parser_invalid_status_line():
    # ...
    stream = ahttpx.DuplexStream(b'...')

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([(b"Host", b"example.com")])
    await p.send_body(b'')

    msg = 'Stream closed early reading response status line'
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_status_line()

    # ...
    stream = ahttpx.DuplexStream(b'HTTP/1.1' + b'x' * 5000)

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([(b"Host", b"example.com")])
    await p.send_body(b'')

    msg = 'Exceeded maximum size reading response status line'
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_status_line()

    # ...
    stream = ahttpx.DuplexStream(b'HTTP/1.1' + b'x' * 5000 + b'\r\n')

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([(b"Host", b"example.com")])
    await p.send_body(b'')

    msg = 'Exceeded maximum size reading response status line'
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_status_line()


@pytest.mark.trio
async def test_parser_sent_unsupported_protocol():
    # Currently only HTTP/1.1 is supported.
    stream = ahttpx.DuplexStream()

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    msg = 'Sent unsupported protocol version'
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.send_method_line(b"GET", b"/", b"HTTP/1.0")


@pytest.mark.trio
async def test_parser_recv_unsupported_protocol():
    # Currently only HTTP/1.1 is supported.
    stream = ahttpx.DuplexStream(b"HTTP/1.0 200 OK\r\n")

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    msg = 'Received unsupported protocol version'
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_status_line()


@pytest.mark.trio
async def test_parser_large_body():
    body = b"x" * 6988

    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 6988\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n" + body
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([(b"Host", b"example.com")])
    await p.send_body(b'')

    # Checkout our buffer sizes.
    await p.recv_status_line()
    await p.recv_headers()
    assert len(await p.recv_body()) == 4096
    assert len(await p.recv_body()) == 2892
    assert len(await p.recv_body()) == 0

@pytest.mark.trio
async def test_parser_stream_large_body():
    body = b"x" * 6956

    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"1b2c\r\n" + body + b'\r\n0\r\n\r\n'
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([(b"Host", b"example.com")])
    await p.send_body(b'')

    # Checkout our buffer sizes.
    await p.recv_status_line()
    await p.recv_headers()
    # assert len(p.recv_body()) == 4096
    # assert len(p.recv_body()) == 2860
    assert len(await p.recv_body()) == 6956
    assert len(await p.recv_body()) == 0


@pytest.mark.trio
async def test_parser_not_enough_data_received():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 188\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"truncated"
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([(b"Host", b"example.com")])
    await p.send_body(b'')

    # Checkout our buffer sizes.
    await p.recv_status_line()
    await p.recv_headers()
    await p.recv_body()
    msg = 'Not enough data received for declared Content-Length'
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_body()


@pytest.mark.trio
async def test_parser_not_enough_data_sent():
    stream = ahttpx.DuplexStream()

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"POST", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Content-Type", b"application/json"),
        (b"Content-Length", b"23"),
    ])
    await p.send_body(b'{"msg": "too smol"}')
    msg = 'Not enough data sent for declared Content-Length'
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.send_body(b'')


@pytest.mark.trio
async def test_parser_too_much_data_sent():
    stream = ahttpx.DuplexStream()

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"POST", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Content-Type", b"application/json"),
        (b"Content-Length", b"19"),
    ])
    msg = 'Too much data sent for declared Content-Length'
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.send_body(b'{"msg": "too chonky"}')


@pytest.mark.trio
async def test_parser_missing_host_header():
    stream = ahttpx.DuplexStream()

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    msg = "Request missing 'Host' header"
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.send_headers([])


@pytest.mark.trio
async def test_client_connection_close():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 12\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"hello, world"
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Connection", b"close"),
    ])
    await p.send_body(b'')

    protocol, code, reason_phase = await p.recv_status_line()
    headers = await p.recv_headers()
    body = await p.recv_body()
    terminator = await p.recv_body()

    assert protocol == b'HTTP/1.1'
    assert code == 200
    assert reason_phase == b"OK"
    assert headers == [
        (b'Content-Length', b'12'),
        (b'Content-Type', b'text/plain'),
    ]
    assert body == b"hello, world"
    assert terminator == b""

    assert repr(p) == "<HTTPParser [client DONE, server DONE]>"

    await p.complete()
    assert repr(p) == "<HTTPParser [client CLOSED, server CLOSED]>"
    assert p.is_closed()


@pytest.mark.trio
async def test_server_connection_close():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 12\r\n"
        b"Content-Type: text/plain\r\n"
        b"Connection: close\r\n"
        b"\r\n"
        b"hello, world"
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([(b"Host", b"example.com")])
    await p.send_body(b'')

    protocol, code, reason_phase = await p.recv_status_line()
    headers = await p.recv_headers()
    body = await p.recv_body()
    terminator = await p.recv_body()

    assert protocol == b'HTTP/1.1'
    assert code == 200
    assert reason_phase == b"OK"
    assert headers == [
        (b'Content-Length', b'12'),
        (b'Content-Type', b'text/plain'),
        (b'Connection', b'close'),
    ]
    assert body == b"hello, world"
    assert terminator == b""

    assert repr(p) == "<HTTPParser [client DONE, server DONE]>"
    await p.complete()
    assert repr(p) == "<HTTPParser [client CLOSED, server CLOSED]>"


@pytest.mark.trio
async def test_invalid_status_code():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 99 OK\r\n"
        b"Content-Length: 12\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"hello, world"
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Connection", b"close"),
    ])
    await p.send_body(b'')

    msg = "Received invalid status code"
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_status_line()


@pytest.mark.trio
async def test_1xx_status_code():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 103 Early Hints\r\n"
        b"Link: </style.css>; rel=preload; as=style\r\n"
        b"Link: </script.js>; rel=preload; as=script\r\n"
        b"\r\n"
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 12\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"hello, world"
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([(b"Host", b"example.com")])
    await p.send_body(b'')

    protocol, code, reason_phase = await p.recv_status_line()
    headers = await p.recv_headers()

    assert protocol == b'HTTP/1.1'
    assert code == 103
    assert reason_phase == b'Early Hints'
    assert headers == [
        (b'Link', b'</style.css>; rel=preload; as=style'),
        (b'Link', b'</script.js>; rel=preload; as=script'),
    ]

    protocol, code, reason_phase = await p.recv_status_line()
    headers = await p.recv_headers()
    body = await p.recv_body()
    terminator = await p.recv_body()

    assert protocol == b'HTTP/1.1'
    assert code == 200
    assert reason_phase == b"OK"
    assert headers == [
        (b'Content-Length', b'12'),
        (b'Content-Type', b'text/plain'),
    ]
    assert body == b"hello, world"
    assert terminator == b""


@pytest.mark.trio
async def test_received_invalid_content_length():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: -999\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"hello, world"
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Connection", b"close"),
    ])
    await p.send_body(b'')

    await p.recv_status_line()
    msg = "Received invalid Content-Length"
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_headers()


@pytest.mark.trio
async def test_sent_invalid_content_length():
    stream = ahttpx.DuplexStream()

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    msg = "Sent invalid Content-Length"
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        # Limited to 20 digits.
        # 100 million terabytes should be enough for anyone.
        await p.send_headers([
            (b"Host", b"example.com"),
            (b"Content-Length", b"100000000000000000000"),
        ])


@pytest.mark.trio
async def test_received_invalid_characters_in_chunk_size():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"0xFF\r\n..."
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Connection", b"close"),
    ])
    await p.send_body(b'')

    await p.recv_status_line()
    await p.recv_headers()
    msg = "Received invalid chunk size"
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_body()


@pytest.mark.trio
async def test_received_oversized_chunk():
    stream = ahttpx.DuplexStream(
        b"HTTP/1.1 200 OK\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"FFFFFFFFFF\r\n..."
    )

    p = ahttpx.HTTPParser(stream, mode='CLIENT')
    await p.send_method_line(b"GET", b"/", b"HTTP/1.1")
    await p.send_headers([
        (b"Host", b"example.com"),
        (b"Connection", b"close"),
    ])
    await p.send_body(b'')

    await p.recv_status_line()
    await p.recv_headers()
    msg = "Received invalid chunk size"
    with pytest.raises(ahttpx.ProtocolError, match=msg):
        await p.recv_body()
