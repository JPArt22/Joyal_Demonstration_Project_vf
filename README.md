# Proyecto MD - Demostración de Joyal a la Fórmula de Cayley

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## 📋 Descripción

**Proyecto MD** es una aplicación interactiva de escritorio que implementa la demostración combinatoria de André Joyal para la **Fórmula de Cayley**, la cual establece que existen exactamente $n^{n-2}$ árboles etiquetados con $n$ vértices.

La aplicación permite a los usuarios explorar la biyección entre árboles etiquetados de 9 vértices y funciones $f: V \rightarrow V$, además de implementar un sistema de **cifrado Hill Cipher** de 9×9 basado en las funciones generadas.

### Teorema de Cayley

El teorema de Cayley establece que:

$$T(n) = n^{n-2}$$

donde $T(n)$ es el número de árboles etiquetados distintos con $n$ vértices.

Para $n = 9$: $T(9) = 9^7 = 4,782,969$ árboles distintos.

### Demostración de Joyal

André Joyal proporcionó una elegante demostración biyectiva que establece una correspondencia uno a uno entre:
- **Árboles etiquetados** con $n$ vértices
- **Funciones** $f: \{1, 2, ..., n\} \rightarrow \{1, 2, ..., n\}$

La demostración utiliza el concepto de **vértebra**: un camino simple desde un vértice inicial hasta un vértice final en el árbol, donde todos los demás vértices se dirigen hacia la vértebra.

## ✨ Características

### Funcionalidades Principales

1. **Construcción de Función desde Árbol**
   - Construcción interactiva de árboles mediante clicks
   - Selección de vértices inicial y final
   - Generación automática de función correspondiente
   - Visualización de vértebra y aristas dirigidas
   - **Desencriptación** de textos usando la función generada

2. **Construcción de Árbol desde Función**
   - Ingreso de función como lista de 9 valores
   - Visualización del bosque funcional (con ciclos)
   - Conversión automática a árbol con vértebra
   - Identificación de vértices en ciclos
   - **Encriptación** de textos usando la función generada

3. **Criptografía Hill Cipher 9×9**
   - Generación de matriz de cifrado a partir de función
   - Alfabeto extendido: A-Z, Ñ, espacio, coma, punto (30 caracteres)
   - Cifrado por bloques de 9 caracteres
   - Encriptación y desencriptación robusta

### Interfaz Gráfica

- **Diseño minimalista moderno** con tema oscuro (Catppuccin Mocha)
- **Visualización elegante** de grafos con canvas interactivo
- **Animaciones sutiles** en hover de vértices
- **Paleta de colores profesional** y accesible
- **Navegación intuitiva** entre modos
- **Paneles informativos** con scroll y actualizaciones en tiempo real

## 🎨 Diseño Visual

La aplicación utiliza una paleta de colores cuidadosamente seleccionada:

- **Fondo principal**: `#11111b` (negro suave)
- **Contenedores**: `#1e1e2e` (gris oscuro)
- **Vértices**: `#89b4fa` (azul claro)
- **Vértebras**: `#f38ba8` (rosa/rojo)
- **Aristas dirigidas**: `#cba6f7` (púrpura)
- **Texto**: `#cdd6f4` (gris claro)
- **Acentos**: `#a6e3a1` (verde menta)

## 🚀 Instalación y Ejecución

### Requisitos del Sistema

- **Sistema Operativo**: Windows 10 o superior
- **Python**: 3.8 o superior
- **Espacio en disco**: ~100 MB (incluyendo dependencias)
- **RAM**: Mínimo 2 GB

### Método 1: Ejecución Automática (Recomendado)

1. **Descargue o clone el repositorio**:
   ```bash
   git clone <repository-url>
   cd JOyal_3
   ```

2. **Ejecute el archivo `run.bat`**:
   - Haga doble clic en `run.bat`
   - El script automáticamente:
     - Verificará la instalación de Python
     - Creará un entorno virtual
     - Instalará todas las dependencias (numpy, customtkinter)
     - Iniciará la aplicación

### Método 2: Instalación Manual

1. **Clone el repositorio**:
   ```bash
   git clone <repository-url>
   cd JOyal_3
   ```

2. **Cree un entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Active el entorno virtual**:
   ```bash
   venv\Scripts\activate
   ```

4. **Instale las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecute la aplicación**:
   ```bash
   python app.py
   ```

### Dependencias

El proyecto requiere las siguientes librerías de Python:

```
numpy>=1.20.0          # Computación numérica y matrices
customtkinter>=5.0.0   # Interfaz gráfica moderna
```

## 📖 Guía de Uso

### Modo 1: Construir Función desde Árbol

