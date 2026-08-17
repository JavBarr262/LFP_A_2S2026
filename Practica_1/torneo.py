from clases import Tablero
from validaciones import val_intento

class Torneo:

    def __init__(self):
        self.sudokus = {}
        self.jugadores = {}
        self.intentos = []

    def cargar_sudokus(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{ruta}'.")
            return
        except OSError as e:
            print(f"Error al abrir el archivo '{ruta}': {e}")
            return

        self.sudokus = {}
        cargados=0
        for numero_linea, linea in enumerate(lineas, start=1):
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(",")
            if len(partes) != 3:
                print(f"Error en la línea {numero_linea}: Formato incorrecto. Se esperaba {linea}")
                continue

            id_sudoku, dificultad, tablero_str = partes
            tablero_str = tablero_str.strip()
            if len(tablero_str) != 81 or not tablero_str.isdigit():
                print(f"Error en la línea {numero_linea}: el tablero del sudokku{id_sudoku} es inválido no cumple con 81 digitos validos")
                continue
            try:
                tablero=Tablero(id_sudoku, dificultad, tablero_str)
                self.sudokus[tablero.id_sudoku]=tablero
                cargados +=1
            except ValueError as e:
                print(f"Error en la línea {numero_linea}: {e}")    
        print (f"sudokus cargados: {cargados} desde:{ruta}") 