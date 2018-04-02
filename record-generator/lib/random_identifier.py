import string
from random import choice

def random_identifier(length=22):
    return ''.join(choice(string.ascii_lowercase) for _ in range(length))
