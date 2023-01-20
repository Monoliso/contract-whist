""" Este modulo incluye todas las funciones para imprimir a la terminal. """

def clear() -> None:
    """ Limpia la terminal """

    print("\033[H\033[J", end="")

def imprimir_triunfo_palo(triunfo: "tuple[str, str]", palo: "tuple[str, str]") -> None:
    if palo:
        print(f"El triunfo de esta mano es '{triunfo[1]}', y el palo de la baza es '{palo[1]}'.")
    else:
        print(f"El triunfo de esta mano es '{triunfo[1]}'.")

def imprimir_mazo(mazo: "list[tuple]", enumerado: bool) -> None:
    """ Dada una lista de cartas recorre 3 veces la misma para permitir mostrarlas
        en serie en la terminal.  """
    tamaño = len(mazo)
    print("┌─────┐ "*tamaño)
    for carta in mazo:
        if carta[0] == "10": 
            print(f"│{carta[0]}   │ ", end='')
        else: print(f"│{carta[0]}    │ ", end='')
    print('')
    for carta in mazo:
        print(f"│  {carta[1]}  │ ", end='')
    print('')
    for carta in mazo:
        if carta[0] == "10":
            print(f"│   {carta[0]}│ ", end='')
        else: print(f"│    {carta[0]}│ ", end='')
    print('')
    print("└─────┘ "*tamaño)
    if enumerado:
        for i in range(tamaño):
            print(f"   {i+1}\t", end='')
        print("\n")
    # \033[F
    # \033[A

def imprimir_predicciones(predicciones: dict) -> None:
    for jugador, prediccion in predicciones.items():
        print(f"{jugador} dijo {prediccion}")

def imprimir_ganador_baza(ganador: str, triunfo: "tuple[str, str]", \
        mesa: "dict[tuple:str]") -> None:
    clear()
    print(f"Carta triunfo:")
    imprimir_mazo([triunfo], False)
    print(f"Las cartas en la mesa fueron jugadas por: {list(mesa.values())}")
    imprimir_mazo(list(mesa), False)
    print(f"La baza la ganó {ganador}")
    input("")

def imprimir_puntaje(puntos_mano, puntos_juego) -> None:
    print(f"El puntaje de esta mano fue: {puntos_mano}")
    print(f"Puntaje de cada jugador: {puntos_juego}")
    input()

def imprimir_mazos_principales(mano, baza, jugadores) -> None:
    numero_bazas, triunfo = mano
    palo_baza, mesa, jugador, cartas_jugador = baza
    clear()
    if jugadores:
        print(f"El orden de los jugadores es: {jugadores}")
    print(f"Carta triunfo de la mano N°{numero_bazas}:")
    imprimir_mazo([triunfo], False)
    if mesa:
        print("Mesa:")
        imprimir_mazo(list(mesa), False)
    print(f"Cartas de {jugador}:")
    imprimir_mazo(cartas_jugador, True) # imprimir_mazo(ordenar_cartas_por_palo(cartas_jugador))
    if mesa:
        print(f"Las cartas en la mesa fueron jugadas por: {list(mesa.values())}")
    imprimir_triunfo_palo(triunfo, palo_baza)

def imprimir_resultado(resultado: str):
    pass

# ---------------------------

def imprimir_mazo_deprecated(mazo: set) -> None:
    for carta in mazo:
        imprimir_carta_deprecated(carta)
    
def imprimir_carta_deprecated(carta: tuple) -> None:
    print("┌─────┐")
    if carta[0] == "10":
        print(f"│{carta[0]}   │")
        print(f"│  {carta[1]}  │")
        print(f"│   {carta[0]}│")
    else:
        print(f"│{carta[0]}    │")
        print(f"│  {carta[1]}  │")
        print(f"│    {carta[0]}│")
    print("└─────┘")

# ---------------------------