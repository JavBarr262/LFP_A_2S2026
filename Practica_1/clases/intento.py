class Intento:

    def __init__(self, carnet, id_sudoku, solucion, tiempo_segundos, fecha):
        self.carnet=int(carnet)
        self.id_sudoku=int(id_sudoku)
        self.cadena_solucion=solucion
        self.tiempo_segundos=int(tiempo_segundos)
        self.fecha=fecha.strip()
        self.matriz_solucion=self._contruir_matriz(solucion)

        self.pistas_respetadas = None
        self.filas_validas = 0
        self.columnas_validas = 0
        self.cajas_validas = 0
        self.porcentaje_validez = 0.0
        self.resuelto_correctamente = False

    @staticmethod
    def _contruir_matriz(cadena):
        matriz=[]
        for fila in range(9):
            fila_valores=[]
            for columna in range(9):
                indice=fila*9+columna
                fila_valores.append(int(cadena[indice]))
            matriz.append(fila_valores)
        return matriz

    def __repr__(self):
        return(f"intento carnet={self.carnet}, id_sudoku={self.id_sudoku}," f"validacion={self,self.porcentaje_validez}%. resuelto={self.resuelto_correctamente}")