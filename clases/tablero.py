class Tablero:

    def __init__(self, id_sudoku, dificultad, cadena):
        self.id_sudoku = int(id_sudoku)
        self.dificultad = dificultad.strip()
        self.cadena_original = cadena
        self.matriz = self._construir_matriz(cadena)

    @staticmethod
    def _construir_matriz(cadena):
        matriz = []
        for fila in range(9):
            fila_valores = []
            for columna in range(9):
                indice = fila * 9 + columna
                fila_valores.append(int(cadena[indice]))
            matriz.append(fila_valores)
        return matriz

    def obtener_valor(self, fila, columna):
        return self.matriz[fila][columna]

    def es_pista(self, fila, columna):
        return self.matriz[fila][columna]!= 0

    def __repr__(self):
        return f"Tablero(id={self.id_sudoku}, dificultad='{self.dificultad}')"