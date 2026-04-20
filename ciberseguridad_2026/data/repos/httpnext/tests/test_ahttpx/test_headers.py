import ahttpx
import pytest


def test_headers_from_dict():
    headers = ahttpx.Headers({
        'Content-Length': '1024',
        'Content-Type': 'text/plain; charset=utf-8',
    })
    assert headers['Content-Length'] == '1024'
    assert headers['Content-Type'] == 'text/plain; charset=utf-8'


def test_headers_from_list():
    headers = ahttpx.Headers([
        ('Location', 'https://www.example.com'),
        ('Set-Cookie', 'session_id=3498jj489jhb98jn'),
    ])
    assert headers['Location'] == 'https://www.example.com'
    assert headers['Set-Cookie'] == 'session_id=3498jj489jhb98jn'


def test_header_keys():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert list(h.keys()) == ["Accept", "User-Agent"]


def test_header_values():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert list(h.values()) == ["*/*", "python/httpx"]


def test_header_items():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert list(h.items()) == [("Accept", "*/*"), ("User-Agent", "python/httpx")]


def test_header_get():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert h.get("User-Agent") == "python/httpx"
    assert h.get("user-agent") == "python/httpx"
    assert h.get("missing") is None


def test_header_copy_set():
    h = ahttpx.Headers({"Expires": "0"})
    h = h.copy_set("Expires", "Wed, 21 Oct 2015 07:28:00 GMT")
    assert h == ahttpx.Headers({"Expires": "Wed, 21 Oct 2015 07:28:00 GMT"})

    h = ahttpx.Headers({"Expires": "0"})
    h = h.copy_set("expires", "Wed, 21 Oct 2015 07:28:00 GMT")
    assert h == ahttpx.Headers({"Expires": "Wed, 21 Oct 2015 07:28:00 GMT"})


def test_header_copy_remove():
    h = ahttpx.Headers({"Accept": "*/*"})
    h = h.copy_remove("Accept")
    assert h == ahttpx.Headers({})

    h = ahttpx.Headers({"Accept": "*/*"})
    h = h.copy_remove("accept")
    assert h == ahttpx.Headers({})


def test_header_getitem():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert h["User-Agent"] == "python/httpx"
    assert h["user-agent"] == "python/httpx"
    with pytest.raises(KeyError):
        h["missing"]


def test_header_contains():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert "User-Agent" in h
    assert "user-agent" in h
    assert "missing" not in h


def test_header_bool():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert bool(h)
    h = ahttpx.Headers()
    assert not bool(h)


def test_header_iter():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert [k for k in h] == ["Accept", "User-Agent"]


def test_header_len():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert len(h) == 2


def test_header_repr():
    h = ahttpx.Headers({"Accept": "*/*", "User-Agent": "python/httpx"})
    assert repr(h) == "<Headers {'Accept': '*/*', 'User-Agent': 'python/httpx'}>"


def test_header_invalid_name():
    with pytest.raises(ValueError):
        ahttpx.Headers({"Accept\n": "*/*"})


def test_header_invalid_value():
    with pytest.raises(ValueError):
        ahttpx.Headers({"Accept": "*/*\n"})
