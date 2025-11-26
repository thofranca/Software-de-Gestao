while True:
    
    print("\n=== SOFTWARE DE GESTÃO ===")
    print("Feito por: Bruno Belinasso e Thomáz França\n")
    print("1 - Cadastrar bem patrimonial")
    print("2 - Listar bens")
    print("3 - Editar bem")
    print("4 - Excluir bem")
    print("5 - Gerar relatório")
    print("0 - Sair\n")

    try:

        resp = inteiro_menu(input("Escolha uma opção acima: "), 5)

        if resp == 0:
            print("Saindo do sistema.")
            break
        elif resp == 1:
            cp.cadastrar_bem()
        elif resp == 2:
            cp.listar_bens()
            input("\nPressione Enter para continuar")
        elif resp == 3:
            cp.editar_bem()
        elif resp == 4:
            cp.excluir_bem()
        elif resp == 5:
            cp.gerar_relatorio()
        

    except ErroDeMenu as e:
        print(f"Erro: {e}")
        input(f"Pressione Enter para continuar")
    except ErroDeTipo as e:
        print(f"Erro: {e}")
        input(f"Pressione Enter para continuar")