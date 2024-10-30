from mapa import *
from nodo import Nodo
import math

# 0 -> hierba -> . -> 2
# 1 -> muro -> #
# 4 -> agua -> ~ -> 4
# 5 -> roca -> * -> 6

def calculoVecino(mapi, n, destino, heuristica):#Tengo que hacer esto para que no pise las casillas de muro -> #
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
                        vecinos.append(Nodo(n,Casilla(coordX,coordY),1.5,destino,calculoCalorias(mapi,coordX,coordY),heuristica))
                    else:#Las casillas rectas valen 1
                        vecinos.append(Nodo(n,Casilla(coordX,coordY),1,destino,calculoCalorias(mapi,coordX,coordY),heuristica))

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

def calculoFocal(frontera, epsilon):
    # Calcular el factor de expansión con epsilon para relajar el criterio de optimalidad
    factor = 1 + epsilon

    # Encontrar el nodo con el menor valor de f en la lista frontera
    f_min = float('inf')
    for nodo in frontera:
        if nodo.f < f_min:
            f_min = nodo.f

    # Crear la lista focal con nodos cuyo valor de f cumple con el criterio del factor
    lista_focal = []
    for nodo in frontera:
        if nodo.f <= factor * f_min:
            lista_focal.append(nodo)

    # Ordenar la lista focal por la cantidad de calorías de cada nodo (heurística secundaria)
    lista_focal_ordenada = sorted(lista_focal, key=lambda nodo: nodo.cal)

    # Retornar el nodo con menor calorías de la lista focal si la lista no está vacía
    if lista_focal_ordenada:
        nodo_seleccionado = lista_focal_ordenada[0]
    else:
        nodo_seleccionado = None

    return nodo_seleccionado

def es_admisible(nodo_actual, destino):
    distancia_real = math.sqrt((destino.getCol() - nodo_actual.posicion.getCol())**2 + (destino.getFila() - nodo_actual.posicion.getFila())**2)
    if nodo_actual.h > distancia_real:
        print(f'Nodo actual -> {nodo_actual.h}\nDistancia real -> {distancia_real}')
        return False
    return True

def aestrella(mapi, origen, destino, camino, heuristica):

    nodo_inicio = Nodo(None, origen, None, destino, 0, heuristica)
    nodo_inicio.g = 0
    nodo_inicio.h = 0
    nodo_inicio.f = 0

    listaFrontera = [nodo_inicio]  # Nodos no explorados
    listaInterior = []  # Nodos explorados

    while listaFrontera:  # Mientras queden nodos en la lista frontera
        listaFrontera = sorted(listaFrontera, key=lambda nodo: nodo.f)  # Ordeno la lista frontera
        n = listaFrontera[0]  # Nodo con menor f

        if not es_admisible(n, destino):
            # Opcional: detener el algoritmo si encuentra una heurística inadmisible
            print("La heurística no es admisible.")

        # Verificar si el nodo actual es el destino
        if n.posicion.getCol() == destino.getCol() and n.posicion.getFila() == destino.getFila():
            actual = n
            calorias = 0
            print(f'Número de nodos visitados -> {len(listaInterior)}')

            while actual.padre is not None:  # Recompone el camino y calcula las calorías
                coordX = actual.posicion.getFila()
                coordY = actual.posicion.getCol()
                calorias += calculoCalorias(mapi, coordX, coordY)
                camino[coordX][coordY] = 'c'
                actual = actual.padre
            return n.f, calorias  # Devuelve el coste total
        else:  # Si no es el destino
            listaFrontera.remove(n)
            listaInterior.append(n)

            vecinos = calculoVecino(mapi, n, destino, heuristica)

            for m in vecinos:
                if m not in listaInterior:  # Que no estén ya expandidos
                    if m not in listaFrontera:  # Añadir a la frontera si no está
                        listaFrontera.append(m)
                    else:
                        for l in listaFrontera:
                            if m == l and m.f < l.f:
                                m.padre = n
                                listaFrontera[listaFrontera.index(l)] = m
    return -1, 0

def aestrellaEpsilon(mapi, origen, destino, camino, eps, heuristica):
    nodo_inicio = Nodo(None, origen, 0, destino, 0, heuristica)

    listaFrontera = [nodo_inicio]
    listaInterior = []

    while listaFrontera:
        listaFrontera = sorted(listaFrontera, key=lambda nodo: nodo.f)
        n = calculoFocal(listaFrontera, eps)

        if not es_admisible(n, destino):
            # Opcional: detener el algoritmo si encuentra una heurística inadmisible
            print("La heurística no es admisible.")

        if n.posicion.getCol() == destino.getCol() and n.posicion.getFila() == destino.getFila():
            actual = n
            calorias = 0
            print(f'Número de nodos visitados -> {len(listaInterior)}')

            while actual.padre is not None:
                coordX = actual.posicion.getFila()
                coordY = actual.posicion.getCol()
                calorias += calculoCalorias(mapi, coordX, coordY)
                camino[coordX][coordY] = 'c'
                actual = actual.padre
            return n.f, calorias

        listaFrontera.remove(n)
        listaInterior.append(n)

        vecinos = calculoVecino(mapi, n, destino, heuristica)

        for m in vecinos:
            if m not in listaInterior:
                if m not in listaFrontera:
                    listaFrontera.append(m)
                else:
                    for l in listaFrontera:
                        if m == l and m.f < l.f:
                            m.padre = n
                            listaFrontera[listaFrontera.index(l)] = m
    return -1, 0