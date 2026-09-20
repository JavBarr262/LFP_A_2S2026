from tokens import Token, TipoToken, TipoError

PALABRAS_BLOQUE = ("HORARIO", "CURSOS", "CATEDRATICOS", "AULAS", "CLASES")
PALABRAS_ELEMENTO = ("curso", "catedratico", "aula", "clase")
PALABRAS_RELACION = ("con", "en")
DIAS_VALIDOS = ("LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO")
CATEGORIAS_VALIDAS = ("TITULAR", "INTERINO", "AUXILIAR")
SIMBOLOS_VALIDOS = ("{", "}", "[", "]", ":", ",", ";")
HORA_MIN_MINUTOS = 6 * 60       
HORA_MAX_MINUTOS = 21 * 60      

def _es_letra(c):
    return ("a" <= c <= "z") or ("A" <= c <= "Z")

def _es_digito(c):
    return "0" <= c <= "9"

def _es_alfanumerico(c):
    return _es_letra(c) or _es_digito(c)

def _es_espacio(c):
    return c == " " or c == "\t" or c == "\r"

def _es_mayusculas(palabra):
    for c in palabra:
        if not ("A" <= c <= "Z"):
            return False
    return len(palabra) > 0


def _entero_desde_digitos(digitos):
    try:
        return int(digitos)
    except ValueError:
        return None


