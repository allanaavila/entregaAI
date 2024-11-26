import re


def validar_cnpj(cnpj: str) -> str | None:
    """
    Valida e formata um CNPJ.

    O CNPJ é validado de acordo com as seguintes regras:
    1. Deve conter 14 dígitos após remover caracteres não numéricos.
    2. Não pode ser uma sequência repetida (e.g., "11111111111111").
    3. Os dois dígitos verificadores são validados com base no cálculo oficial.

    :param cnpj: String contendo o CNPJ a ser validado.
    :return: O CNPJ formatado (apenas números) se for válido, ou None se for inválido.
    """
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return None

    if cnpj == cnpj[0] * 14:
        return None

    def calcular_digito(cnpj_parcial, pesos):
        soma = sum(int(digito) * peso for digito, peso in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos_primeiro = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_segundo = [6] + pesos_primeiro

    cnpj_base = cnpj[:12]
    primeiro_digito = calcular_digito(cnpj_base, pesos_primeiro)
    segundo_digito = calcular_digito(cnpj_base + primeiro_digito, pesos_segundo)

    if cnpj[-2:] == primeiro_digito + segundo_digito:
        return cnpj
    else:
        return None
