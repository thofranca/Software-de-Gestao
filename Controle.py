import numpy as np
import time
import pandas as pd
import openpyxl
import Erros
import pickle
from Erros import ErroDeTipo, ErroDeMenu, ErroDePlaca, inteiro_menu, placa

class Carro:

    """
    Representa um veículo cadastrado no sistema.

    Atributos privados:
        __marca (str): marca do veículo.
        __modelo (str): modelo do veículo.
        __placa (str): placa do veículo.
        __tempo (list): lista de tempos (segundos) de cada lavagem registrada.
    
    Propriedades:
        marca, modelo, placa, tempo_carro, lav (quantidade de lavagens registradas).

    Método útil:
        dici(): devolve um dicionário com os atributos principais para exportação ao DataFrame.
    """

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
            "quantia de lavagens" : self.lav
        }
    
    def __str__(self):
        return f"\n{self.__marca} || {self.__modelo} || {self.__placa}"
    
    @property
    def lav(self):
        return len(self.__tempo)
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
    """
    Representa um produto de limpeza do estoque.

    Atributos privados:
        __nome (str): nome do produto.
        __valor (float): valor unitário do produto.
        __quantidade (float): quantidade disponível (ml).

    Propriedades:
        nome, valor, quantidade.  
    
    Métodos:
        dicio(): retorna um dicionário com nome, valor e quantidade para exportação ao DataFrame.
    """

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

class Lavagem:
    """
    Representa uma lavagem em andamento ou finalizada.

    Atributos privados:
        __carro (Carro): objeto Carro associado à lavagem.
        __status (str): estado atual ('Em Andamento', 'Pausado', etc).
        __tempo (float): timestamp de início (time.time()).
        __preco (float): preço cobrado pela lavagem.
        __tempopausado (float): timestamp ou tempo acumulado de pausa conforme usado.

    Propriedades:
        carro, status, tempo, preco_lavagem, tempopausado.

    Observação:
        Classe com número maior de getters e setters por necessidade de controle de fluxo do sistema.
    """
    def __init__(self, carro: Carro, status: str, tempo: time):
        self.__carro = carro
        self.__status = status
        self.__tempo = tempo
        self.__preco = 80.00
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
    @property
    def preco_lavagem(self):
        return self.__preco
    @preco_lavagem.setter
    def set_preco_lavagem(self, n):
        self.__preco = n
    @tempopausado.setter
    def set_tempopausado(self,n):
        self.__tempopausado = n
    @status.setter
    def set_status(self,n):
        self.__status = n
    @carro.setter
    def set_carro(self,n):
        self.__carro = n
    @tempo.setter
    def set_tempo(self,n):
        self.__tempo = n