1. **Conectar Vértices**:
   - Click en un vértice para seleccionarlo
   - Click en otro vértice para conectarlos
   - Conecte todos los 9 vértices sin formar ciclos (8 aristas)

2. **Seleccionar Vértices Especiales**:
   - Una vez conectado el árbol, seleccione el **vértice inicial**
   - Luego seleccione el **vértice final**

3. **Visualizar Resultado**:
   - La vértebra se muestra en líneas punteadas rojas
   - Las aristas dirigidas se muestran con flechas púrpura
   - El panel derecho muestra la función generada

4. **Desencriptar Texto** (Opcional):
   - Click en "Activar Desencriptación"
   - Ingrese el texto cifrado
   - Click en "Desencriptar"

### Modo 2: Construir Árbol desde Función

1. **Ingresar Función**:
   - Ingrese 9 valores separados por comas
   - Formato: `f(1),f(2),...,f(9)`
   - Ejemplo: `1,2,3,6,6,6,7,8,9`
   - Los valores deben estar entre 1 y 9

2. **Construir Bosque**:
   - Click en "Construir Bosque"
   - Se visualizará el grafo funcional con posibles ciclos y bucles

3. **Convertir a Árbol**:
   - Click en "Convertir a Árbol"
   - Los ciclos se convierten en vértebra
   - Se muestran aristas dirigidas hacia la vértebra

4. **Encriptar Texto** (Opcional):
   - Click en "Activar Encriptación"
   - Ingrese el texto plano
   - Click en "Encriptar"

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
JOyal_3/
│
├── app.py                    # Punto de entrada principal
├── run.bat                   # Script de instalación y ejecución
├── requirements.txt          # Dependencias de Python
├── README.md                 # Este archivo
│
├── logic/                    # Módulos de lógica de negocio
│   ├── __init__.py          # Inicialización del paquete
│   ├── graph_logic.py       # Lógica de grafos y árboles
│   ├── crypto_logic.py      # Cifrado Hill Cipher
│   └── math_utils.py        # Utilidades matemáticas (matrices, determinantes)
│
└── gui/                      # Módulos de interfaz gráfica
    ├── __init__.py          # Inicialización del paquete
    ├── main_window.py       # Ventana principal y menú
    ├── tree_view.py         # Vista de construcción desde árbol
    ├── function_view.py     # Vista de construcción desde función
    └── graph_canvas.py      # Canvas para visualización de grafos
```

### Módulos Principales

#### `logic/graph_logic.py`
- Clase `GraphLogic`: Gestión de grafos con conjuntos disjuntos
- Algoritmos de búsqueda (DFS) y detección de ciclos
- Construcción de función desde árbol y viceversa
- Cálculo de vértebras y dirección de aristas

#### `logic/crypto_logic.py`
- Clase `CryptoEngine`: Motor de encriptación/desencriptación
- Implementación de Hill Cipher 9×9
- Conversión de caracteres a números (alfabeto extendido)
- Manejo de longitud variable con padding

#### `logic/math_utils.py`
- Algoritmo de Bareiss para determinantes enteros
- Cálculo de matriz adjunta e inversa modular
- Generación de matrices invertibles desde funciones
- Multiplicación matriz-vector modular

#### `gui/main_window.py`
- Clase `MainWindow`: Ventana principal con navegación
- Menú de bienvenida elegante
- Gestión de vistas y transiciones

#### `gui/tree_view.py` y `gui/function_view.py`
- Vistas especializadas para cada modo
- Paneles de información dinámica
- Integración con lógica de negocio
- Controles de encriptación/desencriptación

#### `gui/graph_canvas.py`
- Canvas personalizado para dibujo de grafos
- Renderizado de vértices con sombras
- Aristas simples, dirigidas y vértebras
- Bucles (self-loops) con estilo elíptico
- Detección de hover y eventos de mouse

## 🔐 Criptografía

### Alfabeto Extendido

El sistema utiliza un alfabeto de **30 caracteres**:

```
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z Ñ , . ESPACIO
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29
```

### Proceso de Cifrado

1. **Conversión**: Texto → Números (con longitud embebida)
2. **Padding**: Rellenar a múltiplo de 9 con espacios
3. **Cifrado**: Multiplicación por matriz de clave (módulo 30)
4. **Conversión**: Números → Texto cifrado

### Proceso de Descifrado

1. **Conversión**: Texto cifrado → Números
2. **Descifrado**: Multiplicación por matriz inversa (módulo 30)
3. **Extracción**: Recuperar longitud original
4. **Conversión**: Números → Texto plano

### Generación de Matriz de Clave

La matriz de cifrado 9×9 se genera determinísticamente a partir de la función:

```python
M[i][j] = (f[i] * (j + 1) + (f[j] + 1)) mod 30
```

Si la matriz no es invertible módulo 30, se utiliza una matriz diagonal ajustada.

## 🔄 Flujo de la Aplicación

### Diagrama de Flujo General

```
[Inicio]
   ↓
