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


def comprobar(mapi, origen, coste, cal, destino):

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

    listaFrontera.append(nodo_inicio)

    while listaFrontera:
        n = sorted(listaFrontera, key=lambda nodo:nodo.f)