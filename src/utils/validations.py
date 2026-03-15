import re


def validate_document_number(value: str) -> bool:
    value = re.sub(r"\D", "", value)

    if len(value) == 11:
        return validate_cpf(value)
    elif len(value) == 14:
        return validate_cnpj(value)

    return False


def validate_cpf(cpf: str) -> bool:
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    total = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = (total * 10 % 11) % 10

    total = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = (total * 10 % 11) % 10

    return cpf[-2:] == f"{digit1}{digit2}"


def validate_cnpj(cnpj: str) -> bool:
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights2 = [6] + weights1

    total = sum(int(cnpj[i]) * weights1[i] for i in range(12))
    digit1 = 11 - total % 11
    digit1 = digit1 if digit1 < 10 else 0

    total = sum(int(cnpj[i]) * weights2[i] for i in range(13))
    digit2 = 11 - total % 11
    digit2 = digit2 if digit2 < 10 else 0

    return cnpj[-2:] == f"{digit1}{digit2}"
