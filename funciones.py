import sys, pygame
from casilla import *
from mapa import *
from pygame.locals import *

from nodo import Nodo

# 0 -> hierba -> .
# 1 -> muro -> #
# 4 -> agua -> ~
# 5 -> roca -> *

cos = [("normal",1), ("diagonal",1.5)]

esfuerzo = [("hierba",2),("agua",4),("roca",6)]

def calculoVecino(mapi, n, destino):#Tengo que hacer esto para que no pise las casillas de muro -> #
    vecinos = []

    #Calcular los vecinos teniendo en cuenta los muros y que se salga de la cuadricula
    for i in range(-1,2):
        for j in range(-1,2):
            coordX = n.posicion.getFila() + i
            coordY = n.posicion.getCol() + j
            res = mapi.getCelda(coordX, coordY)
            if mapi.getCelda(coordX,coordY) != 1 and (mapi.getAncho() - 1 != coordX and mapi.getAlto() - 1 != coordY):#Mirar lo de out of range
                if i != 0 and j != 0:
                    vecinos.append(Nodo(n,Casilla(coordX,coordY),1.5,destino))
                else:
                    vecinos.append(Nodo(n,Casilla(coordX,coordY),1,destino))

    return vecinos

def aestrella(mapi, origen, cal, destino, camino):

    nodo_inicio = Nodo(None, origen, None, destino)
    nodo_inicio.g = 0
    nodo_inicio.h = 0
    nodo_inicio.f = 0

    nodo_final = Nodo(None, destino, None, destino)
    nodo_final.g = 0
    nodo_final.h = 0
    nodo_final.f = 0

    listaFrontera = []#Nodos no explorados
    listaInterior = []#Nodos explorados

    listaFrontera.append(nodo_inicio)

    while listaFrontera:
        listaFrontera = sorted(listaFrontera, key=lambda nodo:nodo.f)
        n = listaFrontera[0]

        if n.posicion.getCol() == destino.getCol() and n.posicion.getFila() == destino.getFila():
            actual = n
            camAux = []
            while actual:
                camino[actual.posicion.getCol()][actual.posicion.getFila()] = 'c'
                actual = actual.padre
            return n.f
        else:

            for x in listaFrontera:
                if n.posicion.getCol() == x.posicion.getCol() and n.posicion.getFila() == x.posicion.getFila():
                    listaFrontera.pop(0)
                    break

            listaInterior.append(n)

            vecinos = calculoVecino(mapi, n, destino)

            for m in vecinos:
                if m not in listaInterior:
                    if m not in listaFrontera:
                        listaFrontera.append(m)
                    else:
                        for l in listaFrontera:
                            if (m.posicion.getCol() == l.posicion.getCol() and m.posicion.getFila() == l.posicion.getFila()) and m.f < l.f:
                                m.padre = n
                                listaFrontera[listaFrontera.index(l)] = m
    print('Error, no se encuentra solucion')

