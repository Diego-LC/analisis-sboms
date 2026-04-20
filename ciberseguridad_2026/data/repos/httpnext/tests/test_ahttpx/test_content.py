import ahttpx
import os
import tempfile
import pytest


# HTML

@pytest.mark.trio
async def test_html():
    html = ahttpx.HTML("<html><body>Hello, world</body></html>")

    assert str(html) == '<html><body>Hello, world</body></html>'
    assert bytes(html) == b'<html><body>Hello, world</body></html>'
    assert html.headers() == {
        "Content-Type": "text/html; charset='utf-8'",
        "Content-Length": "38",
    }


# Text

@pytest.mark.trio
async def test_text():
    text = ahttpx.Text("Hello, world")

    assert str(text) == 'Hello, world'
    assert bytes(text) == b'Hello, world'
    assert text.headers() == {
        "Content-Type": "text/plain; charset='utf-8'",
        "Content-Length": "12",
    }


# JSON

@pytest.mark.trio
async def test_json():
    data = ahttpx.JSON({'data': 123})

    assert bytes(data) == b'{"data":123}'
    assert data.headers() == {
        "Content-Type": "application/json",
        "Content-Length": "12",
    }


# Form

def test_form():
    f = ahttpx.Form("a=123&a=456&b=789")

    assert str(f) == "a=123&a=456&b=789"
    assert repr(f) == "<Form [('a', '123'), ('a', '456'), ('b', '789')]>"
    assert f.multi_dict() == {
        "a": ["123", "456"],
        "b": ["789"]
    }


def test_form_from_dict():
    f = ahttpx.Form({
        "a": ["123", "456"],
        "b": "789"
    })
    assert str(f) == "a=123&a=456&b=789"
    assert repr(f) == "<Form [('a', '123'), ('a', '456'), ('b', '789')]>"
    assert f.multi_dict() == {
        "a": ["123", "456"],
        "b": ["789"]
    }


def test_form_from_list():
    f = ahttpx.Form([("a", "123"), ("a", "456"), ("b", "789")])
    assert str(f) == "a=123&a=456&b=789"
    assert repr(f) == "<Form [('a', '123'), ('a', '456'), ('b', '789')]>"
    assert f.multi_dict() == {
        "a": ["123", "456"],
        "b": ["789"]
    }


def test_empty_form():
    f = ahttpx.Form()
    assert str(f) == ''
    assert repr(f) == "<Form []>"
    assert f.multi_dict() == {}


def test_form_accessors():
    f = ahttpx.Form([("a", "123"), ("a", "456"), ("b", "789")])
    assert "a" in f
    assert "A" not in f
    assert "c" not in f
    assert f["a"] == "123"
    assert f.get("a") == "123"
    assert f.get("nope", default=None) is None


def test_form_dict():
    f = ahttpx.Form([("a", "123"), ("a", "456"), ("b", "789")])
    assert list(f.keys()) == ["a", "b"]
    assert list(f.values()) == ["123", "789"]
    assert list(f.items()) == [("a", "123"), ("b", "789")]
    assert list(f) == ["a", "b"]
    assert dict(f) == {"a": "123", "b": "789"}


def test_form_multidict():
    f = ahttpx.Form([("a", "123"), ("a", "456"), ("b", "789")])
    assert f.get_list("a") == ["123", "456"]
    assert f.multi_items() == [("a", "123"), ("a", "456"), ("b", "789")]
    assert f.multi_dict() == {"a": ["123", "456"], "b": ["789"]}


def test_form_builtins():
    f = ahttpx.Form([("a", "123"), ("a", "456"), ("b", "789")])
    assert len(f) == 2
    assert bool(f)
    assert hash(f)
    assert f == ahttpx.Form([("a", "123"), ("a", "456"), ("b", "789")])


def test_form_copy_operations():
    f = ahttpx.Form([("a", "123"), ("a", "456"), ("b", "789")])
    assert f.copy_set("a", "abc") == ahttpx.Form([("a", "abc"), ("b", "789")])
    assert f.copy_append("a", "abc") == ahttpx.Form([("a", "123"), ("a", "456"), ("a", "abc"), ("b", "789")])
    assert f.copy_remove("a") == ahttpx.Form([("b", "789")])


@pytest.mark.trio
async def test_form_encode():
    form = ahttpx.Form({'email': 'address@example.com'})
    assert form['email'] == "address@example.com"

    assert bytes(form) == b"email=address%40example.com"
    assert form.headers() == {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "27",
    }


# Files

