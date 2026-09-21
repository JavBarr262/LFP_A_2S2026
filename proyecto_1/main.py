import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "clases"))


def ejecutar_consola(ruta_archivo):
    from errores import GestorErrores
    from analizador_lexico import tokenizar_texto
    from modelo import ConstructorModelo, detectar_choques
    from reportes import GeneradorReportes

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    gestor_errores = GestorErrores()
    tokens = tokenizar_texto(contenido, gestor_errores)

    constructor = ConstructorModelo(tokens)
    horario = constructor.construir()
    conflictos = detectar_choques(horario)

    errores = gestor_errores.obtener_errores()

    carpeta_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)),"reportes")
    generador = GeneradorReportes(horario, tokens, errores, carpeta_salida)
    rutas = generador.generar_todos()

    print("Archivo analizado: {}".format(ruta_archivo))
    print("-" * 60)
    print("Tokens reconocidos   : {}".format(len(tokens)))
    print("Errores lexicos       : {}".format(len(errores)))
    print("Cursos                : {}".format(len(horario.cursos)))
    print("Catedraticos          : {}".format(len(horario.catedraticos)))
    print("Aulas                 : {}".format(len(horario.aulas)))
    print("Clases                : {}".format(len(horario.clases)))
    print("Choques de horario    : {}".format(len(conflictos)))
    print("-" * 60)
    print("Reportes generados en: {}".format(carpeta_salida))
    for nombre, ruta in rutas.items():
        print("  - {}: {}".format(nombre, ruta))

    if errores:
        print("-" * 60)
        print("Detalle de errores lexicos:")
        for e in errores:
            print("  #{} [{}] '{}' (L{}:C{}) -> {}".format(
                e.numero, e.tipo_error, e.lexema, e.linea, e.columna, e.descripcion
            ))

def main():
    if len(sys.argv) > 1:
        ejecutar_consola(sys.argv[1])
    else:
        from gui import main as gui_main
        gui_main()


if __name__ == "__main__":
    main()
