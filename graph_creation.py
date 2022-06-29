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

"""
# Tests
print(get_IndivFamily_DataFrame().head())
df = get_IndivFamily_DataFrame()
df1 = df.set_index('INDI',inplace=False)
print(df1.at['@I11262@','FAMC'])
"""


def get_IndivLinks_DataFrame(file_path='Queen_Eliz_II.ged'):

    df = get_IndivFamily_DataFrame(file_path)

    df1 = df.set_index('INDI',inplace=False)

    df2 = pd.DataFrame(
    {
        'INDI' : df1.index,
    })
    df2['PARENT1'] = np.NaN
    df2.set_index('INDI',inplace=True)

    N_childrens_max = 0
    N_siblings_max = 0
    N_uncles_max = 0

    for indiv1 in df2.index :

        #Parents : FAMC of the character = FAMS of parents
        N_parents = 0

        for indiv2 in df[df['FAMS'] == df1.at[f'{indiv1}','FAMC']]['INDI'] :
            N_parents += 1
            df2.at[f'{indiv1}',f'PARENT{N_parents}'] = f'{indiv2}'

        #Childrens : FAMS of the character = FAMC of childrens
        N_childrens = 0

        for indiv3 in df[df['FAMC'] == df1.at[f'{indiv1}','FAMS']]['INDI'] :
            N_childrens += 1
            if N_childrens > N_childrens_max : N_childrens_max = N_childrens
            df2.at[f'{indiv1}',f'CHILD{N_childrens}'] = f'{indiv3}'

        #Siblings : FAMC of character = FAMC of siblings
        N_siblings = 0

        for indiv4 in df[df['FAMC'] == df1.at[f'{indiv1}','FAMC']]['INDI'] :
            if indiv4 != indiv1 and df1.at[f'{indiv1}','FAMC'] != 'NaN':
                N_siblings += 1
                if N_siblings > N_siblings_max : N_siblings_max = N_siblings
                df2.at[f'{indiv1}',f'SIBLING{N_siblings}'] = f'{indiv4}'

        #Spouse : FAMS of the character = FAMS of spouse
        N_spouse = 0

        for indiv6 in df[df['FAMS'] == df1.at[f'{indiv1}','FAMS']]['INDI'] :
            if indiv6 != indiv1 and df1.at[f'{indiv1}','FAMS'] != 'NaN':
                N_spouse += 1
                df2.at[f'{indiv1}',f'SPOUSE{N_spouse}'] = f'{indiv6}'


    for indiv5 in df2.index :
        
        #Grand parents : parents of the character's parents
        N_gp = 0

        for parent in df2.loc[f'{indiv5}',['PARENT1','PARENT2']] :
            if not pd.isna(parent):
                for gparent in df2.loc[f'{parent}',['PARENT1','PARENT2']] :
                    if not pd.isna(gparent):
                        N_gp += 1
                        df2.at[f'{indiv5}',f'GRAND_PARENT{N_gp}'] = f'{gparent}'
        
        #Grand child : childrens of the character's childrens
        N_gc = 0

        for child in df2.loc[f'{indiv5}',[f'CHILD{i}' for i in range(1, N_childrens_max + 1)]] :
            if not pd.isna(child):
                for gchild in df2.loc[f'{child}',[f'CHILD{j}' for j in range(1, N_childrens_max + 1)]] :
                    if not pd.isna(gchild):
                        N_gc += 1
                        df2.at[f'{indiv5}',f'GRAND_CHILD{N_gc}'] = f'{gchild}'
        
        #Nephews : childrens of the character's siblings
        N_nephews = 0

        for sibling in df2.loc[f'{indiv5}',[f'SIBLING{k}' for k in range(1, N_siblings_max + 1)]] :
            if not pd.isna(sibling):
                for child in df2.loc[f'{sibling}',[f'CHILD{l}' for l in range(1, N_childrens_max + 1)]] :
                    if not pd.isna(child):
                        N_nephews += 1
                        df2.at[f'{indiv5}',f'NEPHEW{N_nephews}'] = f'{child}'

        #Uncles & aunts : siblings of the character's parents
        N_uncles = 0

        for parent in df2.loc[f'{indiv5}',[f'PARENT{m}' for m in range(1, 3)]] :
            if not pd.isna(parent):
                for sibling in df2.loc[f'{parent}',[f'SIBLING{n}' for n in range(1, N_siblings_max + 1)]] :
                    if not pd.isna(sibling):
                        N_uncles += 1
                        if N_uncles > N_uncles_max : N_uncles_max = N_uncles
                        df2.at[f'{indiv5}',f'UNCLE{N_uncles}'] = f'{sibling}'
    

    for indiv7 in df2.index :

        #Cousins : childrens of the charcter's uncles & aunts
        N_cousin = 0

        for uncle in df2.loc[f'{indiv7}',[f'UNCLE{m}' for m in range(1, N_uncles_max + 1)]] :
            if not pd.isna(uncle) :
                for children in df2.loc[f'{uncle}', [f'CHILD{o}' for o in range(1, N_childrens_max + 1)]] :
                    if not pd.isna(children):
                        N_cousin += 1
                        df2.at[f'{indiv6}', f'COUSIN{N_cousin}'] = f'{children}'


    df2 = df2.reindex(sorted(df2.columns), axis=1)
    return df2


"""
# Tests
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', None)
print(get_IndivLinks_DataFrame().head())
"""


distances = {'parent' : 2, 
         'spouse' : 1,
         'sibling' : 2, 
         'grandparent' : 3,
         'grandchild' : 3, 
         'nephew' : 3, 
         'uncle' : 3,
         'cousin' : 3,
         'child' : 2
        }

def graph_value(col) :
    """
    Gives the correct tuple value in the graph

    Parameters 
    ---
    d : int
        distance 
    col : string
        family link

    Returns
    ---
    Couple
        (int,string)
        (distance, family link)
    
    """
    
    link = ""
    for i in range(len(str(col))-1) :
        if col[i] != "_" :
            link += col[i].lower()
    d = distances[link]
    return d,link
    


def build_IndGraph(file_path='Queen_Eliz_II.ged'):
    """
    Builds a graph in the form of a dictionnary
    
    Returns
    ---
    Dictionnary
        dictionnary of dictionnaries
        values are couples (int,string)
    """
    g = {}
    df = get_IndivLinks_DataFrame(file_path)

    for IND1 in df.index :
        g[IND1] = {}
        for column in df.columns :
            INDI2 = df.at[f'{IND1}',column]
            if not pd.isna(INDI2) :
                g[IND1][INDI2] = graph_value(column)
    return g

"""
# Test : graph creation
graph = build_IndGraph()
print(graph)
"""