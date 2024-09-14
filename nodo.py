class Nodo():
    def __init__(self, padre, posicion,g,destino):
        self.padre = padre
        self.posicion = posicion

        #Calculamos g
        if self.padre is None:
            self.g = 0
        else:
            self.g = self.padre.g + g

        #Calculamos la h con Manhattan
        self.h = abs(destino.getCol() - posicion.getCol()) + abs(destino.getFila() - posicion.getFila())
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.posicion.getCol() == other.posicion.getCol() and self.posicion.getFila() == other.posicion.getFila