# Imports
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
#from dijkstar import Graph, find_path
import gedcom.tags
import numpy as np
import pandas as pd
import math
from dijkstar import Graph, find_path

# Parser
gedcom_parser = Parser()
file_path = 'Queen_Eliz_II.ged'
gedcom_parser = Parser()
gedcom_parser.parse_file(file_path)
root_child_elements = gedcom_parser.get_root_child_elements()

# dijk_search(graph, v1,v2)

# creation of Graph() object

def make_graph_dijkstar(graph) :
    new_graph = Graph()
    for 