[Menú Principal]
   ├──→ [Modo 1: Función desde Árbol]
   │      ├──→ Conectar vértices
   │      ├──→ Seleccionar inicio/fin
   │      ├──→ Generar función
   │      └──→ Desencriptar (opcional)
   │
   └──→ [Modo 2: Árbol desde Función]
          ├──→ Ingresar función
          ├──→ Visualizar bosque
          ├──→ Convertir a árbol
          └──→ Encriptar (opcional)
```

### Algoritmo de Construcción (Modo 1)

1. Usuario construye árbol conectando vértices
2. Validación: No formar ciclos (Union-Find)
3. Árbol completo: 9 vértices, 8 aristas
4. Selección de vértice inicial `v_i`
5. Selección de vértice final `v_f`
6. DFS: Encontrar camino `v_i → v_f` (vértebra)
7. Asignar función en vértebra: `f(v_k) = v_{k+1}` invertido
8. Dirigir aristas restantes hacia `v_f` (BFS)
9. Completar función: `f(v) = vértice_siguiente`

### Algoritmo de Construcción (Modo 2)

1. Usuario ingresa función `f(1),...,f(9)`
2. Construir grafo dirigido: `v → f(v)`
3. Detectar ciclos usando búsqueda de caminos
4. Identificar vértices en ciclos (vértebra)
5. Revertir orden de vértebra
6. Resto de vértices forman aristas dirigidas
7. Visualización: Vértebra + Aristas dirigidas

## 👥 Autores

**Universidad Nacional de Colombia** - Bogotá, Colombia  
Curso: Matemáticas Discretas
**Proyecto**: Demostración de Joyal a la Fórmula de Cayley  

### Equipo de Desarrollo

- **[Nombre del Autor 1]** - Implementación de lógica de grafos
- **[Nombre del Autor 2]** - Desarrollo de interfaz gráfica
- **[Nombre del Autor 3]** - Sistema de criptografía

### Agradecimientos

- **André Joyal**: Por la elegante demostración combinatoria
- **Arthur Cayley**: Por el teorema fundamental
- **Comunidad Open Source**: Por las herramientas utilizadas

### Herramientas de IA

Algunos métodos fueron desarrollados con apoyo de herramientas de inteligencia artificial:
- **ChatGPT** (OpenAI): Algoritmo de Bareiss, generación de matrices
- **Deepseek**: Optimización de detección de ciclos, renderizado de bucles

## 📚 Referencias

### Artículos y Publicaciones

1. **Joyal, A.** (1981). "Une théorie combinatoire des séries formelles". *Advances in Mathematics*, 42(1), 1-82.

2. **Cayley, A.** (1889). "A theorem on trees". *Quarterly Journal of Mathematics*, 23, 376-378.

3. **Stanley, R. P.** (2011). *Enumerative Combinatorics*, Volume 2. Cambridge University Press.

4. **Aigner, M., & Ziegler, G. M.** (2018). *Proofs from THE BOOK* (6th ed.). Springer. (Capítulo sobre Cayley's Formula)

### Recursos en Línea

- [Wikipedia: Cayley's Formula](https://en.wikipedia.org/wiki/Cayley%27s_formula)
- [Wikipedia: Hill Cipher](https://en.wikipedia.org/wiki/Hill_cipher)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2024 Universidad Nacional de Colombia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🐛 Reporte de Errores y Contribuciones

Si encuentra algún error o desea contribuir al proyecto:

1. Abra un **Issue** describiendo el problema o sugerencia
2. Para contribuciones:
   - Fork el repositorio
   - Cree una rama para su característica (`git checkout -b feature/nueva-caracteristica`)
   - Commit sus cambios (`git commit -am 'Agregar nueva característica'`)
   - Push a la rama (`git push origin feature/nueva-caracteristica`)
   - Abra un Pull Request

## 📞 Contacto

**Universidad del Norte**  
Departamento de Matemáticas y Estadística  
Barranquilla, Colombia

Email: [contacto@uninorte.edu.co](mailto:contacto@uninorte.edu.co)

---

**Nota**: Este proyecto es con fines educativos como parte del curso de Matemáticas Discretas. El sistema de criptografía implementado es una demostración académica y no debe utilizarse para propósitos de seguridad real en producción.

---

*Desarrollado con Python 🐍 y CustomTkinter 🎨*

*"Elegancia en la simplicidad" - Filosofía de diseño del proyecto*
