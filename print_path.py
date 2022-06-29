# Imports
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
#from dijkstar import Graph, find_path
import gedcom.tags
import numpy as np
import pandas as pd
import math
from dijkstar import Graph, find_path
from explorer_functions import find_Element


# Parser
gedcom_parser = Parser()
file_path = 'Queen_Eliz_II.ged'
gedcom_parser = Parser()
gedcom_parser.parse_file(file_path)
root_child_elements = gedcom_parser.get_root_child_elements()


# names of family links
links = {'parents' : ('father', 'mother'), 
         'spouse' : ('husband', 'wife'),
         'sibling' : ('brother', 'sister'), 
         'grandparent' : ('grandfather', 'grandmother'),
         'grandchild' : ('grandson', 'granddaughter'), 
         'nephew' : ('nephew', 'niece'), 
         'uncle' : ('uncle', 'aunt'),
         'cousin' : ('cousin', 'cousin')

        }

def find_Element(tag):
    """
    Gets element of ged with its tag

    Parameters
    ---
    tag : str
        tag of element

    Returns 
    ---
    bool 
        Tells if the individual was found
    IndividualElement
        Element corresponding to the tag

    """
    file_path = 'Queen_Eliz_II.ged'
    gedcom_parser = Parser()
    gedcom_parser.parse_file(file_path)
    root_child_elements = gedcom_parser.get_root_child_elements()
    for element in root_child_elements:
        if element.get_tag() == tag :
            return [True, element]
    return [False, element]


def gendered_link(tag, link) :
    """
    Adds gender to family link

    Parameters
    ---
    tag : str
        tag of IndividualElement
    link : str
        family link
    Returns 
    ---
    str 
        link with gender
    """

    indvidual = find_Element(tag)
    
    if indvidual.get_gender() == "M" :
        return links[links][0]
    else :
        return links[links][1]


def print_path(path) :
    """
    Prints interprated path

    Parameters
    ---
    path : list of tuples
        path between two individuals
        tuple : (individual tag, family link)

    Returns
    ---
    int 

    """
    ind, link = path[0]
    print (v2 + "is the" + gendered_link(path[0][0], path[0][1]))
    for i in range (1, len(path)) :
        ind, link = path[i]
        print("of the" + gendered_link(ind, link))
    print ("of" + v1)

    # les print s'afficheront sûrement chacun à la ligne
    # il faut trouver une commande qui empêche ça


# Test
print_path(path[1])