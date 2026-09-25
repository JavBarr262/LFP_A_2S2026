import os

DIAS_ORDEN = ("LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO")

CSS_BASE = """
body { font-family: Arial, sans-serif; margin: 20px; color: #222; }
h1 { font-size: 20px; border-bottom: 2px solid #333; padding-bottom: 6px; }
h2 { font-size: 16px; margin-top: 24px; }
table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
th, td { border: 1px solid #999; padding: 6px 8px; font-size: 13px; text-align: left; }
th { background: #ddd; }
.verde { background: #cfc; }
.rojo { background: #fcc; }
.azul { background: #ccf; }
.naranja { background: #fe9; }
ul { font-size: 14px; }
"""


def _escape(texto):
    if texto is None:
        return ""
    texto = str(texto)
    texto = texto.replace("&", "&amp;")
    texto = texto.replace("<", "&lt;")
    texto = texto.replace(">", "&gt;")
    texto = texto.replace('"', "&quot;")
    return texto


def _hora_a_minutos(hora_str):
    if hora_str is None or len(hora_str) != 5 or hora_str[2] != ":":
        return None
    try:
        h = int(hora_str[0:2])
        m = int(hora_str[3:5])
    except ValueError:
        return None
    return h * 60 + m


def _nivel_carga(horas):
    if horas <= 4:
        return "BAJA", "azul"
    if horas <= 10:
        return "NORMAL", "verde"
    if horas <= 15:
        return "ALTA", "naranja"
    return "SATURADA", "rojo"


