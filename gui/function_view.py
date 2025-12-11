"""
Vista para construir árbol desde función.
Permite al usuario ingresar una función y visualizar el árbol resultante, con opción de encriptado.
"""

import customtkinter as ctk
import random
from gui.graph_canvas import GraphCanvas
from logic import GraphLogic, CryptoEngine


class FunctionView(ctk.CTkFrame):
    """Vista para construir árbol a partir de función."""
    
    def __init__(self, parent, n=9, on_back=None):
        super().__init__(parent, fg_color="#11111b")
        
        self.n = n
        self.graph_logic = GraphLogic(n)
        self.crypto_engine = CryptoEngine(n)
        self.on_back = on_back
        
        # Estado
        self.funcion = [None] * n
        self.camino_vertebra = None
        self.camino_orden = None
        self.camino_inv = None
        self.aristas_vert = []
        self.aristas_dir = []
        self.estado = 0  # 0: ingresar, 1: mostrar bosque, 2: mostrar árbol
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        # Header
        header = ctk.CTkFrame(self, fg_color="#1e1e2e", height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        btn_back = ctk.CTkButton(
            header,
            text="← Volver",
            width=100,
            height=35,
            fg_color="#313244",
            hover_color="#45475a",
            font=("Segoe UI", 13),
            command=self._on_back_clicked
        )
        btn_back.pack(side="left", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            header,
            text=f"Construir Árbol desde Función (n={self.n})",
            font=("Segoe UI", 22, "bold"),
            text_color="#cdd6f4"
        )
        title.pack(side="left", padx=20)
        
        # Contenedor principal
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Panel izquierdo - Canvas
        left = ctk.CTkFrame(main, fg_color="#1e1e2e")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.canvas = GraphCanvas(left, width=700, height=600, n=self.n)
        self.canvas.pack(padx=20, pady=(30, 10))
        
        # Instrucciones debajo del canvas
        instr_frame = ctk.CTkFrame(left, fg_color="#313244")
        instr_frame.pack(padx=20, pady=(0, 20), fill="x")
        
        lbl_instr = ctk.CTkLabel(
            instr_frame,
            text=f"Ingrese f(1), f(2), ... f({self.n}) separados por comas. Ejemplo: {','.join(map(str, range(1, min(self.n+1, 10))))}",
            font=("Segoe UI", 11),
            text_color="#a6adc8",
            justify="center",
            wraplength=700
        )
        lbl_instr.pack(pady=10, padx=15)
        
        # Panel derecho - Controles
        right = ctk.CTkFrame(main, fg_color="#1e1e2e", width=380)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        
        # Título
        lbl_title = ctk.CTkLabel(
            right,
            text="Ingreso de Función",
            font=("Segoe UI", 18, "bold"),
            text_color="#cdd6f4"
        )
        lbl_title.pack(pady=(10, 5))
        
        # Entry para función
        self.entry_funcion = ctk.CTkEntry(
            right,
            placeholder_text="1,2,3,4,5,6,7,8,9",
            height=40,
            font=("Segoe UI", 13)
        )
        self.entry_funcion.pack(padx=20, pady=5, fill="x")
        
        # Botón construir
        self.btn_construir = ctk.CTkButton(
            right,
            text="Construir Bosque",
            fg_color="#89b4fa",
            hover_color="#b4befe",
            text_color="#1e1e2e",
            font=("Segoe UI", 14, "bold"),
            height=40,
            command=self._construir_bosque
        )
        self.btn_construir.pack(padx=20, pady=3, fill="x")
        
        # Mensaje de error
        self.lbl_error = ctk.CTkLabel(
            right,
            text="",
            font=("Segoe UI", 12),
            text_color="#f38ba8",
            wraplength=260
        )
        self.lbl_error.pack(pady=3)
        
        # Título de información
        lbl_info = ctk.CTkLabel(
            right,
            text="Información",
            font=("Segoe UI", 18, "bold"),
            text_color="#cdd6f4"
        )
        lbl_info.pack(pady=(10, 5))
        
        # Panel de información
        self.info_scroll = ctk.CTkScrollableFrame(
            right,
            fg_color="#1e1e2e",
            width=340,
            height=110
        )
        self.info_scroll.pack(padx=20, pady=5, fill="x")
        
        # Botón para generar función aleatoria
        btn_random = ctk.CTkButton(
            right,
            text="🎲 Generar Función Aleatoria",
            fg_color="#89b4fa",
            hover_color="#b4befe",
            text_color="#1e1e2e",
            font=("Segoe UI", 13, "bold"),
            height=40,
            command=self._generar_funcion_aleatoria
        )
        btn_random.pack(pady=5, padx=20, fill="x")
        
        # Botón reset
        btn_reset = ctk.CTkButton(
            right,
            text="Reiniciar",
            fg_color="#f38ba8",
            hover_color="#f5c2e7",
            text_color="#1e1e2e",
            font=("Segoe UI", 13, "bold"),
            command=self._reset
        )
        btn_reset.pack(pady=5, padx=20, fill="x")
        
        self._update_display()
    
    def _construir_bosque(self):
        """Construye el bosque/árbol a partir de la función."""
        texto = self.entry_funcion.get().strip()
        
        if not texto:
            self.lbl_error.configure(text="Por favor ingrese una función")
            return
        
        try:
            valores = [int(x.strip()) for x in texto.split(',')]
            
            if len(valores) != self.n:
                self.lbl_error.configure(text=f"Debe ingresar exactamente {self.n} valores")
                return
            
            if not all(1 <= x <= self.n for x in valores):
                self.lbl_error.configure(text=f"Los valores deben estar entre 1 y {self.n}")
                return
            
            # Convertir a índices 0-(n-1)
            self.funcion = [v - 1 for v in valores]
            
            # Construir árbol
            result = self.graph_logic.construir_arbol_desde_funcion(self.funcion)
            
            self.camino_vertebra = result['camino_vertebra']
            self.camino_orden = result['camino_orden']
            self.camino_inv = result['camino_inv']
            self.aristas_vert = result['aristas_vert']
            self.aristas_dir = result['aristas_dir']
            
            self.estado = 1  # Mostrar bosque
            
            self.lbl_error.configure(text="")
            self.btn_construir.configure(text="Convertir a Árbol", command=self._convertir_arbol)
            
            self._update_display()
            
        except ValueError:
            self.lbl_error.configure(text="Formato inválido. Use números separados por comas")
    
    def _convertir_arbol(self):
        """Convierte el bosque en árbol."""
        self.estado = 2
        self.btn_construir.configure(state="disabled")
        self._update_display()
    
    def _update_display(self):
        """Actualiza la visualización."""
        if self.estado == 0:
            self.canvas.clear_graph()
            # Dibujar solo vértices
            for i in range(self.n):
                self.canvas.draw_vertex(i)
        
        elif self.estado == 1:
            # Mostrar bosque (función completa)
            self.canvas.draw_graph_tree(
                None, None, None,
                self.funcion
            )
        
        elif self.estado == 2:
            # Mostrar árbol con vértebra
            self.canvas.draw_graph_tree(
                None,
                self.aristas_vert,
                self.aristas_dir,
                None
            )
        
        self._update_info_panel()
    
    def _update_info_panel(self):
        """Actualiza el panel de información."""
        # Limpiar
        for widget in self.info_scroll.winfo_children():
            widget.destroy()
        
        # Mostrar mensaje de ayuda inicial
        if self.estado == 0:
            lbl_help = ctk.CTkLabel(
                self.info_scroll,
                text="COMO USAR",
                font=("Segoe UI", 16, "bold"),
                text_color="#ffffff"
            )
            lbl_help.pack(pady=(15, 10), padx=10)
            
            lbl_step = ctk.CTkLabel(
                self.info_scroll,
                text=f"1. Ingrese una funcion f(V)\n   con {self.n} valores\n\n2. Los valores deben estar\n   entre 1 y {self.n}\n\n3. Separe los valores\n   por comas\n\nEjemplo:\n1,2,3,4,5,6,7,8,9",
                font=("Segoe UI", 13),
                text_color="#ffffff",
                justify="left",
                wraplength=300
            )
            lbl_step.pack(pady=15, padx=15)
            
            sep = ctk.CTkFrame(self.info_scroll, height=2, fg_color="#6c7086")
            sep.pack(fill="x", pady=15, padx=20)
            
            lbl_info = ctk.CTkLabel(
                self.info_scroll,
                text="La demostracion de Joyal\nconvertira la funcion en un arbol\netiquetado.",
                font=("Segoe UI", 11),
                text_color="#ffffff",
                justify="center",
                wraplength=300
            )
            lbl_info.pack(pady=(10, 15), padx=10)
            return
        
        if self.estado >= 1 and None not in self.funcion:
            # Mostrar función
            lbl = ctk.CTkLabel(
                self.info_scroll,
                text="Funcion f(V):",
                font=("Segoe UI", 14, "bold"),
                text_color="#ffffff"
            )
            lbl.pack(anchor="w", pady=(10, 5), padx=10)
            
            func_str = ", ".join(str(f + 1) for f in self.funcion)
            lbl_func = ctk.CTkLabel(
                self.info_scroll,
                text=f"[{func_str}]",
                font=("Consolas", 12),
                text_color="#89b4fa",
                wraplength=300,
                justify="center"
            )
            lbl_func.pack(pady=(0, 15), padx=10)
            
            # Vértices en ciclo
            if self.camino_orden:
                sep = ctk.CTkFrame(self.info_scroll, height=2, fg_color="#6c7086")
                sep.pack(fill="x", pady=10, padx=20)
                
                lbl = ctk.CTkLabel(
                    self.info_scroll,
                    text="Vertices en ciclos:",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#ffffff"
                )
                lbl.pack(anchor="w", pady=(10, 5), padx=10)
                
                ciclo_str = ", ".join(str(v + 1) for v in self.camino_orden)
                lbl_ciclo = ctk.CTkLabel(
                    self.info_scroll,
                    text=f"[{ciclo_str}]",
                    font=("Consolas", 12),
                    text_color="#f9e2af",
                    wraplength=300,
                    justify="center"
                )
                lbl_ciclo.pack(pady=(0, 15), padx=10)
            
            # Vértebra
            if self.camino_vertebra and self.estado >= 2:
                sep = ctk.CTkFrame(self.info_scroll, height=2, fg_color="#6c7086")
                sep.pack(fill="x", pady=10, padx=20)
                
                lbl = ctk.CTkLabel(
                    self.info_scroll,
                    text="Vertebra:",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#ffffff"
                )
                lbl.pack(anchor="w", pady=(10, 5), padx=10)
                
                vert_str = " -> ".join(str(v + 1) for v in self.camino_vertebra)
                lbl_vert = ctk.CTkLabel(
                    self.info_scroll,
                    text=vert_str,
                    font=("Consolas", 12),
                    text_color="#f38ba8",
                    wraplength=300,
                    justify="center"
                )
                lbl_vert.pack(pady=(0, 15), padx=10)
                
                # Mapeo
                sep = ctk.CTkFrame(self.info_scroll, height=2, fg_color="#6c7086")
                sep.pack(fill="x", pady=10, padx=20)
                
                lbl = ctk.CTkLabel(
                    self.info_scroll,
                    text="Mapeo (V -> f(V)):",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#ffffff"
                )
                lbl.pack(anchor="w", pady=(10, 5), padx=10)
                
                for i in range(len(self.camino_orden)):
                    v = self.camino_orden[i]
                    fv = self.camino_inv[i]
                    
                    map_str = f"{v + 1} -> {fv + 1}"
                    lbl_map = ctk.CTkLabel(
                        self.info_scroll,
                        text=map_str,
                        font=("Consolas", 12),
                        text_color="#a6e3a1"
                    )
                    lbl_map.pack(anchor="w", pady=2, padx=10)
    
    def _generar_funcion_aleatoria(self):
        """Genera una función aleatoria con n valores."""
        # Generar función aleatoria (cada valor puede ser de 1 a n)
        funcion_aleatoria = [random.randint(1, self.n) for _ in range(self.n)]
        
        # Colocar en el entry
        self.entry_funcion.delete(0, "end")
        self.entry_funcion.insert(0, ",".join(map(str, funcion_aleatoria)))
        
        # Construir automáticamente
        self._construir_bosque()
    
    def _reset(self):
        """Reinicia la vista."""
        self.graph_logic = GraphLogic(self.n)
        self.crypto_engine = CryptoEngine(self.n)
        
        self.funcion = [None] * self.n
        self.camino_vertebra = None
        self.camino_orden = None
        self.camino_inv = None
        self.aristas_vert = []
        self.aristas_dir = []
        self.estado = 0
        
        self.entry_funcion.delete(0, "end")
        self.lbl_error.configure(text="")
        
        self.btn_construir.configure(
            text="Construir Bosque",
            command=self._construir_bosque,
            state="normal"
        )
        
        self._update_display()
    
    def _on_back_clicked(self):
        """Maneja el botón de volver."""
        self._reset()
        if self.on_back:
            self.on_back()
