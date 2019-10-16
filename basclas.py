# Creates the Basis class that mostly stores the basis set information used throughout pbt
# Currently designed in a 'el' wise fashion, i.e., Basis gives you one atom and one el, but you can overload this.
# The intended, but not enforced, format is (atom, el, [exponents], [[contraction1], [contraction2], [contraction3]], changeatom)
# Contraction is currently optional, the others are not.
# Changeatom is a logical that notes whether or not the atom is different to previous instances of Basis - currently experimental
class Basis:
    def __init__(self, atom, el, exponents, contraction=None, changeatom=False):
        self.atom = atom
        self.el = el
        self.exponents = exponents
        self.contraction = contraction
        self.changeatom = changeatom
    def info(self):
        # Basis.info() will print some basic information, just in case
        if (self.contraction):
            return (self.atom, self.el, self.exponents, self.contraction)
        else:
            return (self.atom, self.el, self.exponents)
