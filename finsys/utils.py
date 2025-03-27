import random

def generate_random_number(length=6):
    if length < 1:
        raise ValueError("Length must be at least 1")

    first_digit = random.randint(1, 9)
    remaining_digits = [random.randint(0, 9) for _ in range(length - 1)]

    return int(str(first_digit) + ''.join(map(str, remaining_digits)))