def _envoltorio_html(titulo, cuerpo):
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<style>{css}</style>
</head>
<body>
<h1>{titulo}</h1>
{cuerpo}
</body>
</html>""".format(titulo=titulo, css=CSS_BASE, cuerpo=cuerpo)


class GeneradorReportes:
    def __init__(self, horario, tokens, errores, carpeta_salida):
        self.horario = horario
        self.tokens = tokens
        self.errores = errores
        self.carpeta_salida = carpeta_salida
        os.makedirs(self.carpeta_salida, exist_ok=True)

    def _guardar(self, nombre_archivo, contenido):
        ruta = os.path.join(self.carpeta_salida, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return ruta

    def generar_reporte_horario_semanal(self):
        secciones = {}
        for c in self.horario.clases:
            secciones.setdefault(c.seccion or "GENERAL", []).append(c)

        partes = []
        for sec in sorted(secciones.keys()):
            partes.append("<h2>Seccion: {}</h2>".format(_escape(sec)))
            partes.append("<table>")
            partes.append("<tr><th>Dia</th><th>Inicio</th><th>Fin</th>"
                          "<th>Curso</th><th>Catedratico</th><th>Aula</th>"
                          "<th>Estado</th></tr>")

            clases = sorted(
                secciones[sec],
                key=lambda c: (DIAS_ORDEN.index(c.dia) if c.dia in DIAS_ORDEN else 99,
                               c.inicio or ""),
            )
            for c in clases:
                curso = self.horario.cursos.get(c.curso_codigo)
                cat = self.horario.catedraticos.get(c.catedratico_codigo)
                color = "rojo" if c.choque else "verde"
                estado = "CHOQUE DE HORARIO" if c.choque else "CONFIRMADO"
                partes.append(
                    "<tr class='{color}'><td>{dia}</td><td>{ini}</td><td>{fin}</td>"
                    "<td>{curso}</td><td>{cat}</td><td>{aula}</td>"
                    "<td>{estado}</td></tr>".format(
                        color=color,
                        dia=_escape(c.dia or "-"),
                        ini=_escape(c.inicio or "-"),
                        fin=_escape(c.fin or "-"),
                        curso=_escape(curso.nombre if curso else c.curso_codigo),
                        cat=_escape(cat.nombre if cat else c.catedratico_codigo),
                        aula=_escape(c.aula_codigo or "-"),
                        estado=estado,
                    )
                )
            partes.append("</table>")

        if not secciones:
            partes.append("<p>No se registraron clases en el archivo analizado.</p>")

        html = _envoltorio_html("Reporte 1 - Horario Semanal por Seccion",
                                "\n".join(partes))
        return self._guardar("reporte_horario_semanal.html", html)

    def generar_reporte_carga_catedraticos(self):
        minutos_por_catedratico = {}
        for c in self.horario.clases:
            ini = _hora_a_minutos(c.inicio)
            fin = _hora_a_minutos(c.fin)
            minutos = fin - ini if (ini is not None and fin is not None and fin > ini) else 0
            minutos_por_catedratico[c.catedratico_codigo] = (
                minutos_por_catedratico.get(c.catedratico_codigo, 0) + minutos
            )

        partes = ["<table>",
                  "<tr><th>Catedratico</th><th>Categoria</th>"
                  "<th>Horas semanales</th><th>Clases</th><th>Nivel de carga</th></tr>"]

        conteo_clases = {}
        for c in self.horario.clases:
            conteo_clases[c.catedratico_codigo] = conteo_clases.get(c.catedratico_codigo, 0) + 1

        for codigo, cat in sorted(self.horario.catedraticos.items()):
            minutos = minutos_por_catedratico.get(codigo, 0)
            horas = round(minutos / 60.0, 2)
            nivel, color = _nivel_carga(horas)
            partes.append(
                "<tr class='{color}'><td>{nombre}</td><td>{categoria}</td>"
                "<td>{horas}</td><td>{clases}</td><td>{nivel}</td></tr>".format(
                    color=color,
                    nombre=_escape(cat.nombre),
                    categoria=_escape(cat.categoria or "-"),
                    horas=horas,
                    clases=conteo_clases.get(codigo, 0),
                    nivel=nivel,
                )
            )
        partes.append("</table>")

        if not self.horario.catedraticos:
            partes.append("<p>No se registraron catedraticos en el archivo analizado.</p>")

        html = _envoltorio_html("Reporte 2 - Carga de Catedraticos", "\n".join(partes))
        return self._guardar("reporte_carga_catedraticos.html", html)

    def generar_reporte_estadistico(self):
        BLOQUES_DISPONIBLES = 18  

        choques = sum(1 for c in self.horario.clases if c.choque)

        carga = {}
        for c in self.horario.clases:
            ini = _hora_a_minutos(c.inicio)
            fin = _hora_a_minutos(c.fin)
            minutos = fin - ini if (ini is not None and fin is not None and fin > ini) else 0
            carga[c.catedratico_codigo] = carga.get(c.catedratico_codigo, 0) + minutos

        mayor_codigo = None
        mayor_minutos = 0
        for codigo, minutos in carga.items():
            if minutos > mayor_minutos:
                mayor_minutos = minutos
                mayor_codigo = codigo
        cat_mayor = self.horario.catedraticos.get(mayor_codigo)
        nombre_mayor = cat_mayor.nombre if cat_mayor else (mayor_codigo or "N/A")

        promedio = 0.0
        if self.horario.catedraticos:
            promedio = round(sum(carga.values()) / 60.0 / len(self.horario.catedraticos), 2)

        ocupacion = {}
        for c in self.horario.clases:
            ocupacion[c.aula_codigo] = ocupacion.get(c.aula_codigo, 0) + 1

        filas_aulas = []
        for codigo in self.horario.aulas:
            n = ocupacion.get(codigo, 0)
            pct = round(n / BLOQUES_DISPONIBLES * 100, 1)
            filas_aulas.append((pct, codigo, n))
        filas_aulas.sort(reverse=True)

        aula_top = filas_aulas[0][1] if filas_aulas else "N/A"
        pct_top = filas_aulas[0][0] if filas_aulas else 0

        partes = [
            "<h2>Indicadores generales</h2>",
            "<ul>",
            "<li>Total de cursos: {}</li>".format(len(self.horario.cursos)),
            "<li>Total de catedraticos: {}</li>".format(len(self.horario.catedraticos)),
            "<li>Total de aulas: {}</li>".format(len(self.horario.aulas)),
            "<li>Total de clases programadas: {}</li>".format(len(self.horario.clases)),
            "<li>Clases involucradas en choques de horario: {}</li>".format(choques),
            "<li>Catedratico con mayor carga: {} ({} hrs)</li>".format(
                _escape(nombre_mayor), round(mayor_minutos / 60.0, 2)),
            "<li>Aula con mayor ocupacion: {} ({}%)</li>".format(
                _escape(aula_top), pct_top),
            "<li>Promedio de horas por catedratico: {}</li>".format(promedio),
            "</ul>",
            "<h2>Ocupacion por aula</h2>",
            "<table>",
            "<tr><th>Aula</th><th>Clases asignadas</th><th>% Ocupacion</th></tr>",
        ]
        for pct, codigo, n in filas_aulas:
            color = " class='rojo'" if pct > 80 else ""
            partes.append("<tr{color}><td>{codigo}</td><td>{n}</td>"
                          "<td>{pct}%</td></tr>".format(
                              color=color, codigo=_escape(codigo), n=n, pct=pct))
        partes.append("</table>")

        html = _envoltorio_html("Reporte 3 - Estadistico General del Ciclo",
                                "\n".join(partes))
        return self._guardar("reporte_estadistico_general.html", html)

    def generar_reporte_errores(self):
        partes = ["<table>",
                  "<tr><th>#</th><th>Lexema</th><th>Tipo de Error</th>"
                  "<th>Descripcion</th><th>Linea</th><th>Columna</th></tr>"]
        for e in self.errores:
            partes.append(
                "<tr class='rojo'><td>{n}</td><td>{lex}</td><td>{tipo}</td>"
                "<td>{desc}</td><td>{l}</td><td>{c}</td></tr>".format(
                    n=e.numero, lex=_escape(e.lexema), tipo=_escape(e.tipo_error),
                    desc=_escape(e.descripcion), l=e.linea, c=e.columna))
        partes.append("</table>")
        if not self.errores:
            partes.append("<p>No se detectaron errores lexicos.</p>")

        html = _envoltorio_html("Reporte de Errores Lexicos", "\n".join(partes))
        return self._guardar("reporte_errores_lexicos.html", html)

    def generar_dot_afd(self):
        dot = """digraph AFD_Proyecto1 {
    rankdir=LR;
    node [shape=circle, fontsize=10];
    edge [fontsize=9];

    q0 [label="q0\\n(inicio)", shape=doublecircle, style=filled, fillcolor="#dfe9f5"];

    q0 -> qC1 [label="#"];
    qC1 -> qC2 [label="#"];
    qC2 -> qC2 [label="cualquier char != \\\\n"];
    qC2 -> qACEPTA_COMENTARIO [label="\\\\n / EOF"];
    qACEPTA_COMENTARIO [shape=doublecircle, style=filled, fillcolor="#c8e6c9",
                         label="ACEPTA\\nCOMENTARIO_LINEA"];

    q0 -> qS1 [label="\\""];
    qS1 -> qS1 [label="char != \\" ,  != \\\\n"];
    qS1 -> qACEPTA_CADENA [label="\\""];
    qS1 -> qERROR_CADENA [label="\\\\n / EOF"];
    qACEPTA_CADENA [shape=doublecircle, style=filled, fillcolor="#c8e6c9",
                    label="ACEPTA\\nCADENA"];
    qERROR_CADENA [shape=doublecircle, style=filled, fillcolor="#ffcdd2",
                   label="ERROR\\nCADENA_SIN_CERRAR"];

    q0 -> qN1 [label="digito"];
    qN1 -> qN1 [label="digito"];
    qN1 -> qACEPTA_ENTERO [label="otro (no ':')"];
    qACEPTA_ENTERO [shape=doublecircle, style=filled, fillcolor="#c8e6c9",
                    label="ACEPTA\\nENTERO"];
    qN1 -> qH1 [label=":"];
    qH1 -> qH1 [label="digito"];
    qH1 -> qACEPTA_HORA [label="otro"];
    qACEPTA_HORA [shape=doublecircle, style=filled, fillcolor="#c8e6c9",
                  label="ACEPTA HORA\\n(valida rango 06:00-21:00)"];

    q0 -> qA1 [label="letra"];
    qA1 -> qA1 [label="letra | digito"];
    qA1 -> qCOD1 [label="-"];
    qCOD1 -> qCOD1 [label="digito"];
    qCOD1 -> qACEPTA_CODIGO [label="otro (>=1 digito leido)"];
    qCOD1 -> qERROR_CODIGO [label="otro (0 digitos leidos)"];
    qACEPTA_CODIGO [shape=doublecircle, style=filled, fillcolor="#c8e6c9",
                    label="ACEPTA\\nCODIGO"];
    qERROR_CODIGO [shape=doublecircle, style=filled, fillcolor="#ffcdd2",
                   label="ERROR\\nCODIGO_MAL_FORMADO"];

    qA1 -> qACEPTA_PALABRA [label="otro"];
    qACEPTA_PALABRA [shape=doublecircle, style=filled, fillcolor="#c8e6c9",
                     label="ACEPTA\\n(clasificar: RESERVADA / DIA /\\nCATEGORIA / IDENTIFICADOR)"];

    q0 -> qACEPTA_SIMBOLO [label="{ } [ ] : , ;"];
    qACEPTA_SIMBOLO [shape=doublecircle, style=filled, fillcolor="#c8e6c9",
                     label="ACEPTA\\nSIMBOLO"];

    q0 -> q0 [label="espacio | \\\\n | tab (no genera token)"];

    q0 -> qERROR_CHAR [label="otro caracter"];
    qERROR_CHAR [shape=doublecircle, style=filled, fillcolor="#ffcdd2",
                 label="ERROR\\nCARACTER_NO_RECONOCIDO"];
}
"""
        return self._guardar("afd_proyecto1.dot", dot)

    def generar_diagrama_afd_html(self):
        ruta_dot = self.generar_dot_afd()
        with open(ruta_dot, "r", encoding="utf-8") as f:
            codigo_dot = f.read()

        try:
            import graphviz
            fuente = graphviz.Source(codigo_dot)
            svg_bytes = fuente.pipe(format="svg")
            svg_texto = svg_bytes.decode("utf-8")
            inicio = svg_texto.find("<svg")
            cuerpo = "<div style='overflow:auto; border:1px solid #999; padding:10px;'>" \
                     + svg_texto[inicio:] + "</div>"
        except Exception as error:
            cuerpo = (
                "<p><b>No se pudo renderizar el diagrama automaticamente</b> "
                "({}).</p>"
                "<p>Instala Graphviz (<a href='https://graphviz.org/download/'>"
                "graphviz.org/download</a>) y asegurate de que el comando "
                "<code>dot</code> este en el PATH del sistema, o abre el "
                "archivo <code>afd_proyecto1.dot</code> con cualquier visor "
                "de Graphviz (por ejemplo "
                "<a href='https://dreampuf.github.io/GraphvizOnline/'>"
                "GraphvizOnline</a>).</p>"
                "<h2>Codigo DOT</h2>"
                "<pre style='background:#f4f4f4; padding:10px; overflow:auto;'>{}</pre>"
            ).format(_escape(str(error)), _escape(codigo_dot))

        html = _envoltorio_html("Diagrama del AFD (renderizado con Graphviz)", cuerpo)
        return self._guardar("diagrama_afd.html", html)

    def generar_todos(self):
        return {
            "horario_semanal": self.generar_reporte_horario_semanal(),
            "carga_catedraticos": self.generar_reporte_carga_catedraticos(),
            "estadistico_general": self.generar_reporte_estadistico(),
            "errores_lexicos": self.generar_reporte_errores(),
            "afd_dot": self.generar_dot_afd(),
            "diagrama_afd": self.generar_diagrama_afd_html(),
        }
