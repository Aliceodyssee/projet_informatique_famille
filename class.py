from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
import gedcom.tags
import numpy as np
import pandas as pd
import math


class get_path() :

    def __init__(self,file_path) :
        self.ged = file_path


    def parser(self) :
        gedcom_parser = Parser()
        gedcom_parser.parse_file(self.ged)
        return gedcom_parser.get_root_child_elements()
    

    def get_IndivFamily_DataFrame(self):
        """
        Creates DataFrame of children & spouse families keys of all individuals 
        indexed by their keys, from a gedcom file.

        Parameters
        ---
        file_path : str
            path of the gedcom file

        Returns 
        ---
        pd.DataFrame 
            dataframe of children & spouse families keys of individuals
        """
        root_child_elements = self.parser()
        
        T = []
        
        #Go through indivduals and get their families
        for element in root_child_elements:
            if isinstance(element, IndividualElement):
                L = [element.get_pointer()]
                for child_element in element.get_child_elements() :
                    if child_element.get_tag() == gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE :
                        L += [child_element.get_value()]
                    elif child_element.get_tag() == gedcom.tags.GEDCOM_TAG_FAMILY_CHILD :
                        L += [child_element.get_value()]
                T += [L]

        #Add NaN where information is missing
        full_T = [line+['NaN']*(3-len(line)) for line in T]

        #Create the DataFrame
        df = pd.DataFrame(
        {
            'INDI' : [full_T[k][0] for k in range(len(full_T))],
            'FAMS' : [full_T[k][1] for k in range(len(full_T))],
            'FAMC' : [full_T[k][2] for k in range(len(full_T))],
        })

        return df
    
    
