import pytest
import ahttpx


@pytest.mark.trio
async def test_stream():
    i = ahttpx.Stream()
    with pytest.raises(NotImplementedError):
        await i.read()

    with pytest.raises(NotImplementedError):
        await i.close()

    i.size == None


@pytest.mark.trio
async def test_bytestream():
    data = b'abc'
    s = ahttpx.ByteStream(data)
    assert s.size == 3
    assert await s.read() == b'abc'

    s = ahttpx.ByteStream(data)
    assert await s.read(1) == b'a'
    assert await s.read(1) == b'b'
    assert await s.read(1) == b'c'
    assert await s.read(1) == b''


@pytest.mark.trio
async def test_filestream(tmp_path):
    path = tmp_path / "example.txt"
    path.write_bytes(b"hello world")

    async with ahttpx.FileStream(path) as s:
        assert s.size == 11
        assert await s.read() == b'hello world'

    async with ahttpx.FileStream(path) as s:
        assert await s.read(5) == b'hello'
        assert await s.read(5) == b' worl'
        assert await s.read(5) == b'd'
        assert await s.read(5) == b''

    async with ahttpx.FileStream(path) as s:
        assert await s.read(5) == b'hello'


@pytest.mark.trio
async def test_multipartstream(tmp_path):
    path = tmp_path / 'example.txt'
    path.write_bytes(b'hello world' + b'x' * 50)

    expected = b''.join([
        b'--boundary\r\n',
        b'Content-Disposition: form-data; name="email"\r\n',
        b'\r\n',
        b'heya@example.com\r\n',
        b'--boundary\r\n',
        b'Content-Disposition: form-data; name="upload"; filename="example.txt"\r\n',
        b'\r\n',
        b'hello world' + ( b'x' * 50) + b'\r\n',
        b'--boundary--\r\n',
    ])

    form = [('email', 'heya@example.com')]
    files = [('upload', str(path))]
    async with ahttpx.MultiPartStream(form, files, boundary='boundary') as s:
        assert s.size is None
        assert await s.read() == expected

    async with ahttpx.MultiPartStream(form, files, boundary='boundary') as s:
        assert await s.read(50) == expected[:50]
        assert await s.read(50) == expected[50:100]
        assert await s.read(50) == expected[100:150]
        assert await s.read(50) == expected[150:200]
        assert await s.read(50) == expected[200:250]

    async with ahttpx.MultiPartStream(form, files, boundary='boundary') as s:
        assert await s.read(50) == expected[:50]
        assert await s.read(50) == expected[50:100]
        assert await s.read(50) == expected[100:150]
        assert await s.read(50) == expected[150:200]
        await s.close()  # test close during open file
