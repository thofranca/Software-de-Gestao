import Controle as ct 
from Erros import ErroDeMenu, inteiro_menu

reg = ct.Controle_registro()


def menu_carros():
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

def menu_produtos():
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

def lavagem():
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

def estats():
    reg.carregar_dados()
    while True:
        print("\n=== SOFTWARE DE GESTÃO ===")
        print("Feito por: Bruno Bellinaso e Thomáz França\n")
        print("- Finanças e Estátisticas -\n")
        print("1 - Relação de dados (gastos, faturamento, tempo de serviço)")
        print("2 - Tempo Gasto por Carro")
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