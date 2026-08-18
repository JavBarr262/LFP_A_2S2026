ESTILO_CSS = """
<style>
    table { border-collapse: collapse; }
    th, td { border: 1px solid #333; padding: 6px 10px; text-align: left; }
</style>
"""

def encabezado(titulo):
    return f""" <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
        {ESTILO_CSS}
    </head>
    <body>
         <h1>{titulo}</h1>
"""

def pie_pagina():
    return"""
    </body>
    </html> 
    """

def generar_rep_sudoku(estadisticas, ruta_salida):
    html=[encabezado(" Resumen Sudokus")]
    html.append("<table>")
    html.append("<tr><th>ID Sudoku</th><th>Dificultad </th><th> Cantidad intentos</th> <th>Tiempo promedio (s)</th><th> Porcentaje exito % </th></tr>" )

    for id_sudoku in sorted(estadisticas.keys()):
        datos=estadisticas[id_sudoku]
        html.append("<tr>" f"<td>{id_sudoku}</td>" f"<td>{datos['dificultad']}</td>" f"<td>{datos['cantidad_intentos']}</td>" f"<td>{datos['tiempo_promedio']}</td>" f"<td>{datos['tasa_exito']}%</td>" "</tr>")

    html.append("</table>")
    html.append(pie_pagina())

    with open(ruta_salida,"w",encoding="utf-8") as archivo:
        archivo.write("".join(html))

def generar_rep_jugador(estadisticas, ruta_salida):
    html=[encabezado(" rendimiento jugadores")]
    html.append("<table>")
    html.append("<tr><th>Carnet</th><th>Nombre Completo</th><th>Nivel</th>" "<th>Tableros Intentados</th><th>% Validar Promedio</th>" "<th>Tiempo Promedio (s)</th><th>Resueltos Perfectamente</th></tr>")

    for carnet in sorted(estadisticas.keys()):
        datos= estadisticas[carnet]
        html.append( "<tr>" f"<td>{carnet}</td>" f"<td>{datos['nombre_completo']}</td>" f"<td>{datos['nivel']}</td>" f"<td>{datos['cantidad_tableros']}</td>" f"<td>{datos['validar_promedio']}%</td>" f"<td>{datos['tiempo_promedio']}</td>" f"<td>{datos['resuelto_correcto']}</td>" "</tr>")
    html.append("</table>")
    html.append(pie_pagina())

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write("".join(html))

def generar_rep_top10(mejores10, ruta_salida):
    html=[encabezado("Top 10 mejores tiempos")]
    html.append("<table>")
    html.append("<tr><th>Posicion</th><th>Carnet</th><th>Nombre completo</th><th>ID Sudoku</th><th>Dificultad</th><th>Tiempo (s)</th></tr>")

    if not mejores10:
        html.append("<tr><td >No se han cargados intentos</td></tr>")
    else:
        for registro in mejores10:
            html.append("<tr>" f"<td>{registro['posicion']}</td>"  f"<td>{registro['carnet']}</td>" f"<td>{registro['nombre_completo']}</td>" f"<td>{registro['id_sudoku']}</td>" f"<td>{registro['dificultad']}</td>" f"<td>{registro['tiempo']}</td>" "</tr>")

    html.append("</table>")
    html.append(pie_pagina())

    with open(ruta_salida,"w", encoding="utf-8") as archivo:
        archivo.write("".join(html))
        