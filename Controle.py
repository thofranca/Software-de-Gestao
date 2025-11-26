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
        self.__tempo = []
    def dici(self):
        return {
            "marca" : self.__marca,
            "modelo" : self.__modelo,
            "placa" : self.__placa,
            "lavagens" : len(self.__tempo),
            "tempo medio": np.mean(self.__tempo)
        }
    
    def __str__(self):
        return f"\n{self.__marca} || {self.__modelo} || {self.__placa}"
    
    @property
    def marca(self):
        return self.__marca
    @property
    def modelo(self):
        return self.__modelo
    @property
    def placa(self):
        return self.__placa
    @property
    def tempo_carro(self):
        return self.__tempo
    @tempo_carro.setter
    def set_tempocarro(self,n):
        self.__tempo.append(n)
    @marca.setter
    def set_marca(self, n):
        self.__marca = n
    @modelo.setter
    def set_modelo(self, n):
        self.__modelo = n
    @placa.setter
    def set_placa(self, n):
        self.__placa = n
        

class produtos:
    def __init__(self, nome: str, valor: float, quantidade: float):
        self.__nome = nome
        self.__valor = valor
        self.__quantidade = quantidade
    
    def dicio(self):
        return {
            "nome" : self.__nome,
            "valor" : self.__valor,
            "quantidade" : self.__quantidade
        }
    
    @property
    def nome(self):
        return self.__nome
    @property
    def valor(self):
        return self.__valor
    @property
    def quantidade(self):
        return self.__quantidade
    @nome.setter
    def set_nome(self, n):
        self.__nome = n
    @valor.setter
    def set_valor(self, n):
        self.__valor = n
    @quantidade.setter
    def set_quantidade(self, n):
        self.__quantidade = n
