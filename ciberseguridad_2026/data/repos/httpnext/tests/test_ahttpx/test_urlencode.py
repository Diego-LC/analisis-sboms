import ahttpx


def test_urlencode():
    qs = "a=name%40example.com&a=456&b=7+8+9&c"
    d = ahttpx.urldecode(qs)
    assert d == {
        "a": ["name@example.com", "456"],
        "b": ["7 8 9"],
        "c": [""]
    }


def test_urldecode():
    d = {
        "a": ["name@example.com", "456"],
        "b": ["7 8 9"],
        "c": [""]
    }
    qs = ahttpx.urlencode(d)
    assert qs == "a=name%40example.com&a=456&b=7+8+9&c="


def test_urlencode_empty():
    qs = ""
    d = ahttpx.urldecode(qs)
    assert d == {}


def test_urldecode_empty():
    d = {}
    qs = ahttpx.urlencode(d)
    assert qs == ""
