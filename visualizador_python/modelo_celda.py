class ModeloCelda:
    def __init__(self, numero_celda: int):
        self.numero_celda = numero_celda
        self.ocupada = False
        self.placa = ""
        self.hora_ingreso = ""

    def ocupar(self, placa: str, hora: str):
        self.ocupada = True
        self.placa = placa
        self.hora_ingreso = hora

    def liberar(self):
        self.ocupada = False
        self.placa = ""
        self.hora_ingreso = ""

    def a_diccionario(self) -> dict:
        return {
            "numero": self.numero_celda,
            "ocupada": self.ocupada,
            "placa": self.placa,
            "hora": self.hora_ingreso
        }
