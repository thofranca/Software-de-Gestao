class ErroDeMenu(Exception):
    pass

class ErroDeTipo(Exception):
    pass

class ErroDeSituação(Exception):
    pass

class ErroDePlaca(Exception):
    pass

def inteiro_menu(valor, num):

    try:
        valor = int(valor)
    except ValueError:
        raise ErroDeTipo("O valor inserido precisa ser um número inteiro.")
        
    if valor < 0 or valor > num: 
        raise ErroDeMenu("O valor deve ser uma das opções do menu!")
        
    return valor

def inteiro(valor):

    try:
        valor = int(valor)
    except ValueError:
        raise ErroDeTipo("O valor inserido precisa ser um número inteiro.")
        
    return valor

def situacao(valor):
    a = ("em uso", "disponível", "em manutenção")
    for i in a: 
        if valor.lower() == i:
            return valor
    else:
        raise ErroDeSituação("Situação inválida!")

def placa(valor, lis):
    for i in lis:
        if i.placa == valor:
            raise ErroDePlaca("Parece que o carro ja existe no sistema!")
    else:
        return valor
