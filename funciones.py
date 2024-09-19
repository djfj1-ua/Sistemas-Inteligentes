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

def calculoVecino(mapi, n, destino):#Tengo que hacer esto para que no pise las casillas de muro
    vecinos = []

    vecinos.append(Nodo(n,Casilla(n.posicion.getCol() + 1,n.posicion.getFila()),1,destino))#Derecha
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol() - 1, n.posicion.getFila()),1,destino))#Izquierda
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol(), n.posicion.getFila() - 1),1,destino))#Arriba
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol(), n.posicion.getFila() + 1),1,destino))#Abajo
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol() - 1, n.posicion.getFila() - 1),1.5,destino))#IzqArriba
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol() + 1, n.posicion.getFila() - 1),1.5,destino))#DerArriba
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol() - 1, n.posicion.getFila() + 1),1.5,destino))#IzqAbajo
    vecinos.append(Nodo(n,Casilla(n.posicion.getCol() + 1, n.posicion.getFila() + 1),1.5,destino))#DerAbajo
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol(), n.posicion.getFila()), 1.5, destino))#El mismo

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
                camAux.append(Casilla(actual.posicion.getFila(),actual.posicion.getCol()))
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

