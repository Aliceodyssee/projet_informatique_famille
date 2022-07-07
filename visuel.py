
from treelib import Node, Tree 
tree = Tree() 
tree.create_node("Harry", "harry") # No parent means its the root node 
tree.create_node("Jane", "jane" , parent="harry") 
tree.create_node("Bill", "bill" , parent="harry") 
tree.create_node("Diane", "diane" , parent="jane") 
tree.create_node("Mary", "mary" , parent="diane") 
tree.create_node("Mark", "mark" , parent="jane") 
tree.show()

def print(self,v1,v2) :
        """
        Prints interprated path with visual tree

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

        tree = Tree()
        for i in range(1,len(path)):
            if i%3 == 2 :
                if self.find_Element(ind)[0] : element = self.find_Element(ind)[1]
                name, surname = element.get_name()
                print(" of " + name + surname + ", who is the " + self.gendered_link(ind, link))
            else : print(" of the " + self.gendered_link(ind, link))


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

