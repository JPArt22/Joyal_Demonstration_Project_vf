import sys
sys.path.insert(0, '.')

from logic.crypto_logic import CryptoEngine

# Crear instancia
ce = CryptoEngine()

# Establecer función (como en el código original: 1,2,3,6,6,6,7,8,9 → 0,1,2,5,5,5,6,7,8)
funcion = [0, 1, 2, 5, 5, 5, 6, 7, 8]
print(f"Función: {funcion}")

# Establecer clave
ce.set_key_from_function(funcion)
print(f"Clave establecida: {ce.key is not None}")
print(f"Tipo de clave: {type(ce.key)}")

# Intentar encriptar
try:
    texto = "HOLA"
    print(f"\nTexto original: {texto}")
    encriptado = ce.encrypt(texto)
    print(f"Texto encriptado: {encriptado}")
    
    # Desencriptar
    desencriptado = ce.decrypt(encriptado)
    print(f"Texto desencriptado: {desencriptado}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
