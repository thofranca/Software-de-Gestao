class Carro:
    def __init__(self, marca, modelo, placa):
        self.__marca = marca
        self.__modelo = modelo
        self.__placa = placa
    
    @property
    def marca(self):
        return self.__marca
    @property
    def modelo(self):
        return self.__modelo
    @property
    def placa(self):
        return self.__placa
    @setter.placa
    def set_placa(self, ):
