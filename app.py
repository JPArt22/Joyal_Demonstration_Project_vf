"""
Proyecto MD - Demostración de Joyal a la Fórmula de Cayley
===========================================================

Aplicación interactiva para explorar la biyección entre árboles etiquetados
y funciones, con sistema de criptografía Hill Cipher integrado.

Autor: Universidad Nacional de Colombia - Matemáticas Discretas
"""

import sys
import os

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import start_application


def main():
    """Punto de entrada principal de la aplicación."""
    try:
        start_application()
    except KeyboardInterrupt:
        print("\n\nAplicación cerrada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError crítico: {e}")
        print("\nPor favor reporte este error si persiste.")
        input("\nPresione Enter para salir...")
        sys.exit(1)


if __name__ == "__main__":
    main()