def test_files():
    f = ahttpx.Files()
    assert f.multi_dict() == {}
    assert repr(f) == "<Files []>"


def test_files_from_dict():
    f = ahttpx.Files({
        "a": [
            ahttpx.File("123.json"),
            ahttpx.File("456.json"),
        ],
        "b": ahttpx.File("789.json")
    })
    assert f.multi_dict() == {
        "a": [
            ahttpx.File("123.json"),
            ahttpx.File("456.json"),
        ],
        "b": [
            ahttpx.File("789.json"),
        ]
    }
    assert repr(f) == (
        "<Files [('a', <File '123.json'>), ('a', <File '456.json'>), ('b', <File '789.json'>)]>"
    )



def test_files_from_list():
    f = ahttpx.Files([
        ("a", ahttpx.File("123.json")),
        ("a", ahttpx.File("456.json")),
        ("b", ahttpx.File("789.json"))
    ])
    assert f.multi_dict() == {
        "a": [
            ahttpx.File("123.json"),
            ahttpx.File("456.json"),
        ],
        "b": [
            ahttpx.File("789.json"),
        ]
    }
    assert repr(f) == (
        "<Files [('a', <File '123.json'>), ('a', <File '456.json'>), ('b', <File '789.json'>)]>"
    )


def test_files_accessors():
    f = ahttpx.Files([
        ("a", ahttpx.File("123.json")),
        ("a", ahttpx.File("456.json")),
        ("b", ahttpx.File("789.json"))
    ])
    assert "a" in f
    assert "A" not in f
    assert "c" not in f
    assert f["a"] == ahttpx.File("123.json")
    assert f.get("a") == ahttpx.File("123.json")
    assert f.get("nope", default=None) is None


def test_files_dict():
    f = ahttpx.Files([
        ("a", ahttpx.File("123.json")),
        ("a", ahttpx.File("456.json")),
        ("b", ahttpx.File("789.json"))
    ])
    assert list(f.keys()) == ["a", "b"]
    assert list(f.values()) == [ahttpx.File("123.json"), ahttpx.File("789.json")]
    assert list(f.items()) == [("a", ahttpx.File("123.json")), ("b", ahttpx.File("789.json"))]
    assert list(f) == ["a", "b"]
    assert dict(f) == {"a": ahttpx.File("123.json"), "b": ahttpx.File("789.json")}


def test_files_multidict():
    f = ahttpx.Files([
        ("a", ahttpx.File("123.json")),
        ("a", ahttpx.File("456.json")),
        ("b", ahttpx.File("789.json"))
    ])
    assert f.get_list("a") == [
        ahttpx.File("123.json"),
        ahttpx.File("456.json"),
    ]
    assert f.multi_items() == [
        ("a", ahttpx.File("123.json")), 
        ("a", ahttpx.File("456.json")),
        ("b", ahttpx.File("789.json")),
    ]
    assert f.multi_dict() == {
        "a": [
            ahttpx.File("123.json"),
            ahttpx.File("456.json"),
        ],
        "b": [
            ahttpx.File("789.json"),
        ]
    }


def test_files_builtins():
    f = ahttpx.Files([
        ("a", ahttpx.File("123.json")),
        ("a", ahttpx.File("456.json")),
        ("b", ahttpx.File("789.json"))
    ])
    assert len(f) == 2
    assert bool(f)
    assert f == ahttpx.Files([
        ("a", ahttpx.File("123.json")),
        ("a", ahttpx.File("456.json")),
        ("b", ahttpx.File("789.json")),
    ])


@pytest.mark.trio
async def test_multipart():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"Hello, world")
        f.seek(0)

        multipart = ahttpx.MultiPart(
            form={'email': 'me@example.com'},
            files={'upload': ahttpx.File(f.name)},
            boundary='BOUNDARY',
        )
        assert multipart.form['email'] == "me@example.com"
        assert multipart.files['upload'] == ahttpx.File(f.name)

        fname = os.path.basename(f.name).encode('utf-8')

        assert multipart.headers() == {
            "Content-Type": "multipart/form-data; boundary=BOUNDARY",
            "Transfer-Encoding": "chunked",
        }

        stream = multipart.open()
        content = await stream.read()
        assert content == (
            b'--BOUNDARY\r\n'
            b'Content-Disposition: form-data; name="email"\r\n'
            b'\r\n'
            b'me@example.com\r\n'
            b'--BOUNDARY\r\n'
            b'Content-Disposition: form-data; name="upload"; filename="' + fname + b'"\r\n'
            b'\r\n'
            b'Hello, world\r\n'
            b'--BOUNDARY--\r\n'
        )
