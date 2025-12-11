"""
Módulo de lógica de criptografía.
Implementa el cifrado Hill Cipher de 9×9 con alfabeto extendido.
"""

from logic.math_utils import mat_mul_vec_nxn, inverse_matrix_mod, get_matrix_from_function


# Alfabeto extendido: A-Z + Ñ + , . espacio
ALPHABET = {chr(ord('A') + i): i for i in range(26)}
ALPHABET['Ñ'] = 26
ALPHABET[','] = 27
ALPHABET['.'] = 28
ALPHABET[' '] = 29

REV_ALPH = {v: k for k, v in ALPHABET.items()}

MOD = 30
BLOCK = 9


def char_a_num(ch):
    """Convierte un carácter a número."""
    ch = ch.upper()
    if ch == 'Ñ' or ch == 'ñ':
        return ALPHABET['Ñ']
    if ch in ALPHABET:
        return ALPHABET[ch]
    return ALPHABET[' ']


def num_a_char(n):
    """Convierte un número a carácter."""
    n = n % MOD
    return REV_ALPH.get(n, ' ')


def encode_text_to_numbers(text):
    """
    Codifica texto a números con longitud embebida.
    Formato: [high, low, ...chars...] con padding a múltiplo de BLOCK.
    """
    L = len(text)
    if L > 30 * 30 - 1:
        raise ValueError("Text too long (max 899 characters).")
    
    high = L // MOD
    low = L % MOD
    nums = [high, low]
    
    for ch in text:
        nums.append(char_a_num(ch))
    
    while len(nums) % BLOCK != 0:
        nums.append(ALPHABET[' '])
    
    return nums


def decode_numbers_to_text(nums):
    """Decodifica números a texto usando longitud embebida."""
    if len(nums) < 2:
        return ""
    
    high, low = nums[0], nums[1]
    L = high * MOD + low
    chars = []
    pos = 2
    needed = L
    
    while needed > 0 and pos < len(nums):
        chars.append(num_a_char(nums[pos]))
        pos += 1
        needed -= 1
    
    return ''.join(chars)


def hill_encrypt_numbers(nums, key, MOD=30):
    """Encripta números usando cifrado Hill."""
    out = []
    n = BLOCK
    
    for i in range(0, len(nums), n):
        block = nums[i:i + n]
        v = mat_mul_vec_nxn(key, block, MOD)
        out.extend(v)
    
    return out


def hill_decrypt_numbers(nums, key, MOD=30):
    """Desencripta números usando cifrado Hill."""
    inv = inverse_matrix_mod(key, MOD)
    if inv is None:
        raise ValueError("Key not invertible modulo {}".format(MOD))
    
    out = []
    n = BLOCK
    
    for i in range(0, len(nums), n):
        block = nums[i:i + n]
        v = mat_mul_vec_nxn(inv, block, MOD)
        out.extend(v)
    
    return out


def encrypt_text(plain, key):
    """Encripta texto plano usando una clave matricial."""
    nums = encode_text_to_numbers(plain)
    enc_nums = hill_encrypt_numbers(nums, key, MOD)
    return ''.join(num_a_char(n) for n in enc_nums)


def decrypt_text(ciphertext, key):
    """Desencripta texto cifrado usando una clave matricial."""
    nums = [char_a_num(ch) for ch in ciphertext]
    
    if len(nums) % BLOCK != 0:
        raise ValueError("Invalid ciphertext length (must be multiple of block size).")
    
    dec_nums = hill_decrypt_numbers(nums, key, MOD)
    return decode_numbers_to_text(dec_nums)


class CryptoEngine:
    """Motor de criptografía que maneja encriptación y desencriptación."""
    
    def __init__(self):
        self.key = None
        
    def set_key_from_function(self, funcion):
        """Establece la clave a partir de una función."""
        self.key = get_matrix_from_function(funcion)
        
    def encrypt(self, plaintext):
        """Encripta texto plano."""
        if self.key is None:
            raise ValueError("Key not set. Call set_key_from_function first.")
        return encrypt_text(plaintext, self.key)
    
    def decrypt(self, ciphertext):
        """Desencripta texto cifrado."""
        if self.key is None:
            raise ValueError("Key not set. Call set_key_from_function first.")
        
        # Asegurar que el texto cifrado tenga longitud múltiplo de BLOCK
        while len(ciphertext) % BLOCK != 0:
            ciphertext += " "
        
        return decrypt_text(ciphertext, self.key)
