import mapa
import time



def reconstruir_ruta(padres, destino):

    ruta = []
    actual = destino

    while actual is not None:

        ruta.append(actual)
        actual = padres[actual]

    ruta.reverse()

    return ruta



def calcular_costo(ruta):

    costo_total = 0

    for i in range(len(ruta) - 1):

        origen = ruta[i]
        vecino = ruta[i + 1]

        for siguiente, costo in mapa.obtener_vecinos(origen):

            if siguiente == vecino:

                costo_total += costo
                break

    return costo_total



def bfs(inicio, destino):


    tiempo_inicio = time.perf_counter()


    cola = [inicio]


    descubiertos = [inicio]


    padres = {inicio: None}


    visitados = []


    while cola:


        actual = cola.pop(0)


        visitados.append(actual)


        if actual == destino:

            ruta = reconstruir_ruta(padres, destino)

            costo_total = calcular_costo(ruta)

            tiempo_final = time.perf_counter()

            return {
                "ruta": ruta,
                "visitados": visitados,
                "costo": costo_total,
                "tiempo": tiempo_final - tiempo_inicio
            }


        for vecino, costo in mapa.obtener_vecinos(actual):


            if vecino not in descubiertos:


                descubiertos.append(vecino)


                padres[vecino] = actual


                cola.append(vecino)


    tiempo_final = time.perf_counter()

    return {
        "ruta": None,
        "visitados": visitados,
        "costo": 0,
        "tiempo": tiempo_final - tiempo_inicio
    }


if __name__ == "__main__":

    resultado = bfs(mapa.inicio, mapa.destino)

    print("\n Resultados del algoritmo bfs")


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
