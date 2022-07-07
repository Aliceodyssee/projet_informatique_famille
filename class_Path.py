from class_Graph import *
import time

class Path() :

    def __init__(self, file_path) :

        self.ged = file_path

        self.get_graph = Graph(self.ged)

        self.graph = self.get_graph.build()

        self.links = {'parent' : ('father', 'mother'), 
         'spouse' : ('husband', 'wife'),
         'sibling' : ('brother', 'sister'), 
         'grandparent' : ('grand father', 'grand mother'),
         'grandchild' : ('grand son', 'grand daughter'), 
         'nephew' : ('nephew', 'niece'), 
         'uncle' : ('uncle', 'aunt'),
         'cousin' : ('cousin', 'cousin'),
         'child' : ('son', 'daughter')
        }


    def shortest_path(self, v1, v2) :
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
            adj = self.graph.get(selected_vertex, {})
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
                w = self.graph[s][d][0]
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
                first = [best_dst, self.graph[best_src][best_dst][1]]
                path = [first]
                previous = best_src
                surprevious = visited[previous][1]
                while surprevious:
                    # print(f"inserting {previous}")
                    next = [previous, self.graph[surprevious][previous][1]]
                    path.insert(0, next)
                    previous = surprevious
                    surprevious = visited[previous][1]
                return shortest_length, path
    


    def find_Element(self,pointer):
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
        for element in self.get_graph.parser():
            if element.get_pointer() == pointer:
                return [True, element]
        return [False, element]


    
    def gendered_link(self,tag,link) :
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

        if self.find_Element(tag)[0] : 
            indvidual = self.find_Element(tag)[1]
        
        if indvidual.get_gender() == "M" :
            return self.links[link][0]
        else :
            return self.links[link][1]

    
    def print_table(self,v1,v2):
        shortest_path = self.shortest_path(v1,v2)
        if shortest_path == None : 
            return 'No path'
        _, path = shortest_path

        individuals = []
        links = []
        for i in range (len(path)):
            ind, _ = path[i]
            if self.find_Element(ind)[0] : 
                element = self.find_Element(ind)[1]
                name, surname = element.get_name()
                individuals.append(name + ' ' + surname)

                links.append(path.gendered_link(element, path[i][1]))
        
        df = pd.DataFrame({
            "Name" : individuals,
            "Family link" : links
        })
        df.set_index('Name',inplace=True)
        return df


    def print(self,v1,v2) :
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

        shortest_path = self.shortest_path(v1,v2)
        if shortest_path == None : return 'No path'
        _, path = shortest_path
        ind, link = path[0]

        if self.find_Element(v1)[0] : element1 = self.find_Element(v1)[1]
        name1, surname1 = element1.get_name()

        if self.find_Element(v2)[0] : element2 = self.find_Element(v2)[1]
        name2, surname2 = element2.get_name()

        print (name2 + surname2 + " is the " + self.gendered_link(path[0][0], path[0][1]))
        for i in range (1, len(path)) :
            ind, link = path[i]
            if i%3 == 2 :
                if self.find_Element(ind)[0] : element = self.find_Element(ind)[1]
                name, surname = element.get_name()
                print(" of " + name + surname + ", who is the " + self.gendered_link(ind, link))
            else : print(" of the " + self.gendered_link(ind, link))
        print (" of " + name1 + surname1)


    def get(self,v1,v2) :
        """
        Returns interprated path

        Parameters
        ---
        v1 : IndividualElement
        v2 : IndividualElement

        Returns
        ---
         

        """
        path_detail = ""
        shortest_path = self.shortest_path(v1,v2)
        if shortest_path == None : return None
        length, path = shortest_path

        if self.find_Element(v1)[0] : element1 = self.find_Element(v1)[1]
        name1, _ = element1.get_name()

        if self.find_Element(v2)[0] : element2 = self.find_Element(v2)[1]
        name2, _ = element2.get_name()

        path_detail += name2 + " is the " + self.gendered_link(path[0][0], path[0][1])
        for i in range (1,len(path)) :
            [ind1, link1] = path[i]
            if i == 0 :
                ind2 = v2
            else :
                [ind2, _] = path[i-1]
            
            if i%3 == 2 :
                if self.find_Element(ind1)[0] : element = self.find_Element(ind1)[1]
                name, _ = element.get_name()
                path_detail += " of " + name + ", who is the " + self.gendered_link(ind2, link1)
                
            else : path_detail += " of the " + self.gendered_link(ind2, link1)
        path_detail += " of " + name1 + "."
        return [length,path_detail]

        

    def get_dij(self,v1,v2) :
            """
            Returns interprated path

            Parameters
            ---
            path : list of tuples
                path between two individuals
                tuple : (individual tag, family link)

            Returns
            ---
            int 

            """
            #begin = time.time()
            path_detail = ""
            dij_path, _,_,length = find_path(self.get_graph.build_dij(),v1,v2)
            path = copy.deepcopy(dij_path)
            for i in range(1,len(path)) :
                _ ,link = self.graph[dij_path[i-1]][dij_path[i]]
                path[i] = [dij_path[i], link]
            path.pop(0)
            #end = time.time()
            #print(end-begin)

            if self.find_Element(v1)[0] : element1 = self.find_Element(v1)[1]
            name1, _ = element1.get_name()

            if self.find_Element(v2)[0] : element2 = self.find_Element(v2)[1]
            name2, _ = element2.get_name()

            path_detail += name2 + " is the " + self.gendered_link(path[0][0], path[0][1])
            for i in range (1,len(path)) :
                [ind1, link1] = path[i]
                [ind2, _] = path[i-1]
                if i%3 == 2 :
                    if self.find_Element(ind1)[0] : element = self.find_Element(ind1)[1]
                    name, _ = element.get_name()
                    path_detail += " of " + name + ", who is the " + self.gendered_link(ind2, link1)
                else : path_detail += " of the " + self.gendered_link(ind, link)
            path_detail += " of " + name1 + "."
            return [length,path_detail]