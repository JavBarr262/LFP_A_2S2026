from tokens import TipoToken


class Curso:
    def __init__(self, codigo, nombre, creditos=None):
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos


class Catedratico:
    def __init__(self, codigo, nombre, categoria=None):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria


class Aula:
    def __init__(self, codigo, capacidad=None, edificio=None):
        self.codigo = codigo
        self.capacidad = capacidad
        self.edificio = edificio


class Clase:
    def __init__(self, curso_codigo, catedratico_codigo, aula_codigo, dia, inicio, fin, seccion):
        self.curso_codigo = curso_codigo
        self.catedratico_codigo = catedratico_codigo
        self.aula_codigo = aula_codigo
        self.dia = dia
        self.inicio = inicio
        self.fin = fin
        self.seccion = seccion
        self.choque = False


class Horario:
    def __init__(self):
        self.cursos = {}
        self.catedraticos = {}
        self.aulas = {}
        self.clases = []


def _hora_a_minutos(hora_str):
    if hora_str is None or len(hora_str) != 5 or hora_str[2] != ":":
        return None
    try:
        h = int(hora_str[0:2])
        m = int(hora_str[3:5])
        return h * 60 + m
    except ValueError:
        return None


def _quitar_comillas(lexema):
    if lexema.startswith('"') and lexema.endswith('"'):
        return lexema[1:-1]
    return lexema


class ConstructorModelo:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.tipo not in {TipoToken.COMENTARIO_LINEA}]
        self.pos = 0
        self.n = len(self.tokens)
        self.horario = Horario()

    def _actual(self):
        if self.pos >= self.n:
            return None
        return self.tokens[self.pos]

    def _avanzar(self):
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def construir(self):
        while self.pos < self.n:
            t = self._actual()
            if t.tipo == TipoToken.RESERVADA_ELEMENTO:
                self._procesar_elemento(t.lexema)
            else:
                self._avanzar()
        return self.horario

    def _procesar_elemento(self, tipo_elemento):
        self._avanzar()

        if tipo_elemento == "clase":
            self._procesar_clase()
            return

        self._consumir_simbolo(":")
        nombre_token = self._consumir_tipo(TipoToken.CADENA)
        nombre = _quitar_comillas(nombre_token.lexema) if nombre_token else ""
        atributos = self._leer_bloque_atributos()
        codigo = atributos.get("codigo", nombre)

        if tipo_elemento == "curso":
            self.horario.cursos[codigo] = Curso(codigo, nombre, atributos.get("creditos"))
        elif tipo_elemento == "catedratico":
            self.horario.catedraticos[codigo] = Catedratico(codigo, nombre, atributos.get("categoria"))
        elif tipo_elemento == "aula":
            self.horario.aulas[nombre] = Aula(
                codigo=nombre,
                capacidad=atributos.get("capacidad"),
                edificio=atributos.get("edificio"),
            )

    def _procesar_clase(self):
        self._consumir_simbolo(":")
        curso_token = self._consumir_tipo(TipoToken.CADENA)
        curso_codigo = _quitar_comillas(curso_token.lexema) if curso_token else ""

        self._consumir_palabra("con")
        catedratico_token = self._consumir_tipo(TipoToken.CADENA)
        catedratico_codigo = _quitar_comillas(catedratico_token.lexema) if catedratico_token else ""

        self._consumir_palabra("en")
        aula_token = self._consumir_tipo(TipoToken.CADENA)
        aula_codigo = _quitar_comillas(aula_token.lexema) if aula_token else ""

        atributos = self._leer_bloque_atributos()

        clase = Clase(
            curso_codigo=curso_codigo,
            catedratico_codigo=catedratico_codigo,
            aula_codigo=aula_codigo,
            dia=atributos.get("dia"),
            inicio=atributos.get("inicio"),
            fin=atributos.get("fin"),
            seccion=atributos.get("seccion"),
        )
        self.horario.clases.append(clase)

    def _leer_bloque_atributos(self):
        atributos = {}
        t = self._actual()
        if t is None or not (t.tipo == TipoToken.SIMBOLO and t.lexema == "["):
            return atributos
        self._avanzar()

        while True:
            t = self._actual()
            if t is None:
                break
            if t.tipo == TipoToken.SIMBOLO and t.lexema == "]":
                self._avanzar()
                break
            if t.tipo == TipoToken.SIMBOLO and t.lexema == ",":
                self._avanzar()
                continue
            if t.tipo == TipoToken.IDENTIFICADOR:
                clave = t.lexema
                self._avanzar()
                self._consumir_simbolo(":")
                valor_token = self._actual()
                if valor_token is None:
                    break
                valor = valor_token.lexema
                if valor_token.tipo == TipoToken.CADENA:
                    valor = _quitar_comillas(valor_token.lexema)
                self._avanzar()
                atributos[clave] = valor
            else:
                self._avanzar()
        return atributos

    def _consumir_simbolo(self, simbolo):
        t = self._actual()
        if t is not None and t.tipo == TipoToken.SIMBOLO and t.lexema == simbolo:
            self._avanzar()

    def _consumir_palabra(self, palabra):
        t = self._actual()
        if t is not None and t.lexema == palabra:
            self._avanzar()

    def _consumir_tipo(self, tipo):
        t = self._actual()
        if t is not None and t.tipo == tipo:
            self._avanzar()
            return t
        return None

def detectar_choques(horario):
    conflictos = []
    clases = horario.clases
    n = len(clases)
    for i in range(n):
        for j in range(i + 1, n):
            a = clases[i]
            b = clases[j]

            if a.dia is None or b.dia is None or a.dia != b.dia:
                continue

            mismo_catedratico = (a.catedratico_codigo == b.catedratico_codigo and a.catedratico_codigo)
            misma_aula = (a.aula_codigo == b.aula_codigo and a.aula_codigo)

            if not (mismo_catedratico or misma_aula):
                continue

            ini_a = _hora_a_minutos(a.inicio)
            fin_a = _hora_a_minutos(a.fin)
            ini_b = _hora_a_minutos(b.inicio)
            fin_b = _hora_a_minutos(b.fin)

            if None in (ini_a, fin_a, ini_b, fin_b):
                continue

            if ini_a < fin_b and ini_b < fin_a:
                a.choque = True
                b.choque = True
                conflictos.append((a, b))

    return conflictos
