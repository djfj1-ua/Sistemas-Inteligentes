import sys, pygame, math
from casilla import *
from mapa import *
from pygame.locals import *

from nodo import Nodo

# 0 -> hierba -> . -> 2
# 1 -> muro -> #
# 4 -> agua -> ~ -> 4
# 5 -> roca -> * -> 6

def calculoVecino(mapi, n, destino):#Tengo que hacer esto para que no pise las casillas de muro -> #
    vecinos = []

    #Calcular los vecinos teniendo en cuenta los muros y que no se salga de la cuadricula
    for i in range(-1,2):
        for j in range(-1,2):

            if i == 0 and j == 0:  # Si el nodo es el actual, que salte esa iteración.
                continue

            coordX = n.posicion.getFila() + i
            coordY = n.posicion.getCol() + j
            alto = mapi.getAlto()
            ancho = mapi.getAncho()

            if 0 <= coordX < alto and 0 <= coordY < ancho:#Si esta dentro del mapa
                res = mapi.getCelda(coordX, coordY)#Guardamos en res el tipo de casilla en el que estamos

                if res != 1:#Si no es un muro, almacenamos el nodo dependiendo de si es diagonal o no
                    if i != 0 and j != 0:#Diagonales valen 1.5
                        vecinos.append(Nodo(n,Casilla(coordX,coordY),1.5,destino))
                    else:#Las casillas en linea valen 1
                        vecinos.append(Nodo(n,Casilla(coordX,coordY),1,destino))

    return vecinos

def calculoCalorias(mapi, x, y):

    if mapi.getCelda(x,y) == 0:
        return 2
    elif mapi.getCelda(x,y) == 4:
        return 4
    elif mapi.getCelda(x,y) == 5:
        return 6
    else:
        return 0


def aestrella(mapi, origen, destino, camino):

    nodo_inicio = Nodo(None, origen, None, destino)
    nodo_inicio.g = 0
    nodo_inicio.h = 0
    nodo_inicio.f = 0

    listaFrontera = []#Nodos no explorados
    listaInterior = []#Nodos explorados

    listaFrontera.append(nodo_inicio)

    while listaFrontera:#Mientras queden nodos en la lista frontera
        listaFrontera = sorted(listaFrontera, key=lambda nodo:nodo.f)#Ordeno la lista frontera descendentemente segun f
        n = listaFrontera[0]#Escojo el que tenga menor f para nodo actual

        if n.posicion.getCol() == destino.getCol() and n.posicion.getFila() == destino.getFila():#Si hemos llegado al destino
            actual = n
            calorias = 0
            while actual.padre is not None:#Recompongo el camino y calculo las calorias
                coordX = actual.posicion.getFila()
                coordY = actual.posicion.getCol()
                calorias += calculoCalorias(mapi,coordX,coordY)
                camino[coordX][coordY] = 'c'
                actual = actual.padre
            return n.f, calorias#Devuelvo el coste total
        else:#Si no es la casilla destino

            listaFrontera.remove(n)#Quito el nodo actual de la lista frontera
            listaInterior.append(n)#Paso a explorar el nodo actual

            vecinos = calculoVecino(mapi, n, destino)#Calculo los nodos vecinos del nodo actual

            for m in vecinos:#Para todos los nodos vecinos
                if m not in listaInterior:#Que no esten expandidos ya
                    if m not in listaFrontera:#Si no lo hemos alcanzado aun, lo metemos en lista frontera
                        listaFrontera.append(m)
                    else:#Si ya lo hemos alcanzado anteriormente, calculamos el camino con menor coste entre el camino anterior y el actual
                        for l in listaFrontera:
                            #if (m.posicion.getCol() == l.posicion.getCol() and m.posicion.getFila() == l.posicion.getFila()) and m.f < l.f:#Si es la misma posicion y tiene un coste menor
                            if (m == l) and m.f < l.f:
                                m.padre = n#Cambiamos el padre por el nodo actual
                                listaFrontera[listaFrontera.index(l)] = m#y cambiamos el nodo de la lista frontera por el actual
    return -1, 0

