import random

def crear_jugador(nombre):
    return [nombre, []]

def cant_jugadores():
    i = -1
    while i == -1:
        try:
            jugador = int(input("Ingrese la cantidad de jugadores: "))
            assert 1 < jugador <= 6
            i = 0
        except ValueError:
            print("El valor ingresado no es correcto")
            i = -1
        except AssertionError:
            print("El número de jugadores ingresados no es correcto")
            i = -1

    return jugador

def crear_mazo():
    colores = ['rojo', 'verde', 'azul', 'amarillo']
    valores = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', 'Reversa', 'Saltar']
    cartas_negras = ['+4', 'cambio de color']

    mazo = [[color, valor] for color in colores for valor in valores]
    mazo += [[color, valor] for valor in cartas_negras for color in ['negro']] * 4

    random.shuffle(mazo)
    return mazo

def repartir_cartas(mazo, jugadores):
    for i in range(7):
        for jugador in jugadores:
            carta = mazo.pop()
            jugador[1].append(carta)
    return jugadores

def siguiente_jugador(actual, total, sentido, saltar):
    if sentido == "inverso" and saltar:
        return (actual - 2) % total              #para que saltee en sentido inverso
    elif sentido == "inverso":
        return (actual - 1) % total              #para que cuando toque reversa, vaya en sentido contrario
    elif sentido == "normal" and saltar:
        return (actual + 2) % total
    else:
        return (actual + 1) % total  

def poner_carta_medio(mazo):
    carta_azar = random.choice([carta for carta in mazo if carta[0] != 'negro'])  #para asegurar que la primera carta no sea negra
    mazo.remove(carta_azar)
    return carta_azar

def mostrar_carta_medio(carta_medio):
    print(f"Carta del centro: {carta_medio}")

def comparar_manos(mano, carta_medio):
    tiene_match = False
    for carta in mano:
        if carta[0] == carta_medio[0] or carta[1] == carta_medio[1]:
            tiene_match = True
            carta_a_remover = carta
    if tiene_match:
        mano.remove(carta_a_remover)
    else:
        carta_a_remover = "ninguna"
    return [tiene_match, carta_a_remover, mano]

def agregar_carta_a_mano(mazo, mano):
    if mazo:
        nueva_carta = mazo.pop()
        mano.append(nueva_carta)
        return mano, mazo
    else:
        print("El mazo está vacío. Se mezclará un nuevo mazo.")
        mazo = crear_mazo()
        nueva_carta = mazo.pop()
        mano.append(nueva_carta)
        return mano, mazo

def puede_jugar(carta, carta_medio, color_elegido):
    if carta[0] == 'negro' or carta[1] == 'cambio de color':
        return True, color_elegido
    return carta[0] == carta_medio[0] or carta[1] == carta_medio[1], None

def recolectar_cartas_jugadas(cartas_jugadas, juego):
    juego.extend(cartas_jugadas)
    random.shuffle(juego)
    return juego

def jugar_computadora(mano, carta_medio, color_elegido):
    cartas_jugables = [carta for carta in mano[1] if puede_jugar(carta, carta_medio, color_elegido)[0]]

    if cartas_jugables:
        carta_jugada = random.choice(cartas_jugables)
        mano[1].remove(carta_jugada)
        return carta_jugada
    else:
        return None

# funcion agregada para decir uno cuando tire la ante ultima carta y le quede 1
def advertir_uno(jugadores, jugador_actual):
    #Calcula la longitud de la mano del jugador actual.
    if len(jugadores[jugador_actual][1]) == 1:
        print(f"¡UNO! {jugadores[jugador_actual][0]} tiene una carta restante.")
        
# funcion para calcular la puntuacion de los jugadores


def calcular_puntuacion(manos):
    puntuacion = {}
    for mano in manos:
        total_puntos = 0
         # Recorre cada carta en la mano actual
        for carta in mano[1]:
            if carta[1] == '+2' or carta[1] == 'Reversa' or carta[1] == 'Saltar':
                total_puntos += 20
            elif carta[0] == 'negro':
                total_puntos += 50
            else:
                total_puntos+= int(carta[1])
         # Asigna la puntuación total al diccionario con el nombre del jugador como clave
        puntuacion[mano[0]] = total_puntos
    return puntuacion

