import mapa
import math
import time



def calcular_heuristica(nodo, destino):

    x1, y1 = mapa.posiciones[nodo]
    x2, y2 = mapa.posiciones[destino]

    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distancia



def reconstruir_ruta(padres, destino):

    ruta = []
    actual = destino

    while actual is not None:

        ruta.append(actual)
        actual = padres[actual]

    ruta.reverse()

    return ruta



def greedy(inicio, destino):


    abiertos = [inicio]


    visitados = []


    padres = {inicio: None}


    tiempo_inicio = time.time()


    while abiertos:


        actual = min(
            abiertos,
            key=lambda nodo: calcular_heuristica(nodo, destino)
        )


        abiertos.remove(actual)


        visitados.append(actual)


        if actual == destino:

            tiempo_final = time.time()

            ruta = reconstruir_ruta(padres, destino)

            costo_total = 0


            for i in range(len(ruta) - 1):

                origen = ruta[i]
                vecino = ruta[i + 1]

                for siguiente, costo in mapa.grafo[origen]:

                    if siguiente == vecino:
                        costo_total += costo
                        break

            return {
                "ruta": ruta,
                "visitados": visitados,
                "costo": costo_total,
                "tiempo": tiempo_final - tiempo_inicio
            }


        for vecino, costo in mapa.obtener_vecinos(actual):


            if vecino not in visitados:


                if vecino not in abiertos:

                    abiertos.append(vecino)

                    padres[vecino] = actual


    tiempo_final = time.time()

    return {
        "ruta": None,
        "visitados": visitados,
        "costo": 0,
        "tiempo": tiempo_final - tiempo_inicio
    }


if __name__ == "__main__":

    resultado = greedy(mapa.inicio, mapa.destino)

    print("\n Resultados del algoritmo greedy")

    if resultado["ruta"]:

        print("Ruta encontrada:", " -> ".join(resultado["ruta"]))

        print("Nodos visitados:", resultado["visitados"])

        print("Costo total:", resultado["costo"])

    else:

        print("No se encontro una ruta.")

        print("Nodos visitados:", resultado["visitados"])

    print("Tiempo de ejecucion:",
          resultado["tiempo"], "segundos")
