import numpy as np
import time
import pandas as pd
import openpyxl
import Erros

class Carro:
    def __init__(self, marca, modelo, placa):
        self.__marca = marca
        self.__modelo = modelo
        self.__placa = placa
    
    def dici(self):
        return {
            "marca" : self.__marca,
            "modelo" : self.__modelo,
            "placa" : self.__placa
        }
    
    @property
    def marca(self):
        return self.__marca
    @property
    def modelo(self):
        return self.__modelo
    @property
    def placa(self):
        return self.__placa
    @marca.setter
    def set_marca(self, n):
        return self.__marca == n
    @modelo.setter
    def set_modelo(self, n):
        return self.__modelo == n
    @placa.setter
    def set_placa(self, n):
        return self.__placa == n

class Controle_Lavagens:
    def __init__(self):
        self.carros = pd.DataFrame({
            "marca" : [],
            "modelo" : [],
            "placa" : []
        })

    def carregar_dados(self):
        try:
            self.carros = pd.read_excel('Controle.xlsx')
            print("\nDados carregados com sucesso!")
        except FileNotFoundError:
            print("Erro: o arquivo 'Controle.xlsx' não foi encontrado.")
        except PermissionError:
            print("Erro: sem permissão para ler o arquivo.")
        except EOFError:
            print("Erro: o arquivo está vazio.")
        except Exception as e:
            print(f"Erro inesperado: {e}")    

    def salvar_dados(self, dados):
        try:
            dados.to_excel('Controle.xlsx')
            print ("\nDados gravados com sucesso.")
        except FileNotFoundError:
            print("Erro: caminho do arquivo inválido.")
        except PermissionError:
            print("Erro: sem permissão para gravar o arquivo.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            
    def cadastrar_carro(self):
        try:
            print ("\n=== Novo Carro ===\n")
            marc = input("Indique a marca do veículo: ")
            model = input("\nIndique o modelo: ")
            plac = input("\nIndique a placa: ")
            car = Carro(marc, model, plac)
            self.carros.loc[len(self.carros)] = car.dici()
            self.salvar_dados(self.carros)
            print(self.carros)
            input("Pressione Enter para continuar")
        except FileNotFoundError:
            print("Erro: caminho do arquivo inválido.")
        except PermissionError:
            print("Erro: sem permissão para gravar o arquivo.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def listar_carros(self):
        return print(self.carros)
    
    def editar_bem(self):
        print("\n|| Alteração de Dados ||")

        try:
            while True:
                self.listar_carros()
                resp1 = (input("\nIndique a placa do carro que você deseja alterar o dado (Digite -1 para voltar): "))

                if resp1 == -1:
                    break
                else:
            
                    for b in self.carros:
                        if b.codigo == resp1:

                            print("\n1 - Marca")
                            print("2 - Modelo")
                            print("3 - Placa")
                            print("0 - Voltar")

                            resp2 = inteiro_menu(input("\nQual dado do bem deseja alterar? "), 4)
                            if resp2 == 1:
                                codi = cod(inteiro(input("\nInforme o nova Marca: ")),self.bens)
                                b.codigo = codi
                                print(f"\nMarca atualizada para: {b.codigo}")
                                self.salvar_dados(self.bens)
                                input(f"Pressione Enter para continuar: ")
                                return
                            elif resp2 == 2:
                                desc = input("\nInforme o novo Modelo: ")
                                b.descri = desc
                                print(f"\nModelo atualizada para: {b.descri}")
                                self.salvar_dados(self.bens)
                                input(f"Pressione Enter para continuar: ")
                                return
                            elif resp2 == 3:
                                loc = input("\nInforme a nova placa: ")
                                b.local = loc
                                print(f"\nPlaca atualizada para: {b.local}")
                                self.salvar_dados(self.bens)
                                input(f"Pressione Enter para continuar: ")
                                return
                            else:
                                return
                    else:
                        print(f"\nCódigo Inválido!")

    
        except ErroDeMenu as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para voltar ao Menu Principal")
        except ErroDeTipo as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para voltar ao Menu Principal")
        except ErroDeSituação as e:
            print (f"Erro: {e}")
            input(f"Pressione Enter para voltar ao Menu Principal")
        except ErroDeCodigo as e:
            print (f"Erro: {e}")
            input(f"Pressione Enter para voltar ao Menu Principal")
            