class AnalizadorLexico:
    def __init__(self, texto, gestor_errores):
        self.texto = texto
        self.longitud = len(texto)
        self.pos = 0
        self.linea = 1
        self.columna = 1
        self.contador_tokens = 0
        self.gestor_errores = gestor_errores
        self._ultimo_identificador = None

    def _actual(self):
        if self.pos >= self.longitud:
            return None
        return self.texto[self.pos]

    def _siguiente_caracter(self, offset=1):
        idx = self.pos + offset
        if idx >= self.longitud:
            return None
        return self.texto[idx]

    def _avanzar(self):
        c = self.texto[self.pos]
        self.pos += 1
        if c == "\n":
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        return c

    def _nuevo_numero_token(self):
        self.contador_tokens += 1
        return self.contador_tokens

    def _saltar_espacios(self):
        while self.pos < self.longitud:
            c = self.texto[self.pos]
            if c == "\n" or _es_espacio(c):
                self._avanzar()
            else:
                break

    def _reconocer_comentario(self, linea_inicial, columna_inicial):
        letras = []
        letras.append(self._avanzar())  
        letras.append(self._avanzar())  
        while self.pos < self.longitud and self.texto[self.pos] != "\n":
            letras.append(self._avanzar())
        lexema = "".join(letras)
        return Token(self._nuevo_numero_token(), lexema, TipoToken.COMENTARIO_LINEA,
                     linea_inicial, columna_inicial)

    def _reconocer_cadena(self, linea_inicial, columna_inicial):
        letras = []
        letras.append(self._avanzar())  
        cerrada = False
        while self.pos < self.longitud:
            c = self.texto[self.pos]
            if c == '"':
                letras.append(self._avanzar())
                cerrada = True
                break
            if c == "\n":
                break
            letras.append(self._avanzar())
        lexema = "".join(letras)

        if not cerrada:
            self.gestor_errores.reportar(
                lexema=lexema,
                tipo_error=TipoError.CADENA_SIN_CERRAR,
                descripcion="Cadena sin cerrar iniciada en línea {}, columna {}".format(
                    linea_inicial, columna_inicial
                ),
                linea=linea_inicial,
                columna=columna_inicial,
            )
        return Token(self._nuevo_numero_token(), lexema, TipoToken.CADENA,
                     linea_inicial, columna_inicial)

    def _reconocer_numero_u_hora(self, linea_inicial, columna_inicial):
        digitos_izquierda = []
        while self.pos < self.longitud and _es_digito(self.texto[self.pos]):
            digitos_izquierda.append(self._avanzar())

        if self.pos < self.longitud and self.texto[self.pos] == ":":
            return self._reconocer_hora(digitos_izquierda, linea_inicial, columna_inicial)

        lexema = "".join(digitos_izquierda)
        return Token(self._nuevo_numero_token(), lexema, TipoToken.ENTERO,
                     linea_inicial, columna_inicial)

    def _reconocer_hora(self, digitos_izquierda, linea_inicial, columna_inicial):
        letras = list(digitos_izquierda)
        letras.append(self._avanzar())  # ':'
        digitos_derecha = []
        while self.pos < self.longitud and _es_digito(self.texto[self.pos]):
            digitos_derecha.append(self._avanzar())
        letras.extend(digitos_derecha)
        lexema = "".join(letras)

        horas_str = "".join(digitos_izquierda)
        minutos_str = "".join(digitos_derecha)

        valido = True
        if len(horas_str) != 2 or len(minutos_str) != 2:
            valido = False

        total_minutos = None
        if valido:
            horas = _entero_desde_digitos(horas_str)
            minutos = _entero_desde_digitos(minutos_str)
            if horas is None or minutos is None or minutos > 59:
                valido = False
            else:
                total_minutos = horas * 60 + minutos
                if total_minutos < HORA_MIN_MINUTOS or total_minutos > HORA_MAX_MINUTOS:
                    valido = False

        if not valido:
            self.gestor_errores.reportar(
                lexema=lexema,
                tipo_error=TipoError.HORA_FUERA_DE_RANGO,
                descripcion="Hora fuera de rango en línea {}, columna {}".format(
                    linea_inicial, columna_inicial
                ),
                linea=linea_inicial,
                columna=columna_inicial,
            )
        return Token(self._nuevo_numero_token(), lexema, TipoToken.HORA,
                     linea_inicial, columna_inicial)
    
    def _reconocer_identificador(self, linea_inicial, columna_inicial):
        letras = []
        while self.pos < self.longitud and _es_alfanumerico(self.texto[self.pos]):
            letras.append(self._avanzar())
        base = "".join(letras)

        if self.pos < self.longitud and self.texto[self.pos] == "-":
            guion = self._avanzar()
            digitos = []
            while self.pos < self.longitud and _es_digito(self.texto[self.pos]):
                digitos.append(self._avanzar())
            lexema = base + guion + "".join(digitos)

            if len(digitos) == 0:
                self.gestor_errores.reportar(
                    lexema=lexema,
                    tipo_error=TipoError.CODIGO_MAL_FORMADO,
                    descripcion="Código mal formado: '{}' en línea {}, columna {}".format(
                        lexema, linea_inicial, columna_inicial
                    ),
                    linea=linea_inicial,
                    columna=columna_inicial,
                )
            return Token(self._nuevo_numero_token(), lexema, TipoToken.CODIGO,
                         linea_inicial, columna_inicial)

        tipo = self._clasificar_identificador(base, linea_inicial, columna_inicial)
        token = Token(self._nuevo_numero_token(), base, tipo, linea_inicial, columna_inicial)

        if tipo == TipoToken.IDENTIFICADOR:
            self._ultimo_identificador = base
        else:
            self._ultimo_identificador = None
        return token

    def _clasificar_identificador(self, base, linea_inicial, columna_inicial):
        if base in PALABRAS_BLOQUE:
            return TipoToken.RESERVADA_BLOQUE
        elif base in PALABRAS_ELEMENTO:
            return TipoToken.RESERVADA_ELEMENTO
        elif base in PALABRAS_RELACION:
            return TipoToken.RESERVADA_RELACION
        elif base in DIAS_VALIDOS:
            return TipoToken.DIA
        elif base in CATEGORIAS_VALIDAS:
            return TipoToken.CATEGORIA
        else:
            if self._ultimo_identificador == "dia" and _es_mayusculas(base):
                self.gestor_errores.reportar(
                    lexema=base,
                    tipo_error=TipoError.DIA_NO_RECONOCIDO,
                    descripcion="Día no reconocido: '{}' en línea {}, columna {}".format(
                        base, linea_inicial, columna_inicial
                    ),
                    linea=linea_inicial,
                    columna=columna_inicial,
                )
            return TipoToken.IDENTIFICADOR

    def siguiente_token(self):
        self._saltar_espacios()
        if self.pos >= self.longitud:
            return None

        linea_inicial = self.linea
        columna_inicial = self.columna
        c = self.texto[self.pos]

        if c == "#":
            if self._siguiente_caracter(1) == "#":
                return self._reconocer_comentario(linea_inicial, columna_inicial)
            else:
                self._avanzar()
                self.gestor_errores.reportar(
                    lexema="#",
                    tipo_error=TipoError.CARACTER_NO_RECONOCIDO,
                    descripcion="Carácter no reconocido: '#' en línea {}, columna {}".format(
                        linea_inicial, columna_inicial
                    ),
                    linea=linea_inicial,
                    columna=columna_inicial,
                )
                return self.siguiente_token()
        elif c == '"':
            return self._reconocer_cadena(linea_inicial, columna_inicial)
        elif _es_digito(c):
            return self._reconocer_numero_u_hora(linea_inicial, columna_inicial)
        elif _es_letra(c):
            return self._reconocer_identificador(linea_inicial, columna_inicial)
        elif c in SIMBOLOS_VALIDOS:
            lexema = self._avanzar()
            return Token(self._nuevo_numero_token(), lexema, TipoToken.SIMBOLO,
                         linea_inicial, columna_inicial)
        else:
            self._avanzar()
            self.gestor_errores.reportar(
                lexema=c,
                tipo_error=TipoError.CARACTER_NO_RECONOCIDO,
                descripcion="Carácter no reconocido: '{}' en línea {}, columna {}".format(
                    c, linea_inicial, columna_inicial
                ),
                linea=linea_inicial,
                columna=columna_inicial,
            )
            return self.siguiente_token()


def tokenizar_texto(contenido, gestor_errores):
    analizador = AnalizadorLexico(contenido, gestor_errores)
    tokens = []
    while True:
        token = analizador.siguiente_token()
        if token is None:
            break
        tokens.append(token)
    return tokens

def tokenizar_archivo(ruta_archivo, gestor_errores):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
    return tokenizar_texto(contenido, gestor_errores)
