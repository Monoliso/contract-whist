""" Este modulo incluye todas las funciones para imprimir a la terminal. """

def clear() -> None:
    """ Limpia la terminal """

    print("\033[H\033[J", end="")

def imprimir_mazo(lista_de_cartas: "list[tuple[str, str]]", enumerado: bool) -> None:
    """ Esta función imprime en pantalla horizontalmente una lista de cartas.
        Acepta como parámetro si se encuentra enumerada.  """
    
    # [xG: desplazar el cursor x columnas
    # [xA: ascender el cursor x filas 
    # [xB: descender el cursor x filas

    nro_columnas = 1
    nro_carta = 1
    for carta in lista_de_cartas:
        if carta[0] != "10":
            print(
                f"\033[{nro_columnas}G┌─────┐\n" 
                f"\033[{nro_columnas}G│{carta[0]}    │\n"
                f"\033[{nro_columnas}G│  {carta[1]}  │\n"
                f"\033[{nro_columnas}G│    {carta[0]}│\n"
                f"\033[{nro_columnas}G└─────┘")
        else: 
            print(
                f"\033[{nro_columnas}G┌─────┐\n" 
                f"\033[{nro_columnas}G│10   │\n"
                f"\033[{nro_columnas}G│  {carta[1]}  │\n"
                f"\033[{nro_columnas}G│   10│\n"
                f"\033[{nro_columnas}G└─────┘")
        if enumerado:
            print(f"\033[{nro_columnas}G   {nro_carta}\t")
            print("\033[7A")
        else:
            print("\033[6A")
        nro_columnas += 8
        nro_carta += 1
    if enumerado:
        print("\033[6B")
    else:
        print("\033[5B")

def imprimir_inicio_juego(jugadores: "list[str]") -> None:
    input("\nBienvenidos al Whist, esperamos que disfruten del juego.")
    input(f"El orden de los jugadores es: {jugadores}.")
    input("Empieza el juego.")

def imprimir_inicio_mano(numero_mano: int, jugador: str) -> None:
    clear()
    input(f"Comienza la mano de {numero_mano}. Ahora es el turno de {jugador}.")
    clear()
    input(f"Turno de {jugador}. Presione Enter cuando tenga el dispositivo en mano.")

def imprimir_transicion(jugador: str):
    input(f"Entregue la computadora a {jugador}.")
    clear()
    input(f"Turno de {jugador}. Presione Enter cuando tenga el dispositivo en mano.")
    clear()

def imprimir_canto_predicciones(triunfo: "tuple[str, str]", jugador: str, 
                                cartas_jugador: "list[tuple[str, str]]", 
                                predicciones_previas: "dict[str:int]") -> None:

    print(f"Carta triunfo de la mano actual:")
    imprimir_mazo([triunfo], False)
    print(f"Cartas de {jugador}:")
    imprimir_mazo(cartas_jugador, True)
    if predicciones_previas:
        print(f"Prediccion de cada jugador (nombre, predicción): {predicciones_previas}")

def imprimir_seleccion_carta(triunfo: "tuple[str, str]", mesa: "dict[tuple:str]", 
                             jugador: str, cartas_jugador: "list[tuple]") -> None:

    print(f"Carta triunfo de la mano actual:")
    imprimir_mazo([triunfo], False)
    if mesa:
        jugadores_previos = list(mesa.values())
        palo = (list(mesa.keys()))[0]
        print("Mesa:")
        imprimir_mazo(mesa, False)
    print(f"Cartas de {jugador}:")
    imprimir_mazo(cartas_jugador, True)
    if mesa:
        print(f"Las cartas en la mesa fueron jugadas por: {jugadores_previos}")
        print(f"El triunfo de esta mano es '{triunfo[1]}', y el palo de la baza es '{palo[1]}'.")
    else:
        print(f"El triunfo de esta mano es '{triunfo[1]}'.")

def imprimir_ganador_baza(triunfo: "tuple[str, str]", mesa: "dict[tuple:str]", ganador: str) -> None:

    clear()
    jugadores_orden = list(mesa.values())
    print("Carta triunfo:")
    imprimir_mazo([triunfo], False)
    print("Mesa:")
    imprimir_mazo(mesa, False)
    input(f"Las cartas en la mesa fueron jugadas por: {jugadores_orden}\n\n"
          f"La baza la ganó {ganador}.")
    
def imprimir_puntaje_mano(puntaje_mano: dict, puntaje_juego: dict) -> None:
    input(f"El puntaje de esta mano fue: {puntaje_mano}\n"
          f"Puntaje de cada jugador: {puntaje_juego}")

def imprimir_resultado_juego(puntaje_final: str):
    print("Ha finalizado el juego, los puntajes de cada jugador son:\n\n"
          f"{puntaje_final}")
    
def imprimir_ganador(resultado: tuple) -> None:
    ganador = resultado[0][0]
    puntaje = resultado[1]
    print(f"Ha ganado {ganador} con {puntaje} puntos, felicitaciones! 🥳🎉")

def imprimir_empate(resultado: tuple) -> None:
    ganadores = resultado[0]
    puntaje = resultado[1]
    print(f"Los ganadores fueron {ganadores} con {puntaje} puntos, felicitaciones! 🥳🎉")
