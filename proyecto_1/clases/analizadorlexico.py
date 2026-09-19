from tokens import Token, TipoToken, TipoError   
PALABRAS_BLOQUE=("HORARIO","CURSOS,","CATEDRATICOS","AULAS","CLASES")
PALABRAS_ELEMENTO=("curso","catedratico","aula","clase")
PALABRAS_RELACION=("con","en")
DIAS_VALIDOS=("LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO")
CATEGORIAS_VALIDAS=("TITULAR","INTERINO","AUXILIAR")
SIMBOLOS_VALIDOS=("{","}","[","]",":",",",";")
HORA_MIN_MINUTOS=6*60
HORA_MAX_MINUTOS=21*60

def _es_letra(c):
    return("A"<=c<="z") or ("A"<=c<="Z") 

def _es_digito(c):
    return "0"<=c<="9"

def _es_alfanumerico(c):
    return _es_letra(c) or _es_digito(c)

def _es_espacio(c):
    return c=="" or c=="\t" or c =="\r"

class AnalizadorLexico:
    def __init__(self, texto, gestor_errores):
        self.texto=texto
        self.longitud=len(texto)
        self.pos=0
        self.linea=1
        self.gestor_errores=gestor_errores
        self._ultimo_identificador=None
