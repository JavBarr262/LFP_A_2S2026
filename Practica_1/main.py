"Menu principal"

import os
from torneo import Torneo
from validaciones import val_intento

carpeta_reportes="reportes"

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

def definir_ruta(ruta_predeterminada):
    ruta = input(f"Introduzca la ruta del archivo (por defecto: {ruta_predeterminada}): ").strip()
    return ruta if ruta else ruta_predeterminada

def Validar_carpeta_reportes():
    carpeta_reportes = "reportes"
    if not os.path.exists(carpeta_reportes):
        os.makedirs(carpeta_reportes)
        print(f"Se ha creado la carpeta '{carpeta_reportes}' para los reportes.")
    else:
        print(f"La carpeta '{carpeta_reportes}' ya existe.")

def menu():
    Validar_carpeta_reportes()
    torneo=Torneo()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-8): ").strip()

        if opcion == "1":
            print("Opcion 1 seleccionada: Subir archivos de los sudokus")
            ruta= definir_ruta("datos/sudokus.lfp")
            torneo.cargar_sudokus(ruta)
        elif opcion == "2":
            print("Opcion 2 seleccionada: Subir datos de los jugadores")

        elif opcion == "3":
            print("Opcion 3 seleccionada: Subir datos de los intentos")

        elif opcion == "4":
            print("Opcion  4 seleccionada: Validar los puntajes e intentos")
            torneo.validar_todos_los_intentos()
        elif opcion == "5":
            print("Opcion 5 seleccionada: Generar reporte Resumen por sudoku")
        elif opcion == "6":
            print("Opcion 6 seleccionada: Generar reporte Rendimiento de los jugadores")
        elif opcion == "7":
            print("Opcion 7 seleccionada: Generar reporte TOP 10 mejores jugadores")
        elif opcion == "8":
            print("Opcion 8 seleccionada: Finalizar tarea")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

menu()