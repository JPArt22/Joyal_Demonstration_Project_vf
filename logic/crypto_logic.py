"""
Módulo de lógica de criptografía.
Implementa el cifrado Hill Cipher de n×n con alfabeto extendido.
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


def encode_text_to_numbers(text, block_size):
    """
    Codifica texto a números con longitud embebida.
    Formato: [high, low, ...chars...] con padding a múltiplo de block_size.
    """
    L = len(text)
    if L > 30 * 30 - 1:
        raise ValueError("Text too long (max 899 characters).")
    
    high = L // MOD
    low = L % MOD
    nums = [high, low]
    
    for ch in text:
        nums.append(char_a_num(ch))
    
    while len(nums) % block_size != 0:
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


def hill_encrypt_numbers(nums, key, block_size, MOD=30):
    """Encripta números usando cifrado Hill."""
    out = []
    
    for i in range(0, len(nums), block_size):
        block = nums[i:i + block_size]
        v = mat_mul_vec_nxn(key, block, MOD)
        out.extend(v)
    
    return out


def hill_decrypt_numbers(nums, key, block_size, MOD=30):
    """Desencripta números usando cifrado Hill."""
    inv = inverse_matrix_mod(key, MOD)
    if inv is None:
        raise ValueError("Key not invertible modulo {}".format(MOD))
    
    out = []
    
    for i in range(0, len(nums), block_size):
        block = nums[i:i + block_size]
        v = mat_mul_vec_nxn(inv, block, MOD)
        out.extend(v)
    
    return out


def encrypt_text(plain, key, block_size):
    """Encripta texto plano usando una clave matricial."""
    nums = encode_text_to_numbers(plain, block_size)
    enc_nums = hill_encrypt_numbers(nums, key, block_size, MOD)
    return ''.join(num_a_char(n) for n in enc_nums)


def decrypt_text(ciphertext, key, block_size):
    """Desencripta texto cifrado usando una clave matricial."""
    nums = [char_a_num(ch) for ch in ciphertext]
    
    if len(nums) % block_size != 0:
        raise ValueError("Invalid ciphertext length (must be multiple of block size).")
    
    dec_nums = hill_decrypt_numbers(nums, key, block_size, MOD)
    return decode_numbers_to_text(dec_nums)


class CryptoEngine:
    """Motor de criptografía que maneja encriptación y desencriptación."""
    
    def __init__(self, n=9):
        """
        Inicializa el motor de criptografía.
        
        Args:
            n: Tamaño del bloque (igual al número de vértices)
        """
        self.key = None
        self.n = n
        
    def set_key_from_function(self, funcion):
        """Establece la clave a partir de una función."""
        self.key = get_matrix_from_function(funcion)
        
    def encrypt(self, plaintext):
        """Encripta texto plano."""
        if self.key is None:
            raise ValueError("Key not set. Call set_key_from_function first.")
        return encrypt_text(plaintext, self.key, self.n)
    
    def decrypt(self, ciphertext):
        """Desencripta texto cifrado."""
        if self.key is None:
            raise ValueError("Key not set. Call set_key_from_function first.")
        
        # Asegurar que el texto cifrado tenga longitud múltiplo de n
        while len(ciphertext) % self.n != 0:
            ciphertext += " "
        
        return decrypt_text(ciphertext, self.key, self.n)
