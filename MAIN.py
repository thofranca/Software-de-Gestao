import Controle as ct 
from Erros import ErroDeMenu, ErroDeTipo, inteiro_menu
import MENUS as mn
menu = mn

while True:
    """
    
    Exibe o menu principal do software de gestão e direciona o usuário para
    os módulos específicos do sistema: carros, produtos de limpeza, lavagem
    e finanças/estatísticas.

    O menu permanece em execução contínua até que o usuário selecione a opção
    de sair. A cada ciclo, a entrada do usuário é validada pela função
    `inteiro_menu()`, garantindo que apenas opções válidas sejam processadas.

    Funcionalidades disponíveis:
        1. Gerenciar carros:
            - Cadastro, listagem, edição e exclusão de carros.
        2. Gerenciar produtos de limpeza:
            - Controle de estoque, adição, remoção e edição de produtos.
        3. Lavagem:
            - Iniciar lavagem, finalizar lavagem e visualizar registros.
        4. Finanças e estatísticas:
            - Relatórios de gastos, faturamento, tempo de trabalho e
              métricas relativas aos clientes.
        0. Sair:
            - Encerra a execução do sistema.

    Fluxo:
        - O usuário informa uma opção.
        - Cada opção ativa uma função correspondente no objeto `menu`.
        - Erros de input são tratados de forma amigável, impedindo travamentos.

    Exceções tratadas:
        ErroDeMenu: Quando o usuário escolhe uma opção fora do intervalo permitido.
        ErroDeTipo: Quando o tipo de entrada não é compatível (ex.: letras onde deveria ser número).

    Retorna:
        None: Apenas controla o fluxo do aplicativo e chama outros menus.

    """
       
    print("\n=== SOFTWARE DE GESTÃO ===")
    print("Feito por: Bruno Belinasso e Thomáz França\n")
    print("1 - Gerenciar carros")
    print("2 - Gerenciar produtos de limpeza")
    print("3 - Lavagem")
    print("4 - Finanças e Estatísticas")
    print("0 - Sair\n")
    
    try:

        resp = inteiro_menu(input("Escolha uma opção acima: "), 4)

        if resp == 0:
            print("Saindo do sistema.")
            break
        elif resp == 1:
            menu.menu_carros()
        elif resp == 2:
            menu.menu_produtos()        
            input("\nPressione Enter para continuar")
        elif resp == 3:
            menu.lavagem()
        elif resp == 4:
            menu.estats()

    except ErroDeMenu as e:
        print(f"Erro: {e}")
        input(f"Pressione Enter para continuar")
    except ErroDeTipo as e:
        print(f"Erro: {e}")
        input(f"Pressione Enter para continuar")        