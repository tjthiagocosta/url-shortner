import string
import random


def generate_short_key(length: int = 6) -> str:
    """
    Generate a random short key for URL shortening.
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))
