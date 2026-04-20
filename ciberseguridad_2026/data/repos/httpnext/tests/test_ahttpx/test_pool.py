import ahttpx
import pytest


async def hello_world(request):
    content = ahttpx.Text('Hello, world.')
    return ahttpx.Response(200, content=content)


@pytest.fixture
async def server():
    async with ahttpx.Server(hello_world) as server:
        yield server


@pytest.mark.trio
async def test_connection_pool_request(server):
    async with ahttpx.ConnectionPool() as pool:
        assert repr(pool) == "<ConnectionPool [0 active]>"
        assert len(pool.connections) == 0

        r = await pool.request("GET", server.url)

        assert r.status_code == 200
        assert repr(pool) == "<ConnectionPool [0 active, 1 idle]>"
        assert len(pool.connections) == 1


@pytest.mark.trio
async def test_connection_pool_connection_close(server):
    async with ahttpx.ConnectionPool() as pool:
        assert repr(pool) == "<ConnectionPool [0 active]>"
        assert len(pool.connections) == 0

        r = await pool.request("GET", server.url, headers={"Connection": "close"})

        # TODO: Really we want closed connections proactively removed from the pool,
        assert r.status_code == 200
        assert repr(pool) == "<ConnectionPool [0 active, 1 closed]>"
        assert len(pool.connections) == 1


@pytest.mark.trio
async def test_connection_pool_stream(server):
    async with ahttpx.ConnectionPool() as pool:
        assert repr(pool) == "<ConnectionPool [0 active]>"
        assert len(pool.connections) == 0

        async with await pool.stream("GET", server.url) as r:
            assert r.status_code == 200
            assert repr(pool) == "<ConnectionPool [1 active]>"
            assert len(pool.connections) == 1
            await r.read()

        assert repr(pool) == "<ConnectionPool [0 active, 1 idle]>"
        assert len(pool.connections) == 1


@pytest.mark.trio
async def test_connection_pool_cannot_request_after_closed(server):
    async with ahttpx.ConnectionPool() as pool:
        pool

    with pytest.raises(RuntimeError):
        await pool.request("GET", server.url)


@pytest.mark.trio
async def test_connection_pool_should_have_managed_lifespan(server):
    pool = ahttpx.ConnectionPool()
    with pytest.warns(UserWarning):
        del pool


@pytest.mark.trio
async def test_connection_request(server):
    async with await ahttpx.open_connection(server.url) as conn:
        assert repr(conn) == f"<Connection [{server.url} idle]>"

        r = await conn.request("GET", "/")

        assert r.status_code == 200
        assert repr(conn) == f"<Connection [{server.url} idle]>"


@pytest.mark.trio
async def test_connection_stream(server):
    async with await ahttpx.open_connection(server.url) as conn:
        assert repr(conn) == f"<Connection [{server.url} idle]>"
        async with await conn.stream("GET", "/") as r:
            assert r.status_code == 200
            assert repr(conn) == f"<Connection [{server.url} active]>"
            await r.read()
        assert repr(conn) == f"<Connection [{server.url} idle]>"


# # with httpx.open_connection("https://www.example.com/") as conn:
# #     r = conn.request("GET", "/")

# # >>> pool = httpx.ConnectionPool()
# # >>> pool
# # <ConnectionPool [0 active]>

# # >>> with httpx.open_connection_pool() as pool:
# # >>>     res = pool.request("GET", "https://www.example.com")
# # >>>     res, pool
# # <Response [200 OK]>, <ConnectionPool [1 idle]>

# # >>> with httpx.open_connection_pool() as pool:
# # >>>     with pool.stream("GET", "https://www.example.com") as res:
# # >>>         res, pool
# # <Response [200 OK]>, <ConnectionPool [1 active]>

# # >>> with httpx.open_connection_pool() as pool:
# # >>>     req = httpx.Request("GET", "https://www.example.com")
# # >>>     with pool.send(req) as res:
# # >>>         res.body()
# # >>>     res, pool
# # <Response [200 OK]>, <ConnectionPool [1 idle]>

# # >>> with httpx.open_connection_pool() as pool:
# # >>>     pool.close()
# # <ConnectionPool [0 active]>

# # with httpx.open_connection("https://www.example.com/") as conn:
# #     with conn.upgrade("GET", "/feed", {"Upgrade": "WebSocket") as stream:
# #         ...

# # with httpx.open_connection("http://127.0.0.1:8080") as conn:
# #     with conn.upgrade("CONNECT", "www.encode.io:443") as stream:
# #         stream.start_tls(ctx, hostname="www.encode.io")
# #         ...

