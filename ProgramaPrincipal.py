import Controle as ct 
from Erros import ErroDeMenu, inteiro_menu

lav = ct.Controle_Lavagens()
lav.carregar_dados()

while True:
    
    print("\n=== SOFTWARE DE GESTÃO ===")
    print("Feito por: Bruno Belinasso e Thomáz França\n")
    print("1 - Cadastrar carro")
    print("2 - Listar carros")
    print("3 - Editar carro")
    print("4 - Excluir carro")
    print("0 - Sair\n")
    
    try:

        resp = inteiro_menu(input("Escolha uma opção acima: "), 4)

        if resp == 0:
            print("Saindo do sistema.")
            break
        elif resp == 1:
            lav.cadastrar_carro()
        elif resp == 2:
            lav.listar_carros()
            input("\nPressione Enter para continuar")
        elif resp == 3:
            lav.editar_carros()
        elif resp == 4:
            lav.excluir_carro()

    except ErroDeMenu as e:
        print(f"Erro: {e}")
        input(f"Pressione Enter para continuar")



