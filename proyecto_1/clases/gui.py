import os
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from errores import GestorErrores
from analizador_lexico import tokenizar_texto
from modelo import ConstructorModelo, detectar_choques
from reportes import GeneradorReportes

CARPETA_SALIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reportes")


class AplicacionProyecto1(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("proyecto_1 - Analizador Lexico")
        self.geometry("950x600")

        self.ruta_archivo = None
        self.rutas_reportes = {}

        self._construir_interfaz()

    def _construir_interfaz(self):
        barra = tk.Frame(self)
        barra.pack(fill="x", padx=8, pady=8)

        tk.Button(barra, text="Cargar .hor", width=12,
                  command=self.cargar_archivo).pack(side="left", padx=2)

        self.boton_analizar = tk.Button(barra, text="Analizar", width=12,
                                        command=self.analizar, state="disabled")
        self.boton_analizar.pack(side="left", padx=2)

        self.botones_reportes = {}
        for texto, clave in (("Reporte 1", "horario_semanal"),
                             ("Reporte 2", "carga_catedraticos"),
                             ("Reporte 3", "estadistico_general"),
                             ("Errores", "errores_lexicos")):
            b = tk.Button(barra, text=texto, width=10, state="disabled",
                          command=lambda k=clave: self.abrir_reporte(k))
            b.pack(side="left", padx=2)
            self.botones_reportes[clave] = b

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8)

        self._crear_pestana_preview()
        self._crear_pestana_tokens()
        self._crear_pestana_errores()

        self.estado = tk.Label(self, text="Listo.", anchor="w", relief="sunken")
        self.estado.pack(fill="x", side="bottom")

    def _crear_pestana_preview(self):
        marco = tk.Frame(self.notebook)
        self.notebook.add(marco, text="Archivo")
        self.texto_preview = tk.Text(marco, wrap="none", font=("Courier", 10))
        self.texto_preview.pack(fill="both", expand=True)

    def _crear_pestana_tokens(self):
        marco = tk.Frame(self.notebook)
        self.notebook.add(marco, text="Tokens")
        columnas = ("No.", "Lexema", "Tipo", "Linea", "Columna")
        self.tabla_tokens = self._crear_tabla(marco, columnas, (60, 240, 200, 70, 80))

    def _crear_pestana_errores(self):
        marco = tk.Frame(self.notebook)
        self.notebook.add(marco, text="Errores")
        columnas = ("No.", "Lexema", "Tipo de error", "Descripcion", "Linea", "Columna")
        self.tabla_errores = self._crear_tabla(marco, columnas,
                                               (50, 150, 180, 320, 60, 70))

    def _crear_tabla(self, marco, columnas, anchos):
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        for col, ancho in zip(columnas, anchos):
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho)
        scroll = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tabla

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo .hor",
            filetypes=[("Archivos proyecto_1", "*.hor"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except OSError as e:
            messagebox.showerror("Error al abrir archivo", str(e))
            return

        self.ruta_archivo = ruta
        self.texto_preview.delete("1.0", "end")
        self.texto_preview.insert("1.0", contenido)
        self.boton_analizar.config(state="normal")
        self.estado.config(text="Cargado: " + os.path.basename(ruta))

    def analizar(self):
        if not self.ruta_archivo:
            return

        with open(self.ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()

        gestor = GestorErrores()
        tokens = tokenizar_texto(contenido, gestor)
        horario = ConstructorModelo(tokens).construir()
        conflictos = detectar_choques(horario)
        errores = gestor.obtener_errores()

        self._poblar_tokens(tokens)
        self._poblar_errores(errores)

        generador = GeneradorReportes(horario, tokens, errores, CARPETA_SALIDA)
        self.rutas_reportes = generador.generar_todos()
        for boton in self.botones_reportes.values():
            boton.config(state="normal")

        self.estado.config(text="{} tokens | {} errores | {} clases | {} choques".format(
            len(tokens), len(errores), len(horario.clases), len(conflictos)))
        self.notebook.select(1)

    def _poblar_tokens(self, tokens):
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        for t in tokens:
            self.tabla_tokens.insert("", "end",
                                     values=(t.numero, t.lexema, t.tipo, t.linea, t.columna))

    def _poblar_errores(self, errores):
        self.tabla_errores.delete(*self.tabla_errores.get_children())
        for e in errores:
            self.tabla_errores.insert("", "end",
                                      values=(e.numero, e.lexema, e.tipo_error,
                                              e.descripcion, e.linea, e.columna))

    def abrir_reporte(self, clave):
        ruta = self.rutas_reportes.get(clave)
        if ruta:
            webbrowser.open("file://" + os.path.abspath(ruta))


def main():
    app = AplicacionProyecto1()
    app.mainloop()


if __name__ == "__main__":
    main()
