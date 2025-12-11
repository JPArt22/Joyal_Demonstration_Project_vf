# Inicio Rápido - Proyecto MD

## Ejecución Inmediata

### Windows (Recomendado)

Simplemente haga **doble clic** en:

```
run.bat
```

Eso es todo! El script automáticamente:
- Verificará Python
- Creará entorno virtual
- Instalará dependencias
- Iniciará la aplicación

---

## Estructura del Proyecto

```
JOyal_3/
├── app.py              ← Punto de entrada
├── run.bat             ← Ejecutable Windows
├── requirements.txt    ← Dependencias
├── README.md           ← Documentación completa
│
├── logic/              ← Lógica de negocio
│   ├── graph_logic.py     (Grafos y árboles)
│   ├── crypto_logic.py    (Encriptación)
│   └── math_utils.py      (Matemáticas)
│
└── gui/                ← Interfaz gráfica
    ├── main_window.py     (Ventana principal)
    ├── tree_view.py       (Vista árbol → función)
    ├── function_view.py   (Vista función → árbol)
    └── graph_canvas.py    (Canvas de grafos)
```

---

## Uso Básico

### Modo 1: Árbol → Función

1. Click en vértices para conectarlos (sin ciclos)
2. Seleccione vértice inicial
3. Seleccione vértice final
4. ¡Función generada!

**Bonus**: Desencripte textos usando la función

### Modo 2: Función → Árbol

1. Ingrese función: `1,2,...,n`
2. Construya el bosque
3. Convierta a árbol
4. ¡Visualice la vértebra!

**Bonus**: Encripte textos usando la función

---

## Características Visuales

- **Diseño minimalista** oscuro (Catppuccin Mocha)
- **Vértices interactivos** con hover
- **Vértebras destacadas** en rojo punteado
- **Aristas dirigidas** con flechas
- **Paneles informativos** dinámicos

---

## Dependencias

Solo 2 librerías:
- `numpy` - Cálculos matriciales
- `customtkinter` - UI moderna

---

## Solución de Problemas

### "Python no encontrado"
→ Instale Python 3.8+ desde [python.org](https://python.org)

### "Error al instalar"
→ Ejecute como Administrador

### Ventana no aparece
→ Verifique que no haya firewall bloqueando

---

**¿Listo? ¡Haga doble click en `run.bat`!**
