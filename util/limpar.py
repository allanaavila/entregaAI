import os

def limpar_tela():
    # Para sistemas baseados em Unix (Linux/Mac)
    if os.name == 'posix':
        os.system('clear')
    # Para sistemas Windows
    elif os.name == 'nt':
        os.system('cls')
