import mapa
import math
import time



def calcular_distancia(nodo1, nodo2):

    x1, y1 = mapa.posiciones[nodo1]
    x2, y2 = mapa.posiciones[nodo2]

    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distancia



def obtener_escala_heuristica():

    escala = float("inf")

    for origen in mapa.grafo:

        for vecino, costo in mapa.grafo[origen]:

            distancia = calcular_distancia(origen, vecino)

            if distancia > 0:

                proporcion = costo / distancia

                if proporcion < escala:
                    escala = proporcion

    return escala



def calcular_heuristica(nodo, destino, escala):

    distancia = calcular_distancia(nodo, destino)

    return distancia * escala



def reconstruir_ruta(padres, destino):

    ruta = []
    actual = destino

    while actual is not None:

        ruta.append(actual)
        actual = padres[actual]

    ruta.reverse()

    return ruta



def astar(inicio, destino):


    escala = obtener_escala_heuristica()


    abiertos = [inicio]


    visitados = []


    padres = {inicio: None}


    costos = {inicio: 0}


    tiempo_inicio = time.time()


    while abiertos:


        actual = min(
            abiertos,
            key=lambda nodo: costos[nodo] +
            calcular_heuristica(nodo, destino, escala)
        )


        abiertos.remove(actual)


        visitados.append(actual)


        if actual == destino:

            ruta = reconstruir_ruta(padres, destino)

            tiempo_final = time.time()

            return {
                "ruta": ruta,
                "visitados": visitados,
                "costo": costos[destino],
                "tiempo": tiempo_final - tiempo_inicio
            }


        for vecino, costo in mapa.obtener_vecinos(actual):


            nuevo_costo = costos[actual] + costo


            if nuevo_costo < costos.get(vecino, float("inf")):


                costos[vecino] = nuevo_costo


                padres[vecino] = actual


                if vecino in visitados:
                    visitados.remove(vecino)


                if vecino not in abiertos:
                    abiertos.append(vecino)


    tiempo_final = time.time()

    return {
        "ruta": None,
        "visitados": visitados,
        "costo": 0,
        "tiempo": tiempo_final - tiempo_inicio
    }



if __name__ == "__main__":

    resultado = astar(mapa.inicio, mapa.destino)

    print("\n Resultados del algoritmo A*")

    if resultado["ruta"]:

        print("Ruta encontrada:",
              " -> ".join(resultado["ruta"]))

        print("Nodos visitados:",
              resultado["visitados"])

        print("Costo total:",
              resultado["costo"])

    else:

        print("No se encontro una ruta.")

        print("Nodos visitados:",
              resultado["visitados"])

    print("Tiempo de ejecucion:",
          resultado["tiempo"], "segundos")
