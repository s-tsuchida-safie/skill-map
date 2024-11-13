import re

def encrypt_bit_shift(text: str, shift: int) -> str:
    encrypted_text = ''
    for char in text:
        encrypted_text += chr(ord(char) + shift) if re.match(r'[a-zA-Z]', char) else char
    return encrypted_text

print(encrypt_bit_shift('Hello, World', 3)) # Khoor, Zruog