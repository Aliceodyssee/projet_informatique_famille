class Family :
    def __init__(self) :
        self._family = None
        self._parents = []
        self._children = []
    
    def get_id(self) :
        return self._id
    
    def get_parents(self) :
        """
        Returns
        ---
        parents : two element list of individualElement
        0 : father
        1 : moter
        """
        return self._parents

    def get_children(self) :
        """
        Returns
        ---
        children : list of individualElement
        empty if no child
        """
        return self._children

    def print(self) :
        pass
        





    