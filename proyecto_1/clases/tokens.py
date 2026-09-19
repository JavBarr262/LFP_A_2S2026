class Token:
    def __init__(self, numero, lexema, tipo, linea, columna):
        self.numero = numero
        self.lexema = lexema
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return "Token(#{}, '{}', {}, L{}:C{})".format(
            self.numero, self.lexema, self.tipo, self.linea, self.columna
        )

    def to_dict(self):
        return {
            "numero": self.numero,
            "lexema": self.lexema,
            "tipo": self.tipo,
            "linea": self.linea,
            "columna": self.columna,
        }

    class TipoToken:
        RESERVADA_BLOQUE = "RESERVADA_BLOQUE"
        RESERVADA_ELEMENTO = "RESERVADA_ELEMENTO"
        RESERVADA_RELACION = "RESERVADA_RELACION"
        CODIGO = "CODIGO"
        CADENA = "CADENA"
        HORA = "HORA"
        ENTERO = "ENTERO"
        DIA = "DIA"
        CATEGORIA = "CATEGORIA"
        IDENTIFICADOR = "IDENTIFICADOR"
        SIMBOLO = "SIMBOLO"
        COMENTARIO_LINEA = "COMENTARIO_LINEA"

    class TipoError:
        ERROR_CADENA = "ERROR_CADENA"
        ERROR_HORA = "ERROR_HORA"
        ERROR_ENTERO = "ERROR_ENTERO"
        ERROR_DIA = "ERROR_DIA"
        ERROR_IDENTIFICADOR = "ERROR_IDENTIFICADOR"