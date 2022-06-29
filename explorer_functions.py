from gedcom.element.individual import IndividualElement
from gedcom.element.element import Element
from gedcom.parser import Parser
from gedcom.element.family import FamilyElement
import gedcom.tags
import numpy as np
import pandas as pd
import string
#from gedcom.element.element import Element
#from gedcom.element.file import FileElement
#from gedcom.element.object import ObjectElement

gedcom_parser = Parser()

file_path = 'Queen_Eliz_II.ged'
gedcom_parser = Parser()
gedcom_parser.parse_file(file_path)
root_child_elements = gedcom_parser.get_root_child_elements()

def find_child_data(first_names,last_name):
    for element in root_child_elements:
        if isinstance(element, IndividualElement):
            if element.surname_match(last_name):
                if element.given_name_match(first_names):
                    L1 = []
                    L2 = []
                    (first, last) = element.get_name()
                    print("Information about " + first + " " + last + ":")
                    data = element.get_child_elements()
                    for child in data :
                        L1 += [child]
                        L2 += [child.get_tag()]
                    return L1, L2
    return "No matching person"

# Test
print(find_child_data("Elizabeth II Alexandra Mary", "Windsor"))



def find_IndividualElement(first_names,last_name):
    """
    Get Individual element of ged with first names and last name

    Parameters
    ---
    first_names : str
        complete first names of the individual
    last_name : str
        last names of the individual 

    Returns 
    ---
    bool 
        Tells if the individual was found
    IndividualElement
        IndividualElement corresponding to the individual in the ged

    """
    for element in root_child_elements:
        if isinstance(element, IndividualElement):
            if element.surname_match(last_name):
                return (True, element)
    return [False, element]



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
    for element in root_child_elements:
        if element.get_tag() == tag :
            return [True, element]
    return [False, element]


def get_Spouse_FamilyElement(Individual):
    """
    Get Spouse FamilyElements of an individual

    Parameters
    ---
    Individual : IndividualElement

    Returns
    ---
    list of FamilyElement 
    """
    return gedcom_parser.get_families(Individual,"FAMS")
    


def get_Children_FamilyElement(Individual):
    """
    Get Childrens FamilyElements of an individual

    Parameters
    ---
    Individual : IndividualElement

    Returns
    ---
    list of FamilyElement 
    """
    return gedcom_parser.get_families(Individual,"FAMC")



def get_spouse(Individual):
    """
    Doesn't work
    """
    Family = get_Spouse_FamilyElement(Individual)[0]
    return gedcom_parser.get_family_members(Family,"FAMILY_MEMBERS_TYPE_ALL")


def get_all_Spouse_FamilyElement():
    Spouse_FamilyElements = []
    N = 0
    for element in root_child_elements:
        if isinstance(element, FamilyElement):
            if element.get_tag() == gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE :
                Spouse_FamilyElements += [element]
    return Spouse_FamilyElements


def get_IndivFamily_DataFrame(file_path='Queen_Eliz_II.ged'):
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
    gedcom_parser.parse_file(file_path)
    root_child_elements = gedcom_parser.get_root_child_elements()
    
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


def get_FamChildrens_DataFrame(df):
    """
    """
    df1 = df.set_index('INDI',inplace=False)

    df2 = pd.DataFrame(
    {
        'FAM' : df['FAMS'].drop_duplicates(),
    })
    df2['1FAMC'] = np.NaN
    df2.set_index('FAM',inplace=True)
    N_max = 1

    for family in df2.index :
        N = 0
        for indi in df[df['FAMC'] == f'{family}']['INDI'] :
            N += 1
            if N > N_max :
                N_max = N
                df2[f'{N_max}FAMC'] = np.NaN
            #df2.at[f'{family}',f'{N}FAMC'] = f'{indi}'
            df2.at[f'{family}',f'{N}FAMC'] = df1.at[f'{indi}','FAMS']
    return df2




def get_FamSpouse_DataFrame(df):
    """
    """
    df1 = df.set_index('INDI',inplace=False)

    df2 = pd.DataFrame(
    {
        'FAM' : df['FAMS'].drop_duplicates(),
    })
    df2['1FAMS'] = np.NaN
    df2.set_index('FAM',inplace=True)
    N_max = 1

    for family in df2.index :
        N = 0
        for indi in df[df['FAMS'] == f'{family}']['INDI'] :
            N += 1
            if N > N_max :
                N_max = N
                df2[f'{N_max}FAMS'] = np.NaN
            #df2.at[f'{family}',f'{N}'] = f'{indi}'
            df2.at[f'{family}',f'{N}FAMS'] = df1.at[f'{indi}','FAMC']
    return df2


def get_FamLinks_DataFrame():
    df = get_IndivFamily_DataFrame()
    df3 = pd.concat([get_FamSpouse_DataFrame(df),get_FamChildrens_DataFrame(df)],axis=1)
    return df3