class Controle_registro:
    def __init__(self):
        self.carros = []
        self.dicionario = pd.DataFrame({
            "marca" : [],
            "modelo" : [],
            "placa" : [],
            "lavagens" : [],
            "tempo medio" : []
        })

        self.prodt = []
        self.dicionario_prod = pd.DataFrame({
            "nome" : [],
            "valor" : [],
            "quantidade" : []
        })

        self.lavag = []
        self.dicionario_lav = pd.DataFrame({
            "carro" : [],
            "status" : [],
            "tempo" : []
        })
    def carregar_dados(self):
        try:
            self.dicionario = pd.read_excel('Controle.xlsx')
            print("\nExcel carros carregado com sucesso!")
            with open("Controle.pkl", "rb") as arquivo:
                dados_carregados = pickle.load(arquivo)
                print("\nObjetos carros carregados com sucesso!")
            self.carros = dados_carregados
            self.dicionario_prod = pd.read_excel('Estoque.xlsx')
            print("\nExcel Estoque carregado com sucesso!")
            with open("Estoque.pkl", "rb") as arquivo:
                dados_carregados = pickle.load(arquivo)
                print("\nObjetos de Estoque carregados com sucesso!")
            self.prodt = dados_carregados
            with open("Lavagens.pkl", "rb") as arquivo:
                dados_carregados = pickle.load(arquivo)
                print("\nObjetos de Lavagem carregados com sucesso!")
            self.lavag = dados_carregados
        except FileNotFoundError:
            print("Erro: Um dos arquivos não foi encontrado.")
        except PermissionError:
            print("Erro: sem permissão para ler o arquivo.")
        except EOFError:
            print("Erro: Um dos arquivos está vazio.")
        except Exception as e:
            print(f"Erro inesperado: {e}")    
        except pickle.UnpicklingError:
            print("Erro: o arquivo não contém dados válidos do pickle (pode estar corrompido).")

    def salvar_carro(self, dados, dt):
        try:
            with open("Controle.pkl", "wb") as arquivo:
                pickle.dump(dados, arquivo)
                print ("\nObjetos carros gravados com sucesso.")
            dt.to_excel('Controle.xlsx', index = False)
            print ("\nExcel carros gravado com sucesso.\n")
        except FileNotFoundError:
            print("Erro: caminho do arquivo inválido.")
        except PermissionError:
            print("Erro: sem permissão para gravar o arquivo.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
        except pickle.PickleError as e:
            print(f"Erro ao serializar os dados: {e}")

    def salvar_estoque(self, dados, dt):
        try:
            with open("Estoque.pkl", "wb") as arquivo:
                pickle.dump(dados, arquivo)
                print ("\nObjetos de estoque gravados com sucesso.")
            dt.to_excel('Estoque.xlsx', index = False)
            print ("\nExcel de estoque gravado com sucesso.\n")
        except FileNotFoundError:
            print("Erro: caminho do arquivo inválido.")
        except PermissionError:
            print("Erro: sem permissão para gravar o arquivo.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
        except pickle.PickleError as e:
            print(f"Erro ao serializar os dados: {e}")

    def salvar_lavagem(self, dados):
        try:
            with open("Lavagens.pkl", "wb") as arquivo:
                pickle.dump(dados, arquivo)
                print ("\nObjetos de estoque gravados com sucesso.")
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
            self.salvar_carro(self.carros, self.dicionario)
            print(self.dicionario)
            input("Pressione Enter para continuar")
        except ErroDePlaca as e:
            print(f"Erro: {e}")

    def listar_carros(self):
        if len(self.carros) == 0:
            return print("\nNão há carros listados")
        else:
            return print(self.dicionario)
    
    def editar_carros(self):
        print("\n|| Alteração de Dados ||")

        try:
            while True:
                self.listar_carros()
                resp1 = input("\nIndique a placa do carro que você deseja alterar o dado (Digite 0 para voltar): ")
                if resp1 == '0':
                    break
                else:
            
                    for b in self.carros:
                        if b.placa == resp1:

                            print("\n1 - Marca")
                            print("2 - Modelo")
                            print("3 - Placa")
                            print("0 - Voltar")

                            resp2 = inteiro_menu(input("\nQual dado do carro deseja alterar? "), 3)
                            if resp2 == 1:
                                marc = input("\nInforme o nova Marca: ")
                                b.set_marca = marc
                                self.dicionario.loc[self.dicionario["placa"]==resp1,"marca"] = marc
                                print(f"\nMarca atualizada para: {b.marca}")
                                self.salvar_carro(self.carros, self.dicionario)
                                input(f"Pressione Enter para continuar: ")
                                return
                            elif resp2 == 2:
                                mod = input("\nInforme o novo Modelo: ")
                                b.set_modelo = mod
                                self.dicionario.loc[self.dicionario["placa"]==resp1,"modelo"] = mod
                                print(f"\nModelo atualizada para: {b.modelo}")
                                self.salvar_carro(self.carros, self.dicionario)
                                input(f"Pressione Enter para continuar: ")
                                return
                            elif resp2 == 3:
                                plac = placa(input("\nInforme a nova placa: "), self.carros)
                                b.set_placa = plac
                                self.dicionario.loc[self.dicionario["placa"]==resp1,"placa"] = plac
                                print(f"\nPlaca atualizada para: {b.placa}")
                                self.salvar_carro(self.carros, self.dicionario)
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

            if resp1 == '0':
                return
            else:
                for b in self.carros:
                    if b.placa == resp1:
                        self.carros.remove(b)
                        self.dicionario = self.dicionario[self.dicionario['placa'] != resp1]
                        print(f"\nCarro excluído.")
                        self.salvar_carro(self.carros,self.dicionario)
                        input(f"Pressione Enter para continuar")
                        return
                else:
                    print(f"Placa não encontrada!")
                    input(f"Pressione Enter para continuar")
                    return
    
    def nova_compra(self):
        try:
            print ("\n=== Novo Produto ===\n")
            nom = input("Indique o nome do produto: ")
            valor = float(input("\nIndique o valor em R$: "))
            quantida = float(input("\nIndique a quantidade em ml: "))
            for e in self.prodt:
                if nom.lower() == e.nome.lower():
                    e.set_quantidade = e.quantidade+quantida
                    e.set_valor = e.valor+valor
                    self.dicionario_prod.loc[self.dicionario_prod["nome"]==nom,"quantidade"] = e.quantidade
                    self.dicionario_prod.loc[self.dicionario_prod["nome"]==nom,"valor"] = e.valor
                    print(self.dicionario_prod)
                    input("Pressione Enter para continuar")
                    return
            else:
                prod = produtos(nom, valor, quantida)
                self.prodt.append(prod)
                self.dicionario_prod.loc[len(self.dicionario_prod)] = prod.dicio()
                self.salvar_estoque(self.prodt, self.dicionario_prod)
                print(self.dicionario_prod)
                input("\nPressione Enter para continuar")
                return
        except TypeError as e:
            print(f"Erro: Tipo de valor inserido deve ser um número float")

    def listar_estoque(self):
        if len(self.prodt) == 0:
            return print("\nNão há produtos listados")
        else:
            return print(self.dicionario_prod)
    
    def editar_estoque(self):
        print("\n|| Alteração de Dados ||")

        try:
            while True:
                self.listar_estoque()
                resp1 = input("\nIndique o nome do produto que você deseja alterar o dado (Digite 0 para voltar): ")
                if resp1 == '0':
                    break
                else:
            
                    for b in self.prodt:
                        if b.nome.lower() == resp1.lower():

                            print("\n1 - Nome")
                            print("2 - Valor")
                            print("3 - Quantidade")
                            print("0 - Voltar")

                            resp2 = inteiro_menu(input("\nQual dado do produto deseja alterar? "), 3)
                            if resp2 == 1:
                                nom = input("\nInforme o novo Nome: ")
                                for i in self.prodt:
                                    if nom == i.nome.lower():
                                        res = inteiro_menu(input("\nNome já existente, deseja cruzar os dados de quantidade e valores?\n\n1 - Sim.\n2 - Não e voltar."),2)
                                        if res == '1':
                                            i.set_quantidade = i.quantidade+b.quantidade
                                            i.set_valor = i.valor+b.valor
                                            self.dicionario_prod.loc[self.dicionario_prod["nome"]==nom,"quantidade"] = i.quantidade
                                            self.dicionario_prod.loc[self.dicionario_prod["nome"]==nom,"valor"] = i.valor
                                        elif res == '2':
                                            break
                                        else:
                                            break
                                else:
                                    b.set_nome = nom
                                    self.dicionario_prod.loc[self.dicionario_prod["nome"]==resp1,"nome"] = nom
                                    print(f"\nNome atualizado para: {b.nomd}")
                                    self.salvar_estoque(self.prodt, self.dicionario_prod)
                                    input(f"Pressione Enter para continuar: ")
                                    return
                            elif resp2 == 2:
                                val = float(input("\nInforme o novo valor em R$: "))
                                b.set_valor = val
                                self.dicionario_prod.loc[self.dicionario_prod["nome"]==resp1,"valor"] = val
                                print(f"\nValor atualizado para: {b.valor}")
                                self.salvar_estoque(self.prodt, self.dicionario_prod)
                                input(f"Pressione Enter para continuar: ")
                                return
                            elif resp2 == 3:
                                qnt = float(input("\nInforme a nova quantidade em ml: "))
                                b.set_quantidade = qnt
                                self.dicionario_prod.loc[self.dicionario_prod["nome"]==resp1,"quantidade"] = qnt
                                print(f"\nQuantidade atualizada para: {b.quantidade}")
                                self.salvar_estoque(self.prodt, self.dicionario_prod)
                                input(f"Pressione Enter para continuar: ")
                                return
                            else:
                                return
                    else:
                        print(f"\nProduto não encontrado!")
        except ErroDeMenu as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para voltar ao Menu Principal")
        except TypeError as e:
            print(f"Erro: Tipo de valor inserido deve ser um número float")
        
    def excluir_produto(self):

        print("\n|| Exclusão de Produto ||")
        self.listar_estoque()

        while True:
            resp1 = input("\nIndique o nome do produto que você deseja excluir (Digite 0 para voltar): ")

            if resp1 == '0':
                return
            else:
                for b in self.prodt:
                    if b.nome.lower() == resp1.lower():
                        self.prodt.remove(b)
                        self.dicionario_prod = self.dicionario_prod[self.dicionario_prod['placa'] != resp1]
                        print(f"\nProduto excluído.")
                        self.salvar_estoque(self.prodt,self.dicionario_prod)
                        input(f"Pressione Enter para continuar")
                        return
                else:
                    print(f"Produto não encontrado!")
                    input(f"Pressione Enter para continuar")
                    return    
                
    def inicar_lavagem(self):
            self.listar_carros()
            resp1 = input("\nIndique a placa do carro que você deseja iniciar lavagem (Digite 0 para voltar): ")

            if resp1 == '0':
                return
            else:
                for b in self.carros:
                    if b.placa == resp1:
                        for i in self.lavag:
                            if b == i.carro:
                                print("\nParece que este carro ja está em lavagem!\n")
                                input("Pressione Enter para continuar")
                                break
                        else: 
                            print("Carro indicado para lavagem:", b)
                            resp2 = inteiro_menu(input("\n1 - Sim\n0 - Não\n\nDeseja continuar? "), 1)
                            if resp2 == 1:
                                print("Lavagem iniciada!")
                                self.lavag.append(Lavagem(b, "Em Andamento", time.time()))
                                self.salvar_lavagem(self.lavag)
                                return
                            else:
                                return
                else:
                    print(f"Placa não encontrada!")
                    input(f"Pressione Enter para continuar")
                    return 
                
    def lavagens_and(self):
        if len(self.lavag) == 0:
            print('\nNenhuma lavagem em andamento\n')
        else:
            print("\nLavagens em andamento")
            for i in self.lavag:
                if i.status.lower() == 'em andamento':
                    print(f"{i.carro} - Em andamento - Tempo até aqui: {(time.time() - i.tempo)/60} minutos")
                elif i.status.lower() == 'pausado':
                    print(f"{i.carro} - Pausada - Tempo até aqui: {(i.tempopausado - i.tempo)/60} minutos")
    
    def pausar_finalizar(self):
        print ('\n1 - Finalizar')
        print ('2 - Pausar')
        print ('3 - Despausar')
        print ('0 - Voltar\n')
        try:
            resp1 = inteiro_menu(input("Indique uma das opções do menu: "),3)
            var = None
            if resp1 == 1:
                self.lavagens_and()
                resp2 = input("\nIndique a placa do carro para finalizar a lavagem (0 para voltar): ")
                if resp2 == '0':
                    return
                else:
                    for b in self.lavag:
                        if b.carro.placa == resp2:
                            b.carro.set_tempocarro = time.time()- b.tempopausado - b.tempo
                            print(f"Lavagem finalizada em {(b.carro.tempo_carro[len(b.carro.tempo_carro)])/60}")
                            self.lavag.remove(b)
                            self.salvar_lavagem(self.lavag)
                            return
            elif resp1 == 2:
                self.lavagens_and()
                resp2 = input("\nIndique a placa do carro para pausar a lavagem (0 para voltar): ")
                if resp2 == '0':
                    return
                else:
                    for b in self.lavag:
                        if b.carro.placa == resp2:
                            if b.status == 'pausado':
                                print("A lavagem deve estar em andamento para pausa-lá.")
                                break
                            else:
                                b.set_tempopausado = time.time()
                                b.set_status = 'pausado'
                                print(f"Lavagem pausada em {(b.tempopausado - b.tempo)/60} minutos de trabalho")
                                self.salvar_lavagem(self.lavag)
                                return
                    else:
                        print(f"\nPlaca não encontrada!")
            elif resp1 == 3:
                self.lavagens_and()
                resp2 = input("\nIndique a placa do carro para despausar a lavagem (0 para voltar): ")
                if resp2 == '0':
                    return
                else:
                    for b in self.lavag:
                        if b.carro.placa == resp2:
                            if b.status == 'pausado':
                                b.set_tempopausado = time.time() - b.tempopausado
                                b.set_status = 'Em Andamento'
                                print(f"Lavagem em andamento")
                                self.salvar_lavagem(self.lavag)
                                return
                            else:
                                print("A lavagem deve estar em andamento para pausa-lá.")
                                break
                    else:
                        print(f"\nPlaca não encontrada!")
        except ErroDeMenu as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")

class Lavagem:
    def __init__(self, carro: Carro, status: str, tempo: time):
        self.__carro = carro
        self.__status = status
        self.__tempo = tempo
        self.__tempopausado = 0

    @property
    def carro(self):
        return self.__carro
    @property
    def status(self):
        return self.__status
    @property
    def tempo(self):
        return self.__tempo
    @property
    def tempopausado(self):
        return self.__tempopausado
    @tempopausado.setter
    def set_tempopausado(self,n):
        set_tempopausado = n
    @status.setter
    def set_status(self,n):
        self.__status = n
    @carro.setter
    def set_carro(self,n):
        self.__carro = n
    @tempo.setter
    def set_tempo(self,n):
        self.__tempo = n