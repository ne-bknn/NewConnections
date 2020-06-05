from cache import FileCache
import pytest

@pytest.mark.dependency
def test_dep_networkx():
    import networkx

@pytest.mark.dependency
def test_dep_igraph():
    import igraph

@pytest.mark.dependency
def test_dep_vkapi():
    import vk_api

@pytest.mark.dependency
def test_dep_cairo():
    import cairo

@pytest.mark.smoke
def test_cache_smoke():
    c = FileCache()

@pytest.mark.sanity
def test_cache_contains_1():
    c = FileCache()
    assert c.contains("123") == False

@pytest.mark.sanity
def test_cache_contains_2():
    c = FileCache()
    c.add("123", [])
    assert c.contains("123") == True
    c.delete("123")
    assert c.contains("123") == False

@pytest.mark.sanity
def test__cache_contains_in_new_cache():
    c1 = FileCache()
    c1.add("123", [])
    assert c1.contains("123") == True
    c2 = FileCache()
    assert c2.contains("123") == True
    c1.flush()
    c2.flush()

@pytest.mark.sanity
def test_cache_get():
    c = FileCache()
    c.add("123", ["1", "2", "3"])
    assert c.get("123") == ["1", "2", "3"]
    c.delete("123")
    assert c.contains("123") == False

@pytest.mark.sanity
def test_cache_flush():
    c = FileCache()
    c.add("123", ["1", "2"])
    c.add("326", ["3", "2"])
    c.flush()
    assert c.contains("123") == False
    assert c.contains("326") == False

def get_login_password():
    with open("passwd", "r") as f:
        s = f.readlines()

    login = s[0].strip()
    passwd = s[1].strip()

    return login, passwd

@pytest.mark.sanity
def test_vk_auth():
    login, passwd = get_login_password()

    from vkwrapper import Vk

    v = Vk(cache=FileCache(), login=login, password=passwd)

    l1 = v.get_friends("525008285")
    l2 = v.get_friends("288999853")
    
    # just type checks
    assert isinstance(l1, list) and isinstance(l2, list) and isinstance(l1[0], str) and isinstance(l2[-1], str)

@pytest.mark.integration
def test_graph_creation():
    login, passwd = get_login_password()

    from vkwrapper import Vk
    from graphs import Graph

    v = Vk(cache=FileCache(), login=login, password=passwd)
    g = Graph(v, "238696131")

@pytest.mark.sanity
def test_graph_duplicating_edges():
    login, passwd = get_login_password()

    from vkwrapper import Vk
    from graphs import Graph

    v = Vk(cache=FileCache(), login=login, password=passwd)
    g = Graph(v, "238696131")

    assert g.g.is_simple() == True

@pytest.mark.smoke
def test_graph_get_community_labels():
    login, passwd = get_login_password()
    
    from vkwrapper import Vk
    from graphs import Graph

    v = Vk(cache=FileCache(), login=login, password=passwd)
    g = Graph(v, "238696131")

    g.get_community_labels()

@pytest.mark.smoke
def test__graph_get_community_labels_sparse_graph():
    login, passwd = get_login_password()

    from vkwrapper import Vk
    from graphs import Graph

    v = Vk(cache=FileCache(), login=login, password=passwd)
    g = Graph(v, "148907612")

    g.get_community_labels()