def mostrar_puntuacion(puntuacion):
    print("\n------Puntuación final--------")
    for jugador, puntos in puntuacion.items():
        print(f"{jugador}: {puntos} puntos")

def main():
    juego = crear_mazo()
    participantes = cant_jugadores()

    jugadores = [crear_jugador(f"Jugador {i+1}") for i in range(participantes)]
    jugadores[-1][0] = "Computadora"
    manos = repartir_cartas(juego, jugadores)

    carta_medio = poner_carta_medio(juego)


    jugador_actual = 0
    jugando = True
    color_elegido = None
    saltar = False  #se inicializa 'saltar' en false para que cuando toque esa carta se cambie a True
    sentido = "normal"

    while jugando:
        mano_actual = manos[jugador_actual]
        # if len(mano_actual[1]) == 1 and any(puede_jugar(carta, carta_medio, color_elegido)[0] for carta in mano_actual[1]):
        #     advertir_uno(jugadores, jugador_actual)

        print(f"\nEs el turno de {mano_actual[0]}")
        print()
        mostrar_carta_medio(carta_medio)

        if "Computadora" in mano_actual[0]:
            # if len(mano_actual[1]) == 2 and any(puede_jugar(carta, carta_medio, color_elegido)[0] for carta in mano_actual[1]):
            #     print()
            #     print("Computadora: ¡UNO!")
            carta_jugada = jugar_computadora(mano_actual, carta_medio, color_elegido)

            if carta_jugada is not None:
                print()
                print("La Computadora jugó una carta.")
                print(carta_jugada)
                carta_medio = carta_jugada
                if carta_jugada[1] == 'Reversa':
                    if sentido == "normal":
                        sentido = "inverso"
                        print()
                        print("¡El sentido del juego ha cambiado a inverso!")
                    else:
                        sentido = "normal"
                        print()
                        print("¡El sentido del juego ha vuelto a normal!")

                if carta_jugada[1] == 'Saltar':
                    saltar = True
                    print()
                    print(f"{mano_actual[0]} saltó al próximo jugador.")
                if carta_jugada[0] == 'negro':
                    color_elegido = random.choice(['azul', 'rojo', 'verde', 'amarillo'])
                    carta_medio = [color_elegido, -1]
                    print()
                    print('El color elegido es:', color_elegido)
                if carta_jugada[1] == '+4':
                    siguiente_jugador_indice = siguiente_jugador(jugador_actual, participantes, sentido, saltar)
                    for _ in range(4):
                        manos[siguiente_jugador_indice][1], juego = agregar_carta_a_mano(juego,
                                                                                          manos[siguiente_jugador_indice][
                                                                                              1])
                    print(f"¡{jugadores[siguiente_jugador_indice][0]} toma 4 cartas por la carta '+4'!")
                if carta_jugada[1] == '+2':
                    siguiente_jugador_indice = siguiente_jugador(jugador_actual, participantes, sentido, saltar)
                    for _ in range(2):
                        manos[siguiente_jugador_indice][1], juego = agregar_carta_a_mano(juego,
                                                                                          manos[siguiente_jugador_indice][
                                                                                              1])
                    print(f"¡{jugadores[siguiente_jugador_indice][0]} toma 2 cartas por la carta '+2'!")

            else:
                if juego:
                    print('Computadora no tiene cartas jugables, debe tomar del mazo')
                    mano_actual[1], juego = agregar_carta_a_mano(juego, mano_actual[1])
                else:
                    print("El mazo está vacío. Se mezclará un nuevo mazo")
                    juego = crear_mazo()
                    mano_actual[1] = agregar_carta_a_mano(juego, mano_actual[1])

            if len(mano_actual[1]) == 0:
                print(f"\n¡{mano_actual[0]} ganó la partida!")
                jugando = False
        else:
            print("\nEs tu turno. Esta es tu mano:")
            for i in range(len(mano_actual[1])):
                carta = mano_actual[1][i]
                print(f"{i + 1}: ({carta[0]}, {carta[1]})")

            cartas_jugables = [carta for carta in mano_actual[1] if puede_jugar(carta, carta_medio, color_elegido)[0]]

            if cartas_jugables:
                print("\nCartas jugables:")
                i = 1

                for carta in cartas_jugables:
                    print(f"{i}: {carta}")
                    i += 1

                try:
                    opcion = int(input("Elige el número de la carta que quieres jugar: ")) - 1

                    if 0 <= opcion < len(cartas_jugables):
                        carta_jugada = cartas_jugables[opcion]
                        resultado = puede_jugar(carta_jugada, carta_medio, color_elegido)

                        if resultado[0]:
                            mano_actual[1].remove(carta_jugada)
                            carta_medio = carta_jugada
                            print()

                            if carta_jugada[1] == 'Reversa':
                                if sentido == "normal":
                                    sentido = "inverso"
                                    print()
                                    print("¡El sentido del juego ha cambiado a inverso!")
                                else:
                                    sentido = "normal"
                                    print()
                                    print("¡El sentido del juego ha vuelto a normal!")

                            if carta_jugada[1] == 'Saltar':
                                saltar = True
                                print()
                                print(f"{mano_actual[0]} saltó al próximo jugador.")

                            if carta_jugada[0] == 'negro':
                                try:
                                    color_elegido = input("Elige un color (rojo, verde, azul, amarillo): ")
                                    assert color_elegido.lower() in ["rojo", "verde", "azul", "amarillo"]
                                    carta_medio = [color_elegido, -1]
                                except AssertionError:
                                    print()
                                    print("El valor ingresado no es correcto")
                                    print()
                                    print('Se colocara un color al azar.')
                                    color_elegido = random.choice(['azul', 'rojo', 'verde', 'amarillo'])
                                    carta_medio = [color_elegido, -1]

                            if carta_jugada[1] == '+4':
                                siguiente_jugador_indice = siguiente_jugador(jugador_actual, participantes,sentido, saltar)
                                for _ in range(4):
                                    manos[siguiente_jugador_indice][1], juego = agregar_carta_a_mano(juego,
                                                                                                      manos[
                                                                                                          siguiente_jugador_indice][
                                                                                                          1])
                                print(
                                    f"¡{jugadores[siguiente_jugador_indice][0]} toma 4 cartas por la carta '+4'!")
                            if carta_jugada[1] == '+2':
                                siguiente_jugador_indice = siguiente_jugador(jugador_actual, participantes, sentido, saltar)
                                for _ in range(2):
                                    manos[siguiente_jugador_indice][1], juego = agregar_carta_a_mano(juego,
                                                                                                      manos[
                                                                                                          siguiente_jugador_indice][
                                                                                                          1])
                                print(
                                    f"¡{jugadores[siguiente_jugador_indice][0]} toma 2 cartas por la carta '+2'!")

                            if len(mano_actual[1]) == 0:
                                print(f"\n¡{mano_actual[0]} ganó la partida!")
                                jugando = False

                        else:
                            print("No podés jugar esta carta en este momento. Perdés el turno.")
                    else:
                        print("Opción no válida. Perdés el turno.")
                except ValueError:
                    print("Por favor, ingresa un número válido.")
                except IndexError:
                    print("Opción no válida. Perdés el turno.")
            else:
                if juego:
                    print("No tenés cartas jugables. Tomá una del mazo.")
                    mano_actual[1], juego = agregar_carta_a_mano(juego, mano_actual[1])
                else:
                    print("El mazo está vacío. Se mezclará un nuevo mazo")
                    carta_medio = poner_carta_medio(juego)
                    jugando = False

        advertir_uno(jugadores, jugador_actual)
        jugador_actual = siguiente_jugador(jugador_actual, participantes, sentido, saltar)
        saltar = False  # Reiniciar la bandera de saltar en cada turno


        #cuando el mazo se queda sin cartas
        if not juego:
            #contiene todas las cartas jugadas durante el juego, excluyendo la carta que está actualmente en el medio del mazo 
            cartas_jugadas = [carta for mano in manos for carta in mano[1] if carta != carta_medio]
            juego = recolectar_cartas_jugadas(cartas_jugadas, juego)
            carta_medio = poner_carta_medio(juego)

    puntuacion_final = calcular_puntuacion(manos)
    mostrar_puntuacion(puntuacion_final)

# Programa principal
main()
