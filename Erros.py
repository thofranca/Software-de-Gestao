class ErroDeMenu(Exception):
    pass

class ErroDeTipo(Exception):
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

def placa(valor, lis):
    if len(lis) > 0:
        for i in lis:
            if i.placa == valor:
                raise ErroDePlaca("Parece que o carro ja existe no sistema!")
        else:
            return valor
    else:
        return valor
