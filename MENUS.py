import Controle as ct 
from Erros import ErroDeMenu, ErroDeTipo, inteiro_menu

reg = ct.Controle_registro()


def menu_carros():
    '''

    Exibe o menu de gerenciamento de carros e executa as operações escolhidas pelo usuário.

    Este menu permite cadastrar, listar, editar e excluir carros do sistema.
    A função carrega os dados inicialmente e permanece em loop até que o
    usuário selecione a opção de voltar.

    Funcionalidades disponíveis:
        1. Cadastrar um novo carro
        2. Listar todos os carros cadastrados
        3. Editar os dados de um carro existente
        4. Excluir um carro do sistema
        0. Voltar ao menu anterior

    Fluxo:
        - O usuário escolhe uma opção usando a função `inteiro_menu()`.
        - Cada opção chama o método correspondente do objeto `reg`.
        - Em caso de erro de entrada, exceções personalizadas são tratadas
          e uma mensagem adequada é exibida.

    Exceções tratadas:
        ErroDeMenu: Lançada quando o usuário informa um número fora das opções permitidas.
        ErroDeTipo: Lançada quando a entrada não corresponde ao tipo esperado.

    Retorna:
        None: A função não retorna valor; apenas controla fluxo e chamadas.

    '''

    reg.carregar_dados()
    while True:
        
        print("\n=== SOFTWARE DE GESTÃO ===")
        print("Feito por: Bruno Bellinaso e Thomáz França\n")
        print("- GERENCIAMENTO DE CARROS -\n")
        print("1 - Cadastrar carro")
        print("2 - Listar carros")
        print("3 - Editar carro")
        print("4 - Excluir carro")
        print("0 - Voltar\n")
        
        try:

            resp = inteiro_menu(input("Escolha uma opção acima: "), 4)

            if resp == 0:
                break
            elif resp == 1:
                reg.cadastrar_carro()
            elif resp == 2:
                reg.listar_carros()
                input("\nPressione Enter para continuar")
            elif resp == 3:
                reg.editar_carros()
            elif resp == 4:
                reg.excluir_carro()

        except ErroDeMenu as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")
        except ErroDeTipo as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")        

def menu_produtos():
    '''

    Exibe o menu de gerenciamento de produtos e executa as operações escolhidas pelo usuário.

    Este menu permite cadastrar, listar, editar e excluir produtos do sistema.
    A função carrega os dados inicialmente e permanece em loop até que o
    usuário selecione a opção de voltar.

    Funcionalidades disponíveis:
        1. Cadastrar uma nova compra de produto
        2. Listar todos os produtos cadastrados
        3. Editar os dados de um produto existente
        4. Excluir um produto do sistema
        0. Voltar ao menu anterior

    Fluxo:
        - O usuário escolhe uma opção usando a função `inteiro_menu()`.
        - Cada opção chama o método correspondente do objeto `reg`.
        - Em caso de erro de entrada, exceções personalizadas são tratadas
          e uma mensagem adequada é exibida.

    Exceções tratadas:
        ErroDeMenu: Lançada quando o usuário informa um número fora das opções permitidas.
        ErroDeTipo: Lançada quando a entrada não corresponde ao tipo esperado.

    Retorna:
        None: A função não retorna valor; apenas controla fluxo e chamadas.

    '''
    reg.carregar_dados()
    while True:
        
        print("\n=== SOFTWARE DE GESTÃO ===")
        print("Feito por: Bruno Bellinaso e Thomáz França\n")
        print("- GERENCIAMENTO DE ESTOQUE -\n")
        print("1 - Nova compra")
        print("2 - Listar estoque")
        print("3 - Editar estoque")
        print("4 - Excluir produto")
        print("0 - Voltar\n")
        
        try:

            resp = inteiro_menu(input("Escolha uma opção acima: "), 4)

            if resp == 0:
                return
            elif resp == 1:
                reg.nova_compra()
            elif resp == 2:
                reg.listar_estoque()
                input("\nPressione Enter para continuar")
            elif resp == 3:
                reg.editar_estoque()
            elif resp == 4:
                reg.excluir_produto()
        except ErroDeMenu as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")
        except ErroDeTipo as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")

