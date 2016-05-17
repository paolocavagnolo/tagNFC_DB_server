class padre(object):
    def __init__(self,nome):
        self.nome = nome
    cognome = ""
    eta = 0

class figlio(padre):
    def __init__(self, peso):
        self.peso = peso
    altezza = 0

giuse = padre('giuseppe')

giuse.cognome = "cava"

giuse.eta = 10

print giuse.__dict__

dario = figlio(14)
dario.altezza = 20

print dario.__dict__
