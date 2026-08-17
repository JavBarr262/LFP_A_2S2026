from clases import Tablero, Jugador, Intento
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


    def cargar_jugadores(self, ruta):
        try:
            with open(ruta, "r", encoding="utf=8") as archivo:
             lineas=archivo.readlines()
        except FileNotFoundError:
              print(f"No se encontro el archivo {ruta}")
              return
        except OSError as e:
            print(f"Error al abrir el archivo {ruta} {e}")
            return
        self.jugadores={}
        cargados=0
        for numero_linea, linea in enumerate(lineas, start=1):
            linea=linea.strip()
            if not linea:
                continue
            partes=linea.split(",")
            if len(partes)!=4:
                print(f"Error en linea {numero_linea}formato incorrecto en {linea}")
                continue

            carnet, nombre, apellido, nivel=partes
            try:
                jugador=Jugador(carnet,nombre,apellido,nivel)
                self.jugadores[jugador.carnet]=jugador
                cargados+=1
            except ValueError as e:
                print(f"error en linea {numero_linea} no se pudo crear el jugador{e}")

        print(f"Jugadores cargados {cargados} desde {ruta}")

    def cargar_intentos(self, ruta):
        try:
            with open(ruta,"r", encoding="utf-8") as archivo:
                lineas=archivo.readlines()
        except FileNotFoundError:
            print(f"no se encontro el acrhivo {ruta}")
            return
        except OSError as e:
            print(f"error al abrir el archivo {ruta} {e}")
            return

        self.intentos=[]
        cargados=0
        for numero_linea, linea in enumerate(lineas, start=1):
            linea=linea.strip()
            if not linea:
                continue
            partes=linea.split(",")
            if len(partes) !=5:
                print(f"error en linea {numero_linea} formato incorrecto en {linea}")
                continue

            carnet, id_sudoku,solucion, tiempo_segundos, fecha=partes
            solucion=solucion.strip()
            if len(solucion) != 81 or not solucion.isdigit():
                print(f"error en linea {numero_linea} la solucion no tiene 81 digitos validos")
                continue
            try:
                intento=Intento(carnet, id_sudoku, solucion, tiempo_segundos, fecha)
                self.intentos.append(intento)
                cargados+=1
            except ValueError as e:
                print(f"erro en linea {numero_linea} no se pudo crear intento {e}")

        print(f"intetnos cargados={cargados} desde {ruta}")


    