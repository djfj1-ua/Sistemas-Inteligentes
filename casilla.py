class Casilla():
    def __init__(self, f, c):
        self.fila=f
        self.col=c
        
    def getFila (self):
        return self.fila
    
    def getCol (self):
        return self.col
        
    def __str__(self):
        return f"Casilla(fila: {self.fila}, columna: {self.col})"