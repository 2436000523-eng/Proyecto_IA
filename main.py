import tkinter as tk
from tkinter import ttk

import mapa
import bfs
import dfs
import greedy
import astar

ventana = tk.Tk()

ventana.title("Proyecto de Inteligencia Artificial")
ventana.geometry("1100x700")
ventana.minsize(900, 580)
ventana.configure(bg="#F2F4F8")


COLOR_FONDO = "#F2F4F8"
COLOR_MAPA = "#FFFFFF"
COLOR_LINEA = "#AAB2BD"
COLOR_BLOQUEADA = "#E74C3C"
COLOR_RUTA = "#27AE60"
COLOR_VISITADO = "#F39C12"
COLOR_NODO = "#3498DB"


ultimo_resultado = None
ultimo_inicio = None
ultimo_destino = None



titulo = tk.Label(
    ventana,
    text="PROYECTO DE INTELIGENCIA ARTIFICIAL",
    font=("Arial", 18, "bold"),
    bg=COLOR_FONDO
)

titulo.pack(pady=(8, 2))


subtitulo = tk.Label(
    ventana,
    text="Sistema de busqueda y comparacion de rutas",
    font=("Arial", 10),
    bg=COLOR_FONDO
)

subtitulo.pack(pady=(0, 6))






marco_seleccion = tk.LabelFrame(
    ventana,
    text=" SELECCION DE NODOS ",
    font=("Arial", 10, "bold"),
    bg=COLOR_FONDO,
    padx=10,
    pady=7
)

marco_seleccion.pack(
    padx=15,
    pady=4,
    fill="x"
)




tk.Label(
    marco_seleccion,
    text="Nodo inicial:",
    font=("Arial", 10, "bold"),
    bg=COLOR_FONDO
).pack(side="left", padx=8)


seleccion_inicio = ttk.Combobox(
    marco_seleccion,
    values=mapa.nodos,
    state="readonly",
    width=8
)

seleccion_inicio.pack(side="left", padx=5)

seleccion_inicio.set(mapa.inicio)




tk.Label(
    marco_seleccion,
    text="Nodo destino:",
    font=("Arial", 10, "bold"),
    bg=COLOR_FONDO
).pack(side="left", padx=(25, 8))


seleccion_destino = ttk.Combobox(
    marco_seleccion,
    values=mapa.nodos,
    state="readonly",
    width=8
)

seleccion_destino.pack(side="left", padx=5)

seleccion_destino.set(mapa.destino)






def calcular_costos_ruta(ruta):

    detalles = []

    costo_total = 0

    for i in range(len(ruta) - 1):

        origen = ruta[i]
        destino = ruta[i + 1]

        for vecino, costo in mapa.obtener_vecinos(origen):

            if vecino == destino:

                detalles.append(
                    f"{origen} -> {destino}: {costo}"
                )

                costo_total += costo

                break

    return detalles, costo_total






def obtener_posicion(nodo):



    ancho = lienzo.winfo_width()
    alto = lienzo.winfo_height()



    x, y = mapa.posiciones[nodo]



    minimo_x = min(
        p[0] for p in mapa.posiciones.values()
    )

    maximo_x = max(
        p[0] for p in mapa.posiciones.values()
    )

    minimo_y = min(
        p[1] for p in mapa.posiciones.values()
    )

    maximo_y = max(
        p[1] for p in mapa.posiciones.values()
    )




    if ancho <= 1 or alto <= 1:

        return 0, 0



    margen = 35

    espacio_x = ancho - margen * 2
    espacio_y = alto - margen * 2



    escala_x = espacio_x / (maximo_x - minimo_x)
    escala_y = espacio_y / (maximo_y - minimo_y)




    escala = min(escala_x, escala_y)



    ancho_mapa = (maximo_x - minimo_x) * escala
    alto_mapa = (maximo_y - minimo_y) * escala



    inicio_x = (ancho - ancho_mapa) / 2
    inicio_y = (alto - alto_mapa) / 2



    nueva_x = inicio_x + (x - minimo_x) * escala
    nueva_y = inicio_y + (y - minimo_y) * escala

    return nueva_x, nueva_y






