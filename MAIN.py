import Controle as ct 
from Erros import ErroDeMenu, inteiro_menu
import MENUS as mn
menu = mn

while True:
    
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