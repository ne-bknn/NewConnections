#############################################
# An attempt to write this part without     #
# networkx, it was used just because        #
# it's usage and plotting is a bit simpler. #
# But igraph is way more powerful and       #
# convertion was just extremely ugly        #
#############################################
# UPD: Found a way to convert between two   #
# in a simple manner. May be used for       #
# plot.ly for web end                       #
#############################################
# Comunity expansion algo (c) ne_bknn, 2019 #
#############################################

import os

import igraph
import networkx as nx

from vkwrapper import Vk

class Graph:
    def __init__(self, vk, vk_id: str) -> None:
        self.vk = vk
        target_friends = vk.get_friends(vk_id)
        ig_graph = igraph.Graph()
        ig_graph.add_vertices((vk_id))
        ig_graph.add_vertices(target_friends)
        ig_graph.add_edges([(vk_id, friend) for friend in target_friends])

        for friend in target_friends:
            current_user_friends = vk.get_friends(friend)
            # remove everyone who is not target's friend and add edges
            # filter out duplicate edges
            # KNOWN BUG: there're still duplicate edges, this needs to be sorted out
            frlist = [tuple(sorted((friend, ff))) for ff in current_user_friends if ff in target_friends]
            frlist = list(set(frlist))
            ig_graph.add_edges(frlist)
        
        # simple solution for removing multiple edges
        self.g = ig_graph.simplify()
        self.target = vk_id

    def get_community_labels(self) -> None:
        g_clean = self.g

        # 1. delete target, because target is in every community and it
        # will confuse our algo

        # with this line we try to avoid potential bugs (we could use just 0 index)
        target_index = [x.index for x in g_clean.vs if x["name"] == self.target]
        g_clean.delete_vertices(target_index)

        # 2. we will remove not connected nodes; single nodes will confuse
        # community detection algo. we will return them after 
        # community detection process
        isolates = [vertex["name"] for vertex in g_clean.vs.select(_degree=0)]
        g_clean.vs.select(_degree=0).delete()
    
        # now we have cleaned graph. cluster it
        dendrogram = g_clean.community_edge_betweenness()
        clusters = dendrogram.as_clustering()
        membership = clusters.membership
        for i in range(len(g_clean.vs)):
            g_clean.vs[i]["cluster"] = membership[i]
        
        # get isolates back
        g_clean.add_vertices([isolate for isolate in isolates])

        # get target back
        g_clean.add_vertices((self.target))

        # add nonexistent cluster to isolates and target
        for i in range(len(g_clean.vs)):
            if g_clean.vs[i]["name"] in isolates or g_clean.vs[i]["name"] == self.target:
                g_clean.vs[i]["cluster"] = -1

        # get connections back
        g_clean.add_edges([(self.target, friend["name"]) for friend in g_clean.vs if friend["name"] != self.target])
        
        # save graph
        self.g_clustered = g_clean
        self.n_clusters = len(clusters) + 1
        self.clusters = clusters

    def expand_communities(self) -> None:
        raise NotImplemented

    def get_friends_per_community(self) -> None:
        # note to myself: cluster == -1 should be checked and means that
        # this node does not belong to any cluster. important!
        raise NotImplemented

    def find_friends_intersection(self) -> None:
        raise NotImplemented

    def draw_graph(self) -> None:
        try:
            pal = igraph.drawing.colors.ClusterColoringPalette(self.n_clusters)
            g = self.g_clustered
            g.vs["color"] = pal.get_many(self.clusters.membership)
            layout = self.g_clustered.layout("fr")
            igraph.plot(self.g_clustered, layout = layout)

        except AttributeError:
            # if the clustering wasn't done yet
            layout = self.g.layout("fr")
            igraph.plot(self.g, layout = layout)

