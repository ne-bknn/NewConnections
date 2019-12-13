# NewConnections
Find surprising connections

# Under the hood
Under the hood we get friendlist and connections between them, find communities using [betweenness centrality](https://en.wikipedia.org/wiki/Betweenness_centrality) (or [multilevel](https://en.wikipedia.org/wiki/Multi-level_technique) for large graphs), then get set of friends of each community and find intersection. Easy as a pie!

# Current usage
In Python REPL you can just
```
from graphs import Graph

from vkwrapper import Vk

from cache import FileCache


v = Vk(cache=FileCache())

g = Graph(v, "target_id")

g.get_community_lables()

g.draw_graph()
```
