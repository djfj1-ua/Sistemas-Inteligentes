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
        self.h = 0#abs(destino.getCol() - posicion.getCol()) + abs(destino.getFila() - posicion.getFila())
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.posicion.getCol() == other.posicion.getCol() and self.posicion.getFila() == other.posicion.getFila()

    def __str__(self):
        padre_pos = f'(Fila:{self.padre.posicion.getFila()}, Columna{self.padre.posicion.getCol()})' if self.padre else 'Ninguno'
        return (f'Posición: ({self.posicion.getFila()}, {self.posicion.getCol()})\n'
                f'G: {self.g}\n'
                f'H: {self.h}\n'
                f'F: {self.f}\n'
                f'Padre: {padre_pos}')