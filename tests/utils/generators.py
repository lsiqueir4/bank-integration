import random
from uuid import uuid4


def generate_individual_document_number():
    numbers = [random.randint(0, 9) for _ in range(9)]

    numbers_sum = sum([(10 - i) * numbers[i] for i in range(9)])
    first_digit = 11 - numbers_sum % 11
    first_digit = 0 if first_digit >= 10 else first_digit
    numbers.append(first_digit)

    numbers_sum = sum([(11 - i) * numbers[i] for i in range(10)])
    second_digit = 11 - numbers_sum % 11
    second_digit = 0 if second_digit >= 10 else second_digit
    numbers.append(second_digit)

    return "".join(map(str, numbers))


def generate_company_document_number():
    base = [random.randint(0, 9) for _ in range(8)]
    base += [0, 0, 0, 1]

    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_ = sum([base[i] * weights_1[i] for i in range(12)])
    remainder = sum_ % 11
    first_digit = 0 if remainder < 2 else 11 - remainder
    base.append(first_digit)

    weights_2 = [6] + weights_1
    sum_ = sum([base[i] * weights_2[i] for i in range(13)])
    remainder = sum_ % 11
    second_digit = 0 if remainder < 2 else 11 - remainder
    base.append(second_digit)

    return "".join(map(str, base))


def generate_random_email(domain="example.com"):
    prefix = f"user_{str(uuid4())}"
    return f"{prefix}@{domain}"
