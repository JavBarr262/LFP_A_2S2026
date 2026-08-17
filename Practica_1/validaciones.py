digitos_valido = set(range(1,10))

def validar_dig(valores):
    if len(valores)!= 9:
        return False
    return set(valores)== digitos_valido

def obtener_fila(matriz,indice_fila):
    return matriz[indice_fila]

def obtener_columna(matriz,indice_columna):
    return [matriz[fila][indice_columna] for fila in range(9)]

def obtener_cuadrante(matriz, fila, columna):
    fila_inicio = (fila // 3) * 3
    columna_inicio = (columna // 3) * 3
    cuadrante = []
    for i in range(fila_inicio, fila_inicio + 3):
        for j in range(columna_inicio, columna_inicio + 3):
            cuadrante.append(matriz[i][j])
    return cuadrante

def validar_pistas(tablero, intento):
    for fila in range(9):
        for columna in range(9):
            valor_original = tablero.matriz[fila][columna]
            valor_propuesto = intento.matriz_solucion[fila][columna]
            if valor_original != 0 and valor_original != valor_propuesto:
                return False
    return True

def val_intento(tablero,intento):
    matriz=intento.matriz_solucion

    intento.pistas_correctas=validar_pistas(tablero,intento)

    filas_validas=0
    for indice_fila in range(9):
        if validar_dig(obtener_fila(matriz, indice_fila)):
            filas_validas+=1

    columnas_validas=0
    for indice_columna in range(9):
        if validar_dig(obtener_columna(matriz, indice_columna)):
            columnas_validas+=1

    cuadrante_validas=0
    for cuadrante_fila in range(3):
        for cuadrante_columna in range(3):
            if validar_dig(obtener_cuadrante(matriz, cuadrante_fila, cuadrante_columna)):
                cuadrante_validas+=1

    intento.filas_validas=filas_validas
    intento.columnas_validas=columnas_validas
    intento.cuadrante_validas=cuadrante_validas

    grupos_totales_validos = filas_validas+columnas_validas+cuadrante_validas
    intento.porcentaje_valido= round((grupos_totales_validos/27)*100,2)

    intento.resuelto_correcto=(
        intento.porcentacje_certeza==100 and intento.pistas_correctas
    )

    return intento
