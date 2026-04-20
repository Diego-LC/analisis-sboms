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
async def server():
    async with ahttpx.Server(echo) as server:
        yield server


@pytest.mark.trio
async def test_get(server):
    r = await ahttpx.get(server.url)
    assert r.status_code == 200
    assert r.content == {
        'method': 'GET',
        'query-params': {},
        'content-type': None,
        'json': None,
    }


@pytest.mark.trio
async def test_post(server):
    data = ahttpx.JSON({"data": 123})
    r = await ahttpx.post(server.url, content=data)
    assert r.status_code == 200
    assert r.content == {
        'method': 'POST',
        'query-params': {},
        'content-type': 'application/json',
        'json': {"data": 123},
    }


@pytest.mark.trio
async def test_put(server):
    data = ahttpx.JSON({"data": 123})
    r = await ahttpx.put(server.url, content=data)
    assert r.status_code == 200
    assert r.content == {
        'method': 'PUT',
        'query-params': {},
        'content-type': 'application/json',
        'json': {"data": 123},
    }


@pytest.mark.trio
async def test_patch(server):
    data = ahttpx.JSON({"data": 123})
    r = await ahttpx.patch(server.url, content=data)
    assert r.status_code == 200
    assert r.content == {
        'method': 'PATCH',
        'query-params': {},
        'content-type': 'application/json',
        'json': {"data": 123},
    }


@pytest.mark.trio
async def test_delete(server):
    r = await ahttpx.delete(server.url)
    assert r.status_code == 200
    assert r.content == {
        'method': 'DELETE',
        'query-params': {},
        'content-type': None,
        'json': None,
    }