class Controle_registro:
    """
    Classe responsável por gerenciar todo o fluxo de dados e operações do sistema de 
    controle de lavagem, estoque, finanças e manipulação de produtos.

    Esta classe reúne todos os objetos principais do programa (Carro, Lavagem, Produto),
    além de manter DataFrames persistentes e gerenciar leituras, escritas e atualizações
    nos arquivos Excel e Pickle utilizados como banco de dados.

    Atributos:
    carros : list[Carro]
        Lista de objetos Carro cadastrados.

    dicionario : pandas.DataFrame
        Representação tabular dos carros cadastrados 
        (marca, modelo, placa). Sincronizada com a lista 'carros'.

    prodt : list[produtos]
        Lista de objetos correspondentes aos produtos do estoque.

    dicionario_prod : pandas.DataFrame
        Tabela com nome, valor e quantidade dos produtos. 
        Sincronizada com a lista 'prodt'.

    lavag : list[Lavagem]
        Lista de lavagens em andamento ou finalizadas que ainda 
        não foram apagadas do histórico.

    financas : pandas.DataFrame
        Tabela usada para registrar gastos, faturamento e tempo de trabalho.

    manipulacao : pandas.DataFrame
        DataFrame criado para auxiliar na manipulação dos dados de minutos trabalhados por lavagem.
    
    Esta classe funciona como o "cérebro" do software de gestão, reunindo:

    - Operações de produto e cliente
    - Gerenciamento completo de lavagens
    - Atualização automática de planilhas
    - Persistência de objetos Python
    - Geração de estatísticas e indicadores financeiros

    É a camada central de controle do sistema.

    """  
    def __init__(self):
        self.carros = []
        self.dicionario = pd.DataFrame({
            "marca" : [],
            "modelo" : [],
            "placa" : [],
        })

        self.prodt = []
        self.dicionario_prod = pd.DataFrame({
            "nome" : [],
            "valor" : [],
            "quantidade" : []
        })
        self.lavag = []

        self.financas = pd.DataFrame({
            "gasto" : [],
            "faturamento" : [],
            "tempo de trabalho" : []
        })

        self.manipulacao = pd.DataFrame({
            'manipulacao' : []
        })

    def carregar_dados(self):
        """
        Carrega dados (Excel / pickle) para os atributos do registro:
        - carros (pickle + Excel 'Controle.xlsx')
        - estoque (pickle + Excel 'Estoque.xlsx')
        - lavagens (pickle 'Lavagens.pkl')
        - finanças (Excel 'Financas.xlsx')

        Efeitos:
            Atualiza self.carros, self.dicionario, self.prodt, self.dicionario_prod,
            self.lavag e self.financas.

        Tratamento de erros:
            Captura FileNotFoundError, PermissionError, EOFError, pickle.UnpicklingError
            e Exception geral, exibindo mensagem apropriada.
        """
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
            self.financas = pd.read_excel('Financas.xlsx')
            print("\nExcel de finanças carregado com sucesso!")
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
        """
        Salva a lista de objetos 'dados' (carros) em 'Controle.pkl' via pickle
        e salva o DataFrame 'dt' em 'Controle.xlsx'.

        Parâmetros:
            dados (list): lista de objetos Carro a serializar.
            dt (pandas.DataFrame): DataFrame representando os carros para salvar em Excel.

        Efeitos:
            Cria/atualiza os arquivos Controle.pkl e Controle.xlsx.

        Tratamento de erros:
            Captura FileNotFoundError, PermissionError, pickle.PickleError e Exception geral.
        """
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
        """
        Salva objetos de estoque em 'Estoque.pkl' e salva o DataFrame 'dt' em 'Estoque.xlsx'.

        Parâmetros:
            dados (list): lista de objetos produtos.
            dt (pandas.DataFrame): DataFrame do estoque.

        Efeitos e erros: similar a salvar_carro.
        """
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
        """
        Salva a lista de lavagens em 'Lavagens.pkl'.

        Parâmetros:
            dados (list): lista de objetos Lavagem.

        Tratamento de erros:
            Captura FileNotFoundError, PermissionError, pickle.PickleError e Exception geral.
        """
        try:
            with open("Lavagens.pkl", "wb") as arquivo:
                pickle.dump(dados, arquivo)
                print ("\nObjetos de lavagem gravados com sucesso.")
        except FileNotFoundError:
            print("Erro: caminho do arquivo inválido.")
        except PermissionError:
            print("Erro: sem permissão para gravar o arquivo.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
        except pickle.PickleError as e:
            print(f"Erro ao serializar os dados: {e}")

    def salvar_financas(self, dt, dt1, dt2):
        """
        Salva o DataFrame de finanças em 'Financas.xlsx'.

        Parâmetros:
            dt (pandas.DataFrame): DataFrame de finanças que será salvo.
            dt1 (pandas.DataFrame): DataFrame usado para obter 'tempo de trabalho' (coluna 'manipulacao').
            dt2 (pandas.DataFrame): DataFrame usado para obter 'gasto' (coluna 'valor').

        Efeitos:
            Atualiza colunas de dt ('gasto', 'tempo de trabalho') a partir de dt2/dt1 e salva em Excel.

        Tratamento de erros:
            Captura FileNotFoundError, PermissionError, pickle.PickleError e Exception geral.
        """
        try:
            dt['gasto'] = dt2['valor']
            dt['tempo de trabalho'] = dt1['manipulacao']
            dt.to_excel('Financas.xlsx', index = False)
            print ("\nExcel de finanças gravado com sucesso.\n")
        except FileNotFoundError:
            print("Erro: caminho do arquivo inválido.")
        except PermissionError:
            print("Erro: sem permissão para gravar o arquivo.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
        except pickle.PickleError as e:
            print(f"Erro ao serializar os dados: {e}")

    def cadastrar_carro(self):
        """
        Solicita dados ao usuário (marca, modelo, placa), valida a placa e cadastra um novo Carro.

        Fluxo:
            - Lê inputs do usuário.
            - Valida a placa chamando a função placa().
            - Cria objeto Carro, adiciona em self.carros e adiciona linha em self.dicionario.
            - Persiste chamando salvar_carro().

        Exceções:
            Captura ErroDePlaca (placa inválida/duplicada) e exibe mensagem.
        """
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
        """
        Exibe os carros registrados.

        Comportamento:
            - Se não houver carros, imprime mensagem informativa.
            - Caso contrário, imprime o DataFrame self.dicionario.
        """
        if len(self.carros) == 0:
            return print("\nNão há carros listados")
        else:
            return print(f"\n{self.dicionario}")
    
    def editar_carros(self):
        """
        Permite alterar dados de um carro (marca, modelo, placa).

        Fluxo:
            - Lista carros e pede a placa a ser editada.
            - Se encontrada, solicita qual campo editar e atualiza o objeto e o DataFrame.
            - Persiste alterações com salvar_carro().

        Exceções tratadas:
            ErroDeMenu, ErroDeTipo, ErroDePlaca e TypeError em conversões.
        """
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
            input(f"Pressione Enter para continuar")
        except ErroDeTipo as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")        
        except ErroDePlaca as e:
            print (f"Erro: {e}")
            input(f"Pressione Enter para voltar ao Menu Principal")
        
    def excluir_carro(self):
        """
        Remove um carro do sistema.

        Fluxo:
            - Solicita a placa a ser excluída.
            - Se houver lavagens associadas em self.lavag, remove-as primeiro.
            - Remove o objeto Carro de self.carros e a linha correspondente de self.dicionario.
            - Persiste as mudanças com salvar_carro() e salvar_lavagem().

        Retorno:
            None, apenas efeito colateral nos atributos e arquivos.
        """
        print("\n|| Exclusão de Carro ||")
        self.listar_carros()

        while True:
            resp1 = input("\nIndique a placa do carro que você deseja excluir (Digite 0 para voltar): ")

            if resp1 == '0':
                return
            else:
                for b in self.carros:
                    if b.placa == resp1:
                        for i in self.lavag:
                            if i.carro.placa == b.placa:
                                self.lavag.remove(i)
                                self.salvar_lavagem(self.lavag)
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
        """
        Adiciona produto ao estoque ou atualiza um produto existente.

        Fluxo:
            - Lê nome, valor e quantidade do produto.
            - Se o produto já existir (comparação case-insensitive), atualiza quantidade e valor.
            - Caso contrário, cria novo objeto produtos, adiciona à lista e DataFrame e persiste com salvar_estoque().

        Erros:
            Trata TypeError (valores não numéricos).
        """
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
        """
        Exibe o DataFrame de estoque (self.dicionario_prod) ou mensagem caso esteja vazio.
        """
        if len(self.prodt) == 0:
            return print("\nNão há produtos listados")
        else:
            return print(self.dicionario_prod)
    
    def editar_estoque(self):
        """
        Permite atualizar nome, valor ou quantidade de produto no estoque.

        Fluxo:
            - Lista estoque, solicita nome do produto.
            - Se encontrado, pergunta qual campo alterar e atualiza o objeto e DataFrame.
            - Oferece opção de 'cruzar' dados quando um novo nome já existe (fundir quantidades/valores).
            - Persiste alterações com salvar_estoque() e salvar_financas() quando aplicável.

        Exceções:
            Trata ErroDeMenu, ErroDeTipo e TypeError para entradas inválidas.
        """
        print("\n|| Atualização Estoque ||\n")

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
                                            self.salvar_estoque(self.prodt, self.dicionario_prod)
                                            self.salvar_financas(self.financas, self.manipulacao, self.dicionario_prod)
                                            print("Dados cruzados com sucesso!")
                                            input("Pressione Enter para continuar")
                                        elif res == '2':
                                            break
                                        else:
                                            break
                                else:
                                    b.set_nome = nom
                                    self.dicionario_prod.loc[self.dicionario_prod["nome"]==resp1,"nome"] = nom
                                    print(f"\nNome atualizado para: {b.nome}")
                                    self.salvar_estoque(self.prodt, self.dicionario_prod)
                                    input(f"Pressione Enter para continuar: ")
                                    return
                            elif resp2 == 2:
                                val = float(input("\nInforme o novo valor em R$: "))
                                b.set_valor = val
                                self.dicionario_prod.loc[self.dicionario_prod["nome"]==resp1,"valor"] = val
                                print(f"\nValor atualizado para: {b.valor}")
                                self.salvar_estoque(self.prodt, self.dicionario_prod)
                                self.salvar_financas(self.financas, self.manipulacao, self.dicionario_prod)
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
            input(f"Pressione Enter para continuar")
        except ErroDeTipo as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")        
        except TypeError as e:
            print(f"Erro: Tipo de valor inserido deve ser um número float")
        
    def excluir_produto(self):
        """
        Remove produto do estoque.

        Fluxo:
            - Solicita nome do produto (case-insensitive).
            - Remove objeto da lista e linha do DataFrame, persiste com salvar_estoque()
            e atualiza finanças via salvar_financas().
        """
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
                        self.dicionario_prod = self.dicionario_prod[self.dicionario_prod['nome'] != resp1]
                        print(f"\nProduto excluído.")
                        self.salvar_estoque(self.prodt,self.dicionario_prod)
                        self.salvar_financas(self.financas, self.manipulacao, self.dicionario_prod)
                        input(f"Pressione Enter para continuar")
                        return
                else:
                    print(f"Produto não encontrado!")
                    input(f"Pressione Enter para continuar")
                    return    
                
    def inicar_lavagem(self):
        """
        Inicia uma nova lavagem para um carro existente.

        Fluxo:
            - Lista carros e solicita a placa do carro a ser lavado.
            - Verifica se o carro existe; se não, informa o usuário.
            - Verifica se o carro já está em lavagem (percorrendo self.lavag).
            - Se não estiver em lavagem, solicita confirmação e cria um objeto Lavagem,
            adicionando-o em self.lavag e salvando via salvar_lavagem().
        """
        self.listar_carros()
        resp1 = input("\nIndique a placa do carro que você deseja iniciar lavagem (Digite 0 para voltar): ")
        if resp1 == '0':
            return
        else:
            encontrou_carro = False
            for b in self.carros:
                if b.placa == resp1:
                    encontrou_carro = True
                    encontrou_lavagem = False
                    for i in self.lavag:
                        if b.placa == i.carro.placa:
                            encontrou_lavagem = True
                            print("\nParece que este carro ja está em lavagem!\n")
                            input("Pressione Enter para continuar")
                            return
                    if encontrou_lavagem == False: 
                        print("Carro indicado para lavagem:\n", b)
                        resp2 = inteiro_menu(input("\n1 - Sim\n0 - Não\n\nDeseja continuar? "), 1)
                        if resp2 == 1:
                            print("Lavagem iniciada!")
                            lav = Lavagem(b, "Em Andamento", time.time())
                            self.lavag.append(lav)
                            self.salvar_lavagem(self.lavag)
                            return
                        else:
                            return
            if encontrou_carro == False:
                print(f"Placa não encontrada!")
                input(f"Pressione Enter para continuar")
                return 
                
    def lavagens_and(self):
        """
        Exibe lavagens em andamento ou pausadas.

        Comportamento:
            - Se não houver lavagens, imprime mensagem apropriada.
            - Caso contrário, lista cada lavagem com status e tempo decorrido (em minutos).
        """
        if len(self.lavag) == 0:
            print('\nNenhuma lavagem em andamento')
        else:
            print("\nLavagens em andamento")
            for i in self.lavag:
                if i.status.lower() == 'em andamento':
                    print(f"{i.carro} - Em andamento - Tempo até aqui: {(time.time() - i.tempo)/60:.2f} minutos")
                elif i.status.lower() == 'pausado':
                    print(f"{i.carro} - Pausada - Tempo até aqui: {(i.tempopausado - i.tempo)/60:.2f} minutos")
    
    def pausar_finalizar(self):
        """
        Menu para finalizar, pausar ou despausar lavagens.

        Opções:
            1 - Finalizar: finaliza a lavagem escolhida, registra tempo de trabalho no carro,
                grava faturamento em self.financas e pergunta se deseja atualizar estoque.
            2 - Pausar: marca a lavagem como pausada e grava tempo de pausa.
            3 - Despausar: reverte pausa, ajustando os tempos.
            0 - Voltar

        Fluxo e efeitos:
            - Afeta self.lavag, self.carros, self.manipulacao e self.financas; persiste via salvar_*.
            - Trata entradas inválidas com ErroDeMenu e ErroDeTipo.
        """
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
                            self.lavag.remove(b)
                            self.salvar_lavagem(self.lavag)
                            self.salvar_carro(self.carros, self.dicionario)
                            self.manipulacao.loc[len(self.manipulacao), 'manipulacao'] = b.carro.tempo_carro[len(b.carro.tempo_carro)-1]
                            self.financas.loc[len(self.financas), "faturamento"] = b.preco_lavagem
                            self.salvar_financas(self.financas, self.manipulacao, self.dicionario_prod)
                            print(f"Lavagem finalizada em {(b.carro.tempo_carro[len(b.carro.tempo_carro)-1])/60:.2f} minutos")
                            input("\nDigite Enter para continuar ")
                            print("\nDeseja atualizar o estoque pós lavagem?\n\n1 - Sim\n0 - Não")
                            resp3 = inteiro_menu(input("\nIndique uma das opções do menu: "),1)
                            if resp3 == 0:
                                return
                            else: 
                                self.editar_estoque()
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
                                print(f"Lavagem pausada em {(b.tempopausado - b.tempo)/60:.2f} minutos de trabalho")
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
        except ErroDeTipo as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")        

    def gastos(self):
        """
        Menu de finanças com relatórios rápidos.

        Opções:
            1 - Registros: exibe o DataFrame self.financas (com NaN preenchidos por display).
            2 - Gasto, faturamento e lucro: mostra soma, média, mínimo, máximo e lucro total.
            3 - Horas trabalhadas e R$/h: mostra horas totais e calcula reais por hora (R$/h).

        Observações:
            - A coluna 'gasto' é atualizada a partir de self.dicionario_prod['valor'] no início.
            - Usa np.sum/np.mean/np.min/np.max; assegure que colunas não vazias para evitar warnings/exceptions.

        """
        while True:
            self.financas['gasto'] = self.dicionario_prod['valor']
            print("\n=== SOFTWARE DE GESTÃO ===")
            print("Feito por: Bruno Bellinaso e Thomáz França\n")
            print("- Finanças e Estátisticas -\n")
            print("1 - Registros")
            print("2 - Gasto, faturamento e lucro")
            print("3 - Horas trabalhadas e R$/h")
            print("0 - Voltar\n")
            try:
                resp = inteiro_menu(input("Escolha uma opção acima: "), 3)
                if resp == 0:
                    break
                elif resp == 1:
                    if len(self.financas) != 0:
                        print("\nRegistro de valores\n")
                        print(self.financas.fillna(0))
                    else:
                        print('\nNão há registros.')
                    input("\nPressione Enter para continuar")
                elif resp == 2:
                    print("\nGastos, faturamento e lucro totais\n")
                    print(f"Gasto total: {np.sum(self.financas['gasto'])}\n")
                    print(f"Média de gastos: {np.mean(self.financas.loc[self.financas['gasto'] != 0, 'gasto'])}\n")
                    print(f"Gasto mínimo: {np.min(self.financas.loc[self.financas['gasto'] != 0, 'gasto'])}\n")
                    print(f"Gasto máximo: {np.max(self.financas.loc[self.financas['gasto'] != 0, 'gasto'])}\n")
                    print(f"Faturamento total: {np.sum(self.financas['faturamento'])}\n")
                    print(f"Faturamento médio: {np.mean(self.financas.loc[self.financas['faturamento'] != 0, 'faturamento'])}\n")
                    print(f"Lucro total: {(np.sum(self.financas['faturamento']))-(np.sum(self.financas['gasto']))}\n")
                    input("Pressione Enter para continuar")
                elif resp == 3:
                    if np.sum(self.financas['tempo de trabalho'].fillna(0)) != 0:
                        print("\nHoras trabalhadas e R$/h\n")
                        print(f"Horas totais trabalhadas: {(np.sum(self.financas['tempo de trabalho'].fillna(0)))/360:.2f}\n")
                        print(f"Reais por hora trabalhada: {((np.sum(self.financas['faturamento']))-(np.sum(self.financas['gasto'])))/((np.sum(self.financas['tempo de trabalho'].fillna(0)))/360):.2f} R$/h")
                    else:
                        print("Sem horas de trabalho registradas.")
                    input("Pressione Enter para continuar")
            except ErroDeMenu as e:
                print(f"Erro: {e}")
                input(f"Pressione Enter para continuar")
            except ErroDeTipo as e:
                print(f"Erro: {e}")
                input(f"Pressione Enter para continuar")        

    def tempo_por_carro(self):
        """
        Menu de estatísticas por carro e por atributos.

        Opções:
            1 - Dados de lavagem por carro: imprime tempo médio e quantidade de lavagens por carro.
            2 - Carros que mais lavaram: gera DataFrame com contagem de lavagens e ordena do maior para o menor.
            3 - Marcas mais frequentes: mostra a marca mais comum e quantidade de aparições.
            4 - Modelos mais frequentes: mostra o modelo mais comum e quantidade de aparições.
            0 - Voltar

        Observações:
            - As operações usam pandas (value_counts, sort_values) e numpy (mean).
        """
        while True:
            print("\n=== SOFTWARE DE GESTÃO ===")
            print("Feito por: Bruno Bellinaso e Thomáz França\n")
            print("- Finanças e Estátisticas -\n")
            print("1 - Dados de lavagem por carro")
            print("2 - Carros que mais lavaram")
            print("3 - Marcas mais frequentes")
            print("4 - Modelos mais frequentes")
            print("0 - Voltar\n")
            try:
                resp = inteiro_menu(input("Escolha uma opção acima: "), 4)
                if resp == 0:
                    break
                elif resp == 1:
                    if len(self.carros) > 0:
                        for i in self.carros:
                            if len(i.tempo_carro) > 0:
                                print(f"{i} - Tempo médio: {(np.mean(i.tempo_carro))/60:.2f}\n")
                                print(f"Quantidade de lavagens: {i.lav}\n")
                            else: 
                                print(f"{i} - Sem lavagem registrada\n")
                    else:
                        print("\nSem carros registrados.\n")
                    input("Pressione Enter para continuar ")
                elif resp == 2:
                    df = pd.DataFrame({
                        "marca" : [],
                        "modelo" : [],
                        "placa" : [],
                        "quantia de lavagens" : []
                    })
                    if len(self.carros) > 0:
                        for i in self.carros:
                            df.loc[len(df)] = i.dici()
                            if np.sum(df['quantia de lavagens']) != 0:
                                print(df.sort_values('quantia de lavagens', ascending=False))
                            else: 
                                print("\nNenhuma lavagem foi feita!\n")
                    else:
                        print("\nSem carros registrados.")
                    input("Pressione Enter para continuar ")
                elif resp == 3:
                    if len(self.carros) > 0:
                        print(f"\nMarca mais frequente: {self.dicionario['marca'].value_counts().idxmax()}\n")
                        print(f"Quantidade de aparições: {self.dicionario['marca'].value_counts().max()}\n")
                    else:
                        print("\nSem carros registrados.")
                    input("Pressione Enter para continuar ")
                elif resp == 4:
                    if len(self.carros) > 0:
                        print(f"\nModelo mais frequente: {self.dicionario['modelo'].value_counts().idxmax()}")
                        print(f"Quantidade de aparições: {self.dicionario['modelo'].value_counts().max()}\n")
                    else:
                        print("\nSem carros registrados.")
                    input("Pressione Enter para continuar ")
            except ErroDeMenu as e:
                print(f"Erro: {e}")
                input(f"Pressione Enter para continuar")
            except ErroDeTipo as e:
                print(f"Erro: {e}")
                input(f"Pressione Enter para continuar")        
                        