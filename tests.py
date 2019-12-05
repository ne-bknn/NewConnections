from cache import FileCache

def test_contains_1():
    c = FileCache()
    assert c.contains("123") == False

def test_contains_2():
    c = FileCache()
    c.add("123", [])
    assert c.contains("123") == True
    c.delete("123")
    assert c.contains("123") == False

def test_get():
    c = FileCache()
    c.add("123", ["1", "2", "3"])
    assert c.get("123") == ["1", "2", "3"]
    c.delete("123")
    assert c.contains("123") == False

def test_flush():
    c = FileCache()
    c.add("123", ["1", "2"])
    c.add("326", ["3", "2"])
    c.flush()
    assert c.contains("123") == False
    assert c.contains("326") == False
