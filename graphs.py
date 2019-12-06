#############################################
# An attempt to write this part without     #
# networkx, it was used just because        #
# it's usage and plotting is a bit simpler. #
# But igraph is way more powerful and       #
# convertion is just extremely ugly         #
#############################################
# Comunity expansion algo (c) ne_bknn, 2019 #
#############################################

import os

import igraph
import networkx as nx

from vkwrapper import vk

class Graph:
    #def __init__(self, vk, vk_id: str = "0") -> None:
    #    self.vk = vk
    #    nx_graph = nx.Graph()
    #    nx_graph.add_node(vk_id)
    #    friends = self.vk.get_friends(vk_id)
    #    nx_graph.add_nodes_from(friends)

    #    for friend in friends:
    #        nx_graph.add_edge(vk_id, friend)
    #        current_user_friends = vk.get_friends(friend)
    #        for current_user_friend in current_user_friends:
    #            if current_user_friend in friends:
    #                nx_graph.add_edge(friend, current_user_friend)

    #    self.nx_graph = nx_graph

    def __init__(self, vk, vk_id: str = "0") -> None:
        self.vk = vk
        target_friends = vk.get_friends(vk_id)
        ig_graph = igraph.Graph()
        ig_graph.add_vertices((vk_id))
        ig_graph.add_vertices(target_friends)
        ig_graph.add_edges([(vk_id, friend) for friend in target_friends])

        for friend in target_friends:
            current_user_friends = vk.get_friends(friend)
            # remove everyone who is not target's friend and add edges
            ig_graph.add_edges([(friend, ff) for ff in current_user_friends if ff in friends])

        self.g = ig_graph

    def get_community_labels(self) -> None:
        raise NotImplemented

    def expand_communities(self) -> None:
        raise NotImplemented

    def get_friends_per_community(self) -> None:
        raise NotImplemented

    def find_friends_intersection(self) -> None:
        raise NotImplemented

    def draw_graph(self) -> None:
        raise NotImplemented

