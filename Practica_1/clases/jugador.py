class Jugador:

    def __init__(self, carnet, nombre, apellido, nivel):
        self.carnet=int(carnet)
        self.nombre=nombre.strip()
        self.apellido=apellido.strip()
        self.nivel=nivel.strip()

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __repr__(self):
        return f"jugador carnet={self.carnet}, nombre={self,self.nombre_completo}, nuvel={self.nivel}"
