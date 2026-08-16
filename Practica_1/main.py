"Menu principal"

import os

def mostrar_menu():
    print("\n-------------------")
    print(" Numerix - Torneo de Sudoku")
    print("---------------------")
    print("1) Subir archivos de los sudokus")
    print("2) Subir datos de los jugadores")
    print("3) Subir datos de los intentos")
    print("4) Validadar los puntajes e intentos")
    print("5) Generar reporte Resumen por sudoku")
    print("6) Generar reporte Rendimiento de los jugadores")
    print("7) Generar reporte TOP 10 mejores jugadores")
    print("8) Finalizar tarea")

def menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-8): ")

        if opcion == "1":
            print("Opcion 1 seleccionada: Subir archivos de los sudokus")
            # Lógica para subir archivos de sudokus
        elif opcion == "2":
            print("Opcion 2 seleccionada: Subir datos de los jugadores")
            # Lógica para subir datos de jugadores
        elif opcion == "3":
            print("Opcion 3 seleccionada: Subir datos de los intentos")
            # Lógica para subir datos de intentos
        elif opcion == "4":
            print("Opcion  4 seleccionada: Validar los puntajes e intentos")
            # Lógica para validar puntajes e intentos
        elif opcion == "5":
            print("Opcion 5 seleccionada: Generar reporte Resumen por sudoku")
            # Lógica para generar reporte resumen por sudoku
        elif opcion == "6":
            print("Opcion 6 seleccionada: Generar reporte Rendimiento de los jugadores")
            # Lógica para generar reporte de rendimiento de los jugadores   
        elif opcion == "7":
            print("Opcion 7 seleccionada: Generar reporte TOP 10 mejores jugadores")
            # Lógica para generar reporte de los top 10 mejores jugadores
        elif opcion == "8":
            print("Opcion 8 seleccionada: Finalizar tarea")
            # Lógica para finalizar la tarea
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

menu()