def dibujar_mapa(resultado=None, inicio=None, destino=None):

    lienzo.delete("all")

    ruta = []
    visitados = []

    if inicio is None:
        inicio = seleccion_inicio.get()

    if destino is None:
        destino = seleccion_destino.get()

    if resultado:

        ruta = resultado["ruta"] or []
        visitados = resultado["visitados"]





    conexiones_dibujadas = []

    for origen in mapa.grafo:

        for vecino, costo in mapa.grafo[origen]:

            conexion = tuple(sorted((origen, vecino)))

            if conexion in conexiones_dibujadas:
                continue

            conexiones_dibujadas.append(conexion)

            x1, y1 = obtener_posicion(origen)
            x2, y2 = obtener_posicion(vecino)

            bloqueada = mapa.esta_bloqueada(
                origen, vecino
            )

            if bloqueada:

                color = COLOR_BLOQUEADA
                grosor = 3
                estilo = (6, 3)

            else:

                color = COLOR_LINEA
                grosor = 2
                estilo = None

            lienzo.create_line(
                x1, y1,
                x2, y2,
                fill=color,
                width=grosor,
                dash=estilo
            )



            xm = (x1 + x2) / 2
            ym = (y1 + y2) / 2

            texto = "X" if bloqueada else str(costo)

            lienzo.create_text(
                xm,
                ym - 9,
                text=texto,
                fill=COLOR_BLOQUEADA if bloqueada else "black",
                font=("Arial", 9, "bold")
            )





    for i in range(len(ruta) - 1):

        origen = ruta[i]
        vecino = ruta[i + 1]

        x1, y1 = obtener_posicion(origen)
        x2, y2 = obtener_posicion(vecino)

        lienzo.create_line(
            x1, y1,
            x2, y2,
            fill=COLOR_RUTA,
            width=5
        )





    for nodo in mapa.nodos:

        x, y = obtener_posicion(nodo)

        if nodo == inicio and nodo == destino:

            color = "#8E44AD"

        elif nodo == inicio:

            color = "#2ECC71"

        elif nodo == destino:

            color = "#9B59B6"

        elif nodo in ruta:

            color = COLOR_RUTA

        elif nodo in visitados:

            color = COLOR_VISITADO

        else:

            color = COLOR_NODO

        lienzo.create_oval(
            x - 20,
            y - 20,
            x + 20,
            y + 20,
            fill=color,
            outline="black",
            width=2
        )

        lienzo.create_text(
            x,
            y,
            text=nodo,
            fill="white",
            font=("Arial", 11, "bold")
        )



def mostrar_resultados(nombre, resultado, inicio, destino):

    cuadro_resultados.config(state="normal")

    cuadro_resultados.delete("1.0", tk.END)

    cuadro_resultados.insert(
        tk.END,
        "ALGORITMO: " + nombre + "\n"
    )

    cuadro_resultados.insert(
        tk.END,
        "--------------------------------\n"
    )

    cuadro_resultados.insert(
        tk.END,
        f"Inicio: {inicio}\n"
        f"Destino: {destino}\n\n"
    )

    if resultado["ruta"]:

        ruta = resultado["ruta"]

        detalles, costo_total = calcular_costos_ruta(ruta)


        cuadro_resultados.insert(
            tk.END,
            "RUTA ENCONTRADA\n"
        )

        cuadro_resultados.insert(
            tk.END,
            " -> ".join(ruta) + "\n\n"
        )



        cuadro_resultados.insert(
            tk.END,
            "NODOS EXPLORADOS\n"
        )

        cuadro_resultados.insert(
            tk.END,
            " -> ".join(resultado["visitados"]) + "\n\n"
        )

        cuadro_resultados.insert(
            tk.END,
            "COSTO DE CADA CONEXION\n"
        )

        for detalle in detalles:

            cuadro_resultados.insert(
                tk.END,
                detalle + "\n"
            )


        cuadro_resultados.insert(
            tk.END,
            "\n--------------------------------\n"
        )

        cuadro_resultados.insert(
            tk.END,
            f"COSTO TOTAL: {costo_total}\n"
        )

    else:

        cuadro_resultados.insert(
            tk.END,
            "NO SE ENCONTRO UNA RUTA.\n\n"
        )

        cuadro_resultados.insert(
            tk.END,
            "NODOS EXPLORADOS:\n"
            + " -> ".join(resultado["visitados"])
            + "\n"
        )

        cuadro_resultados.insert(
            tk.END,
            "\nCOSTO TOTAL: No disponible\n"
        )


    cuadro_resultados.insert(
        tk.END,
        "\nTIEMPO DE EJECUCION\n"
    )

    cuadro_resultados.insert(
        tk.END,
        "{:.8f} segundos\n".format(
            resultado["tiempo"]
        )
    )

    cuadro_resultados.config(state="disabled")



def ejecutar_algoritmo(nombre):

    global ultimo_resultado
    global ultimo_inicio
    global ultimo_destino

    inicio = seleccion_inicio.get()
    destino = seleccion_destino.get()

    if not inicio or not destino:
        return


    if nombre == "BFS":

        resultado = bfs.bfs(inicio, destino)

    elif nombre == "DFS":

        resultado = dfs.dfs(inicio, destino)

    elif nombre == "GREEDY":

        resultado = greedy.greedy(inicio, destino)

    elif nombre == "A*":

        resultado = astar.astar(inicio, destino)


    ultimo_resultado = resultado
    ultimo_inicio = inicio
    ultimo_destino = destino


    dibujar_mapa(
        resultado,
        inicio,
        destino
    )


    mostrar_resultados(
        nombre,
        resultado,
        inicio,
        destino
    )


