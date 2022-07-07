
class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.enfant_gauche = None
        self.enfant_droit = None

    def insert_gauche(self, valeur):
        if self.enfant_gauche == None:
            self.enfant_gauche = Noeud(valeur)
        else:
            new_node = Noeud(valeur)
            new_node.enfant_gauche = self.enfant_gauche
            self.enfant_gauche = new_node

    def insert_droit(self, valeur):
        if self.enfant_droit == None:
            self.enfant_droit = Noeud(valeur)
        else:
            new_node = Noeud(valeur)
            new_node.enfant_droit = self.enfant_droit
            self.enfant_droit = new_node
    def get_valeur(self):
        return self.valeur
    def get_gauche(self):
        return self.enfant_gauche
    def get_droit(self):
        return self.enfant_droit
    
def affiche(arbre):
    if arbre != None:
        return (arbre.get_valeur(), affiche(arbre.get_gauche()), affiche(arbre.get_droit()))


racine = Noeud('A')
racine.insert_gauche('B')
racine.insert_droit('F')

b_node = racine.get_gauche()
b_node.insert_gauche('C')
b_node.insert_droit('D')

f_node = racine.get_droit()
f_node.insert_gauche('G')
f_node.insert_droit('H')

c_node = b_node.get_gauche()
c_node.insert_droit('E')

g_node = f_node.get_gauche()
g_node.insert_gauche('I')

h_node = f_node.get_droit()
h_node.insert_droit('J')

   
print(affiche(racine))
   