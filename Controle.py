import numpy as np
import time
import pandas as pd
import openpyxl
import Erros
import pickle
from Erros import ErroDeTipo, ErroDeMenu, ErroDeSituação, ErroDePlaca, inteiro_menu, placa

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
        self.carros = []
        self.dicionario = pd.DataFrame({
            "marca" : [],
            "modelo" : [],
            "placa" : []
        })

    def carregar_dados(self):
        try:
            self.dicionario = pd.read_excel('Controle.xlsx')
            with open("Controle.pkl", "rb") as arquivo:
                dados_carregados = pickle.load(arquivo)
                print("\nDados carregados com sucesso!")
            self.carros = dados_carregados
            print("\nDados carregados com sucesso!")
        except FileNotFoundError:
            print("Erro: o arquivo 'Controle.pkl' não foi encontrado.")
        except PermissionError:
            print("Erro: sem permissão para ler o arquivo.")
        except EOFError:
            print("Erro: o arquivo está vazio.")
        except Exception as e:
            print(f"Erro inesperado: {e}")    
        except pickle.UnpicklingError:
            print("Erro: o arquivo não contém dados válidos do pickle (pode estar corrompido).")

    def salvar_dados(self, dados, dt):
        try:
            with open("Controle.pkl", "wb") as arquivo:
                pickle.dump(dados, arquivo)
                print ("\nObjetos gravados com sucesso.")
            dt.to_excel('Controle.xlsx', index = False)
            print ("\nExcel gravado com sucesso.\n")
        except FileNotFoundError:
            print("Erro: caminho do arquivo inválido.")
        except PermissionError:
            print("Erro: sem permissão para gravar o arquivo.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
        except pickle.PickleError as e:
            print(f"Erro ao serializar os dados: {e}")

    def cadastrar_carro(self):
        try:
            print ("\n=== Novo Carro ===\n")
            marc = input("Indique a marca do veículo: ")
            model = input("\nIndique o modelo: ")
            plac = placa(input("\nIndique a placa: "), self.carros)
            car = Carro(marc, model, plac)
            self.carros.append(car)
            self.dicionario.loc[len(self.dicionario)] = car.dici()
            self.salvar_dados(self.carros, self.dicionario)
            print(self.dicionario)
            input("Pressione Enter para continuar")
        except ErroDePlaca as e:
            print(f"Erro: {e}")

    def listar_carros(self):
        if len(self.carros) == 0:
            return print("Não há carros listados")
        else:
            return print(self.dicionario)
    
    def editar_carros(self):
        print("\n|| Alteração de Dados ||")

        try:
            while True:
                self.listar_carros()
                resp1 = input("\nIndique a placa do carro que você deseja alterar o dado (Digite 0 para voltar): ")

                if resp1 == 0:
                    break
                else:
            
                    for b in self.carros:
                        if b.placa == resp1:

                            print("\n1 - Marca")
                            print("2 - Modelo")
                            print("3 - Placa")
                            print("0 - Voltar")

                            resp2 = inteiro_menu(input("\nQual dado do bem deseja alterar? "), 4)
                            if resp2 == 1:
                                marc = input("\nInforme o nova Marca: ")
                                b.set_marca = marc
                                self.dicionario.loc[self.dicionario["placa"]==resp1,"marca"] = marc
                                print(f"\nMarca atualizada para: {b.marca}")
                                self.salvar_dados(self.carros, self.dicionario)
                                input(f"Pressione Enter para continuar: ")
                                return
                            elif resp2 == 2:
                                mod = input("\nInforme o novo Modelo: ")
                                b.set_modelo = mod
                                self.dicionario.loc[self.dicionario["placa"]==resp1,"modelo"] = mod
                                print(f"\nModelo atualizada para: {b.modelo}")
                                self.salvar_dados(self.carros, self.dicionario)
                                input(f"Pressione Enter para continuar: ")
                                return
                            elif resp2 == 3:
                                plac = placa(input("\nInforme a nova placa: "), self.carros)
                                b.set_placa = plac
                                self.dicionario.loc[self.dicionario["placa"]==resp1,"placa"] = plac
                                print(f"\nPlaca atualizada para: {b.placa}")
                                self.salvar_dados(self.carros, self.dicionario)
                                input(f"Pressione Enter para continuar: ")
                                return
                            else:
                                return
                    else:
                        print(f"\nPlaca não encontrada!")

        except ErroDeMenu as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para voltar ao Menu Principal")
        except ErroDePlaca as e:
            print (f"Erro: {e}")
            input(f"Pressione Enter para voltar ao Menu Principal")
        
    def excluir_carro(self):
        print("\n|| Exclusão de Carro ||")
        self.listar_carros()

        while True:
            resp1 = input("\nIndique a placa do carro que você deseja excluir (Digite 0 para voltar): ")

            if resp1 == 0:
                return
            else:
                for b in self.carros:
                    if b.placa == resp1:
                        self.carros.remove(b)
                        self.dicionario = self.dicionario[self.dicionario['placa'] != resp1]
                        print(f"\nCarro excluído.")
                        self.salvar_dados(self.carros,self.dicionario)
                        input(f"Pressione Enter para continuar")
                        return
                else:
                    print(f"Placa não encontrada!")
                    input(f"Pressione Enter para continuar")
                    return
    
            