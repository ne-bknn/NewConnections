from cache import FileCache

def test_networkx():
    import networkx

def test_igraph():
    import igraph

def test_vkapi():
    import vk_api

def test_cairo():
    import cairo

def test_contains_1():
    c = FileCache()
    assert c.contains("123") == False

def test_contains_2():
    c = FileCache()
    c.add("123", [])
    assert c.contains("123") == True
    c.delete("123")
    assert c.contains("123") == False

def test_contains_in_new_cache():
    c1 = FileCache()
    c1.add("123", [])
    assert c1.contains("123") == True
    c2 = FileCache()
    assert c2.contains("123") == True
    c1.flush()
    c2.flush()

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

def test_auth():
    with open("passwd", "r") as f:
        s = f.readlines()

    login = s[0].strip()
    passwd = s[1].strip()
    
    # checks whether creds are valid
    assert login.endswith("2")

    from vkwrapper import Vk

    v = Vk(cache=FileCache(), login=login, password=passwd)

    l1 = v.get_friends("525008285")
    l2 = v.get_friends("288999853")
    
    # just type checks
    assert isinstance(l1, list) and isinstance(l2, list) and isinstance(l1[0], str) and isinstance(l2[-1], str)

def test_graph_creation():
    with open("passwd", "r") as f:
        s = f.readlines()

    login = s[0].strip()
    passwd = s[1].strip()

    assert login.endswith("2")

    from vkwrapper import Vk
    from graphs import Graph

    v = Vk(cache=FileCache(), login=login, password=passwd)
    g = Graph(v)

