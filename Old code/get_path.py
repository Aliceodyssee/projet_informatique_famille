# Imports
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
#from dijkstar import Graph, find_path
import gedcom.tags
import numpy as np
import pandas as pd
import math

# Parser
gedcom_parser = Parser()
file_path = 'Queen_Eliz_II.ged'
gedcom_parser = Parser()
gedcom_parser.parse_file(file_path)
root_child_elements = gedcom_parser.get_root_child_elements()



def shortest_path_up(graph, v1, v2) :
    """
    Updated version of shortest_path
    Includes family relationship types

    graph : 
        dictionnary which values are dictionnaries
        neighbour vertexes are family members
        separated by maximum one (or two ?) vertex
        each item is a tuple (weight, 'family relationship')
    v1, v2 : 
        IndividualElement, keys of graph

    processus the path in order to give 
    the precise link between v1 and v2

    returns tuple (distance,list of list with precise link between v1 and v2, v1 not included)
    """

    # keep track of what has been visited
    # with what distance, and from what vertex
    visited = {v1: (0, None)}
    # the edges at the border between
    # the visited and unvisited parts
    border_edges = set()
    # the vertex that was just selected
    selected_vertex = v1

    while True:
        # add to the border the edges that
        # go out of the last selected vertex
        # to unvisited
        # print(f"{selected_vertex=}")
        adj = graph.get(selected_vertex, {})
        for (dest, value) in adj.items():
            if dest not in visited:
                border_edges.add((selected_vertex, dest))
        # remove from the border any edge that would
        # end at the newly_elected vertex
        border_edges = {
            (s, d) for (s, d) in border_edges
            if d != selected_vertex
        }
        # print(f"{border_edges=}")

        # out of luck, no path can be found
        # and border_edges is empty
        if not border_edges:
            print("no edges")
            return None

        # find the best tuple (edge, distance)
        shortest_length = math.inf
        shortest_edge = None
        for (s, d) in border_edges:
            w = graph[s][d][0]
            past_distance, _ = visited[s]
            dist = past_distance + w
            if dist <= shortest_length:
                shortest_length = dist
                shortest_edge = (s, d)

        # mark newly selected vertex
        best_src, best_dst = shortest_edge
        visited[best_dst] = (shortest_length, best_src)
        selected_vertex = best_dst

        # are we done ?
        if best_dst == v2:
            # path contains the vertex and family link
            first = [best_dst, graph[best_src][best_dst][1]]
            path = [first]
            previous = best_src
            surprevious = visited[previous][1]
            while surprevious:
                # print(f"inserting {previous}")
                next = [previous, graph[surprevious][previous][1]]
                path.insert(0, next)
                previous = surprevious
                surprevious = visited[previous][1]
            return shortest_length, path