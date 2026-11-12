nodos = ["A", "B", "C", "D", "E",
         "F", "G", "H", "I", "J"]



grafo = {

    "A": [("B", 4), ("D", 5), ("G", 7)],

    "B": [("A", 4), ("C", 3), ("F", 8)],

    "C": [("B", 3), ("D", 4), ("F", 5), ("I", 10)],

    "D": [("A", 5), ("C", 4), ("E", 3),
          ("G", 6), ("F", 4)],

    "E": [("D", 3), ("F", 5), ("H", 7), ("J", 8)],

    "F": [("B", 8), ("C", 5), ("D", 4),
          ("E", 5), ("I", 4), ("H", 9)],

    "G": [("A", 7), ("D", 6), ("J", 5), ("H", 11)],

    "H": [("E", 7), ("F", 9), ("G", 11),
          ("I", 8), ("J", 6)],

    "I": [("C", 10), ("F", 4), ("H", 8)],

    "J": [("E", 8), ("G", 5), ("H", 6)]
}



bloqueadas = [("D", "F")]



inicio = "A"
destino = "J"



posiciones = {

    "A": (100, 250),
    "B": (220, 100),
    "C": (370, 100),
    "D": (250, 280),
    "E": (430, 280),
    "F": (520, 120),
    "G": (100, 450),
    "H": (600, 400),
    "I": (700, 150),
    "J": (750, 500)

}



def esta_bloqueada(origen, vecino):

    if (origen, vecino) in bloqueadas or (vecino, origen) in bloqueadas:
        return True

    return False



def obtener_vecinos(nodo):

    vecinos_disponibles = []

    for vecino, costo in grafo[nodo]:

        if not esta_bloqueada(nodo, vecino):

            vecinos_disponibles.append((vecino, costo))

    return vecinos_disponibles



print("MAPA DEL PROYECTO DE IA")
print("-----------------------")

print("Nodos:", nodos)
print("Inicio:", inicio)
print("Destino:", destino)
print("Conexiones bloqueadas:", bloqueadas)
print("Cantidad de nodos:", len(nodos))

print("\nMapa cargado correctamente.")
