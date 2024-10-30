import math

class Nodo:
    def __init__(self, padre, posicion,g,destino,cal,heuristica):
        self.padre = padre
        self.posicion = posicion

        #Calculamos g
        if self.padre is None:
            self.g = 0
            self.cal = 0
        else:
            self.g = self.padre.g + g
            self.cal = self.padre.cal + cal
        desColumna = destino.getCol()
        desFila = destino.getFila()
        posColumna = posicion.getCol()
        posFila = posicion.getFila()

        if heuristica == 1:
            #Calculamos la h con Manhattan
            self.h =abs(desColumna - posColumna) + abs(desFila - posFila)
            self.f = self.g + self.h

        elif heuristica == 2:
            #Calculamos la h con euclídea
            self.h = math.sqrt(pow((desColumna - posColumna),2) + pow((desFila - posFila),2))
            self.f = self.g + self.h

        elif heuristica == 3:
            # Fórmula de distancia octile
            # Diferencias absolutas entre las coordenadas
            dx = abs(desColumna - posColumna)
            dy = abs(desFila - posFila)

            self.h = min(dx, dy) * math.sqrt(2) + abs(dx - dy)
            self.f = self.g + self.h

        elif heuristica == 4:
            #Heuristica con h=0
            self.h = 0
            self.f = self.g + self.h

    def __eq__(self, other):
        return self.posicion.getCol() == other.posicion.getCol() and self.posicion.getFila() == other.posicion.getFila()

    def __str__(self):#Funcion creada con chatgpt
        padre_pos = f'(Fila:{self.padre.posicion.getFila()}, Columna{self.padre.posicion.getCol()})' if self.padre else 'Ninguno'
        return (f'Posición: ({self.posicion.getFila()}, {self.posicion.getCol()})\n'
                f'G: {self.g}\n'
                f'H: {self.h}\n'
                f'F: {self.f}\n'
                f'Cal: {self.cal}'
                f'Padre: {padre_pos}')