def lavagem():
    '''

    Exibe o menu de gerenciamento de lavagem e executa as operações escolhidas pelo usuário.

    Este menu permite iniciar, listar, pausar e finalizar lavagens.
    A função carrega os dados inicialmente e permanece em loop até que o
    usuário selecione a opção de voltar.

    Funcionalidades disponíveis:
        1. Iniciar uma nova lavagem
        2. Listar as lavagens em andamento
        3. Pausar, despausar e finalizar uma lavagem
        0. Voltar ao menu anterior

    Fluxo:
        - O usuário escolhe uma opção usando a função `inteiro_menu()`.
        - Cada opção chama o método correspondente do objeto `reg`.
        - Em caso de erro de entrada, exceções personalizadas são tratadas
          e uma mensagem adequada é exibida.

    Exceções tratadas:
        ErroDeMenu: Lançada quando o usuário informa um número fora das opções permitidas.
        ErroDeTipo: Lançada quando a entrada não corresponde ao tipo esperado.

    Retorna:
        None: A função não retorna valor; apenas controla fluxo e chamadas.

    '''
    reg.carregar_dados()
    while True:
        print("\n=== SOFTWARE DE GESTÃO ===")
        print("Feito por: Bruno Bellinaso e Thomáz França\n")
        print("- Lavagem -\n")
        print("1 - Inicar Lavagem")
        print("2 - Lavagens em andamento")
        print("3 - Pausar/Finalizar Lavagem")
        print("0 - Voltar\n")
          
        try:

            resp = inteiro_menu(input("Escolha uma opção acima: "), 3)

            if resp == 0:
                break
            elif resp == 1:
                reg.inicar_lavagem()
            elif resp == 2:
                reg.lavagens_and()
                input("\nPressione Enter para continuar")
            elif resp == 3:
                reg.pausar_finalizar()
        except ErroDeMenu as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")
        except ErroDeTipo as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")

def estats():
    """
    Exibe o menu de finanças e estatísticas do sistema
    
    permitindo ao usuário acessar informações relacionadas aos gastos, 
    faturamento, tempo trabalhado e dados de clientes.

    Funcionalidades disponíveis:
        1. Exibir relação completa de dados financeiros:
           - Gastos totais
           - Faturamento acumulado
           - Tempo total de serviço
           - Cálculos derivados (ex.: média)
        2. Exibir dados relacionados aos clientes, incluindo quantidade de
           lavagens, tempo médio por carro e outras métricas.

    Fluxo:
        - Os dados são carregados no início com `reg.carregar_dados()`.
        - O usuário escolhe uma opção por meio da função `inteiro_menu()`.
        - Cada escolha direciona para um relatório específico dentro de `reg`.

    Exceções tratadas:
        ErroDeMenu: Disparada quando a opção informada está fora do intervalo permitido.
        ErroDeTipo: Disparada quando o tipo da entrada é inválido.

    Retorna:
        None: A função controla apenas fluxo e exibição de relatórios.

    """
    reg.carregar_dados()
    while True:
        print("\n=== SOFTWARE DE GESTÃO ===")
        print("Feito por: Bruno Bellinaso e Thomáz França\n")
        print("- Finanças e Estátisticas -\n")
        print("1 - Relação de dados (gastos, faturamento, tempo de serviço)")
        print("2 - Dados de clientes")
        print("0 - Voltar\n")
          
        try:

            resp = inteiro_menu(input("Escolha uma opção acima: "), 2)

            if resp == 0:
                break
            elif resp == 1:
                reg.gastos()
            elif resp == 2:
                reg.tempo_por_carro()
        except ErroDeMenu as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")
        except ErroDeTipo as e:
            print(f"Erro: {e}")
            input(f"Pressione Enter para continuar")        