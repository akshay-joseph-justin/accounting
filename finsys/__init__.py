import random


def generate_random_number(digits):
    if digits < 1:
        raise ValueError("Number of digits must be at least 1")

    lower_bound = 10 ** (digits - 1)  # Smallest number with given digits
    upper_bound = (10 ** digits) - 1  # Largest number with given digits

    return random.randint(lower_bound, upper_bound)
