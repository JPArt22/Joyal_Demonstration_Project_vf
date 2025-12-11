"""
Script de prueba para verificar el funcionamiento con diferentes valores de n.
"""

import sys
sys.path.insert(0, '.')

from logic.graph_logic import GraphLogic
from logic.crypto_logic import CryptoEngine
from logic.math_utils import get_matrix_from_function

def test_n(n):
    print(f"\n{'='*60}")
    print(f"PROBANDO CON n = {n}")
    print(f"{'='*60}")
    
    # Test GraphLogic
    print(f"\n1. GraphLogic con n={n}")
    gl = GraphLogic(n)
    print(f"   - Vértices inicializados: {len(gl.parent)}")
    print(f"   - Grafo inicializado: {len(gl.grafo)} vértices")
    print(f"   ✓ GraphLogic OK")
    
    # Test CryptoEngine
    print(f"\n2. CryptoEngine con n={n}")
    ce = CryptoEngine(n)
    print(f"   - Tamaño de bloque: {ce.n}")
    
    # Crear función de prueba simple (identidad desplazada)
    funcion = [(i + 1) % n for i in range(n)]
    print(f"   - Función de prueba: {[v+1 for v in funcion]} (base 1)")
    
    # Test matriz
    print(f"\n3. Generando matriz {n}×{n}")
    matriz = get_matrix_from_function(funcion)
    print(f"   - Forma de matriz: {matriz.shape}")
    print(f"   ✓ Matriz generada OK")
    
    # Test encriptación
    print(f"\n4. Test de encriptación")
    ce.set_key_from_function(funcion)
    texto = "HOLA"
    try:
        enc = ce.encrypt(texto)
        print(f"   - Texto original: {texto}")
        print(f"   - Texto encriptado: {enc[:20]}..." if len(enc) > 20 else f"   - Texto encriptado: {enc}")
        
        dec = ce.decrypt(enc)
        print(f"   - Texto desencriptado: {dec}")
        
        if dec == texto:
            print(f"   ✓ Encriptación/Desencriptación OK")
        else:
            print(f"   ✗ ERROR: Desencriptación no coincide")
            return False
    except Exception as e:
        print(f"   ✗ ERROR en encriptación: {e}")
        return False
    
    print(f"\n{'='*60}")
    print(f"✓ TODAS LAS PRUEBAS PASARON PARA n={n}")
    print(f"{'='*60}")
    return True

if __name__ == "__main__":
    valores_n = [3, 5, 7, 9, 12, 15]
    
    print("╔" + "═"*58 + "╗")
    print("║" + " "*15 + "TEST DE SOPORTE PARA n VARIABLE" + " "*12 + "║")
    print("╚" + "═"*58 + "╝")
    
    resultados = {}
    for n in valores_n:
        try:
            resultado = test_n(n)
            resultados[n] = resultado
        except Exception as e:
            print(f"\n✗ ERROR CRÍTICO CON n={n}: {e}")
            import traceback
            traceback.print_exc()
            resultados[n] = False
    
    print("\n\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60)
    for n, resultado in resultados.items():
        status = "✓ PASS" if resultado else "✗ FAIL"
        print(f"n={n:2d}: {status}")
    
    print("\n")
    if all(resultados.values()):
        print("🎉 ¡TODOS LOS TESTS PASARON! 🎉")
        print("La aplicación soporta correctamente n variable.")
    else:
        print("⚠️  ALGUNOS TESTS FALLARON")
        print("Revisar los errores arriba.")
