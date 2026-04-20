import json
import ahttpx
import pytest


async def echo(request):
    response = ahttpx.Response(200, content=ahttpx.JSON({
        'method': str(request.method),
        'query-params': dict(request.url.params.items()),
        'content-type': request.headers.get('Content-Type'),
        'json': json.loads(request.body) if request.body else None,
    }))
    return response


@pytest.fixture
async def client():
    async with ahttpx.Client() as client:
        yield client


@pytest.fixture
async def server():
    async with ahttpx.Server(echo) as server:
        yield server


@pytest.mark.trio
async def test_client(client):
    assert repr(client) == "<Client [0 active]>"


@pytest.mark.trio
async def test_get(client, server):
    r = await client.get(server.url)
    assert r.status_code == 200
    assert r.body == b'{"method":"GET","query-params":{},"content-type":null,"json":null}'
    assert r.content == {
        "method": "GET",
        "query-params": {},
        "content-type": None,
        "json": None
    }


@pytest.mark.trio
async def test_post(client, server):
    data = ahttpx.JSON({"data": 123})
    r = await client.post(server.url, content=data)
    assert r.status_code == 200
    assert r.content == {
        'method': 'POST',
        'query-params': {},
        'content-type': 'application/json',
        'json': {"data": 123},
    }


@pytest.mark.trio
async def test_put(client, server):
    data = ahttpx.JSON({"data": 123})
    r = await client.put(server.url, content=data)
    assert r.status_code == 200
    assert r.content == {
        'method': 'PUT',
        'query-params': {},
        'content-type': 'application/json',
        'json': {"data": 123},
    }


@pytest.mark.trio
async def test_patch(client, server):
    data = ahttpx.JSON({"data": 123})
    r = await client.patch(server.url, content=data)
    assert r.status_code == 200
    assert r.content == {
        'method': 'PATCH',
        'query-params': {},
        'content-type': 'application/json',
        'json': {"data": 123},
    }


@pytest.mark.trio
async def test_delete(client, server):
    r = await client.delete(server.url)
    assert r.status_code == 200
    assert r.content == {
        'method': 'DELETE',
        'query-params': {},
        'content-type': None,
        'json': None,
    }


@pytest.mark.trio
async def test_request(client, server):
    r = await client.request("GET", server.url)
    assert r.status_code == 200
    assert r.content == {
        'method': 'GET',
        'query-params': {},
        'content-type': None,
        'json': None,
    }


@pytest.mark.trio
async def test_stream(client, server):
    async with await client.stream("GET", server.url) as r:
        assert r.status_code == 200
        body = await r.read()
        assert json.loads(body) == {
            'method': 'GET',
            'query-params': {},
            'content-type': None,
            'json': None,
        }


@pytest.mark.trio
async def test_get_with_invalid_scheme(client):
    with pytest.raises(ValueError):
        await client.get("nope://www.example.com")
