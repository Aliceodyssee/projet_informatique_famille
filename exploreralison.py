
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
    A dictionnary with an individual element as key, associated to the spouse and all the direct children. This forms an oriented graph. 
    There is also a bool which will later indicate if the person has already been searched.
    """

    file_path = str(file)
    gedcom_parser = Parser()
    gedcom_parser.parse_file(file_path)
    root_child_elements = gedcom_parser.get_root_child_elements()

    res = {}

    for element in root_child_elements:
        if element.get_tag() == "INDI":
            res[element] = [get_Spouse_FamilyElement(element), get_Children_FamilyElement(element), False]


    return res

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
    #print(graph)

    queue = []
    queue.append(indiv1)

    print(graph.get(indiv1))
    graph.get(indiv1)[-1] = True 


    while queue :
        current = queue.pop(0)
        if current != indiv2:
            print (current, end = " ")

            for i in graph.get(current):
                print(i)
                if graph.get(i)[-1] == False:
                        queue.append(i)
                        graph.get(i)[-1] = True


#indiv1 = find_IndividualElement("William VIII", "Gascoigne")[1]
indiv1 = '<gedcom.element.individual.IndividualElement object at 0x0000027D9F97A310>'
indiv2 = find_IndividualElement("Emma","Ramsay")[1]

#naive("Queen_Eliz_II.ged", indiv1 , indiv2)

print(indiv2.get_level())

#mon erreur vient du fait qu'il ne trouve pas les deux individus dans le fichier converti ...