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


# names of family links
links = {'parent' : ('father', 'mother'), 
         'spouse' : ('husband', 'wife'),
         'sibling' : ('brother', 'sister'), 
         'grandparent' : ('grand father', 'grand mother'),
         'grandchild' : ('grand son', 'grand daughter'), 
         'nephew' : ('nephew', 'niece'), 
         'uncle' : ('uncle', 'aunt'),
         'cousin' : ('cousin', 'cousin'),
         'child' : ('son', 'daughter')

        }

def find_Element(pointer,file_path='Queen_Eliz_II.ged'):
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

    gedcom_parser = Parser()
    gedcom_parser.parse_file(file_path)
    root_child_elements = gedcom_parser.get_root_child_elements()

    for element in root_child_elements:
        if element.get_pointer() == pointer:
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

    if find_Element(tag)[0] : indvidual = find_Element(tag)[1]
    
    if indvidual.get_gender() == "M" :
        return links[link][0]
    else :
        return links[link][1]


def print_path(shortest_path,v1,v2) :
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
    distance, path = shortest_path
    ind, link = path[0]

    if find_Element(v1)[0] : element1 = find_Element(v1)[1]
    name1, surname1 = element1.get_name()

    if find_Element(v2)[0] : element2 = find_Element(v2)[1]
    name2, surname2 = element2.get_name()

    print (name2 + " is the " + gendered_link(path[0][0], path[0][1]))
    for i in range (1, len(path)) :
        ind, link = path[i]
        if i%3 == 2 :
            if find_Element(ind)[0] : element = find_Element(ind)[1]
            name, surname = element.get_name()
            print(" of " + name + ", who is the " + gendered_link(ind, link))
        else : print(" of the " + gendered_link(ind, link))
    print (" of " + name1)

    # les print s'afficheront sûrement chacun à la ligne
    # il faut trouver une commande qui empêche ça

"""
# Test
print_path(path[1])
"""