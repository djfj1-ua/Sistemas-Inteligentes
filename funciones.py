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

def calculoVecino(mapi, n, destino):
    vecinos = []

    vecinos.append(Nodo(n,Casilla(n.posicion.getCol() + 1,n.posicion.getFila()),1,destino))#Derecha
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol() - 1, n.posicion.getFila()),1,destino))#Izquierda
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol(), n.posicion.getFila() - 1),1,destino))#Arriba
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol(), n.posicion.getFila() + 1),1,destino))#Abajo
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol() - 1, n.posicion.getFila() - 1),1.5,destino))#IzqArriba
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol() + 1, n.posicion.getFila() - 1),1.5,destino))#DerArriba
    vecinos.append(Nodo(n, Casilla(n.posicion.getCol() - 1, n.posicion.getFila() + 1),1.5,destino))#IzqAbajo
    vecinos.append(Nodo(n,Casilla(n.posicion.getCol() + 1, n.posicion.getFila() + 1),1.5,destino))#DerAbajo

    return vecinos

def aestrella(mapi, origen, coste, cal, destino, camino):

    nodo_inicio = Nodo(None, origen, None, destino)
    nodo_inicio.g = 0
    nodo_inicio.h = 0
    nodo_inicio.f = 0

    nodo_final = Nodo(None, destino, None, destino)
    nodo_final.g = 0
    nodo_final.h = 0
    nodo_final.f = 0

    listaFrontera = []
    listaInterior = []
    camino = []

    listaFrontera.append(nodo_inicio)

    while listaFrontera:
        laux = sorted(listaFrontera, key=lambda nodo:nodo.f)
        n = laux[0]
        nodo_inicio = n

        if n.posicion.getCol() == destino.getCol() and n.posicion.getFila() == destino.getFila():
            while n.padre is not None:
                n = n.padre
            break
        else:
            listaFrontera.remove(n)
            listaInterior.append(n)

            m = calculoVecino(mapi, n, destino)

            for vecino in m:
                vecino.g = n.g + vecino.g

                if vecino not in listaFrontera:


