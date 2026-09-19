class ErrorLexico:
    def __init__(self, numero, lexema, tipo_error, descripcion, linea, columna):
        self.numero = numero
        self.lexema = lexema
        self.tipo_error = tipo_error
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return "ErrorLexico(#{}, '{}', {}, L{}:C{})".format(
            self.numero, self.lexema, self.tipo_error, self.linea, self.columna
        )
    def to_dict(self):
        return {
            "numero": self.numero,
            "lexema": self.lexema,
            "tipo_error": self.tipo_error,
            "descripcion": self.descripcion,
            "linea": self.linea,
            "columna": self.columna,
        }

class GestorErrores:
        """
        Acumula errores lexicos en una lista, sin detener nunca el analisis.
        """

        def __init__(self):
            self._errores = []
            self._contador = 0

        def reportar(self, lexema, tipo_error, descripcion, linea, columna):
            self._contador += 1
            error = ErrorLexico(
                numero=self._contador,
                lexema=lexema,
                tipo_error=tipo_error,
                descripcion=descripcion,
                linea=linea,
                columna=columna,
            )
            self._errores.append(error)
            return error
        
        def hay_errores(self):
            return len(self._errores) > 0

        def total_errores(self):
            return len(self._errores)

        def obtener_erroer(self):
            return list(self._errores)

        def limpiar(self):
            self._errores=[]
            self._contador=0
