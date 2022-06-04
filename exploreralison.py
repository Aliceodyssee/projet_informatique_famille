
import numpy as np
from gedcom.element.individual import IndividualElement
from gedcom.element.element import Element
from gedcom.parser import Parser
from gedcom.element.family import FamilyElement

from ipynb.fs.full.explorertheoph import *


def convert(file):
    """
    Converts a gedcom file into a graph

    Parameters
    --
    A .ged file name

    Returns
    --
    A dictionnary with a pointer as key, associated to the spouse and all the direct children. This forms an oriented graph.
    """

    file_path = str(file)
    gedcom_parser = Parser()
    gedcom_parser.parse_file(file_path)
    root_child_elements = gedcom_parser.get_root_child_elements()

    res = {}

    for element in root_child_elements:
        if element.get_tag() == "INDI":
            res[element.get_pointer()] = [get_Spouse_FamilyElement(element), get_Children_FamilyElement(element)]


    print(res)

def naive(file, indiv1, indiv2):
    """
    BFS naive algorithm 
    
    Parameters
    --
    file :
        A gedcom file
    indiv1 :
        an individual's pointer
    indiv2 :
        an individual's pointer
    
    Returns
    --
    A list of pointers of intermidiary family members
    """

    graph = convert(file)

convert("Queen_Eliz_II.ged")