def reiniciar_mapa():

    global ultimo_resultado
    global ultimo_inicio
    global ultimo_destino

    ultimo_resultado = None

    ultimo_inicio = seleccion_inicio.get()
    ultimo_destino = seleccion_destino.get()

    dibujar_mapa(
        None,
        ultimo_inicio,
        ultimo_destino
    )

    cuadro_resultados.config(state="normal")

    cuadro_resultados.delete("1.0", tk.END)

    cuadro_resultados.insert(
        tk.END,
        "Selecciona un algoritmo para comenzar.\n\n"
        "Puedes cambiar el nodo inicial y el destino."
    )

    cuadro_resultados.config(state="disabled")



def actualizar_mapa(event):

    dibujar_mapa(
        ultimo_resultado,
        ultimo_inicio,
        ultimo_destino
    )



marco_botones = tk.LabelFrame(
    ventana,
    text=" ALGORITMOS DE BUSQUEDA ",
    font=("Arial", 10, "bold"),
    bg=COLOR_FONDO,
    padx=8,
    pady=6
)

marco_botones.pack(
    padx=15,
    pady=4,
    fill="x"
)


def crear_boton(nombre, columna, color="#3498DB"):

    boton = tk.Button(
        marco_botones,
        text=nombre,
        width=13,
        font=("Arial", 9, "bold"),
        bg=color,
        fg="white",
        activebackground="#2874A6",
        command=lambda: ejecutar_algoritmo(nombre)
    )

    boton.grid(
        row=0,
        column=columna,
        padx=7,
        pady=3
    )


crear_boton("BFS", 0)
crear_boton("DFS", 1)
crear_boton("GREEDY", 2)
crear_boton("A*", 3)


boton_reiniciar = tk.Button(
    marco_botones,
    text="REINICIAR",
    width=13,
    font=("Arial", 9, "bold"),
    bg="#7F8C8D",
    fg="white",
    command=reiniciar_mapa
)

boton_reiniciar.grid(
    row=0,
    column=4,
    padx=7
)


marco_contenido = tk.Frame(
    ventana,
    bg=COLOR_FONDO
)

marco_contenido.pack(
    padx=12,
    pady=6,
    fill="both",
    expand=True
)

marco_contenido.grid_columnconfigure(
    0,
    weight=3
)

marco_contenido.grid_columnconfigure(
    1,
    weight=2
)

marco_contenido.grid_rowconfigure(
    0,
    weight=1
)



marco_mapa = tk.LabelFrame(
    marco_contenido,
    text=" MAPA DE CONEXIONES ",
    font=("Arial", 10, "bold"),
    bg=COLOR_FONDO,
    padx=5,
    pady=5
)

marco_mapa.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 6)
)


lienzo = tk.Canvas(
    marco_mapa,
    width=500,
    height=430,
    bg=COLOR_MAPA,
    highlightthickness=1,
    highlightbackground="#CCCCCC"
)

lienzo.pack(
    fill="both",
    expand=True
)



lienzo.bind(
    "<Configure>",
    actualizar_mapa
)



marco_resultados = tk.LabelFrame(
    marco_contenido,
    text=" RESULTADOS DEL ALGORITMO ",
    font=("Arial", 10, "bold"),
    bg=COLOR_FONDO,
    padx=7,
    pady=7
)

marco_resultados.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(6, 0)
)


cuadro_resultados = tk.Text(
    marco_resultados,
    font=("Consolas", 10),
    wrap="word",
    bg="#FFFFFF",
    fg="#222222",
    relief="solid",
    padx=10,
    pady=10,
    state="disabled"
)

cuadro_resultados.pack(
    side="left",
    fill="both",
    expand=True
)



barra = ttk.Scrollbar(
    marco_resultados,
    orient="vertical",
    command=cuadro_resultados.yview
)

barra.pack(
    side="right",
    fill="y"
)

cuadro_resultados.config(
    yscrollcommand=barra.set
)


leyenda = tk.Label(
    ventana,
    text=(
        "VERDE: Ruta / Inicio     "
        "NARANJA: Explorados     "
        "AZUL: Sin explorar     "
        "MORADO: Destino     "
        "ROJO: Conexion bloqueada"
    ),
    font=("Arial", 9),
    bg=COLOR_FONDO
)

leyenda.pack(pady=(2, 7))


ventana.update_idletasks()

ultimo_inicio = seleccion_inicio.get()
ultimo_destino = seleccion_destino.get()

dibujar_mapa()

ventana.mainloop()
