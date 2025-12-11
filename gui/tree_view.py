"""
Vista para construir función desde árbol.
Permite al usuario construir un árbol y generar una función, con opción de desencriptado.
"""

import customtkinter as ctk
from gui.graph_canvas import GraphCanvas
from logic import GraphLogic, CryptoEngine


class TreeView(ctk.CTkFrame):
    """Vista para construir función a partir de árbol."""
    
    def __init__(self, parent, n=9, on_back=None):
        super().__init__(parent, fg_color="#11111b")
        
        self.n = n
        self.graph_logic = GraphLogic(n)
        self.crypto_engine = CryptoEngine(n)
        self.on_back = on_back
        
        # Estado
        self.vertice_1 = None
        self.vertice_ini = None
        self.vertice_fin = None
        self.funcion = [None] * n
        self.camino_vertebra = None
        self.camino_orden = None
        self.camino_inv = None
        self.aristas_vert = []
        self.aristas_dir = []
        self.estado = 0  # 0: conectar, 1: error ciclo, 2: elegir inicio, 3: elegir fin, 4: listo
        self.modo_desencriptar = False
        self.texto_resultado = ""
        
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
            text=f"Construir Función desde Árbol (n={self.n})",
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
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        
        # Mensaje de estado
        self.lbl_estado = ctk.CTkLabel(
            left,
            text="PASO 1: Conecte todos los vértices sin formar ciclos",
            font=("Segoe UI", 14, "bold"),
            text_color="#89b4fa",
            wraplength=650
        )
        self.lbl_estado.pack(pady=(5, 5))
        
        # Mensaje de ayuda adicional
        self.lbl_ayuda = ctk.CTkLabel(
            left,
            text=f"Click en un vértice, luego en otro para conectarlos.\nEl árbol debe ser completamente conexo.\nNo se permiten ciclos.",
            font=("Segoe UI", 11),
            text_color="#a6adc8",
            wraplength=650,
            justify="center"
        )
        self.lbl_ayuda.pack(pady=(0, 20))
        
        # Panel derecho - Info y controles
        right = ctk.CTkFrame(main, fg_color="#1e1e2e", width=380)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        
        # Título panel
        lbl_info = ctk.CTkLabel(
            right,
            text="Información",
            font=("Segoe UI", 18, "bold"),
            text_color="#cdd6f4"
        )
        lbl_info.pack(pady=(20, 10))
        
        # Scroll para info
        scroll = ctk.CTkScrollableFrame(
            right,
            fg_color="#313244",
            width=340,
            height=400,
            orientation="both"
        )
        scroll.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.info_container = scroll
        
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
        btn_reset.pack(pady=10, padx=20, fill="x")
        
        # Dibujar estado inicial
        self._update_display()
    
    def _on_canvas_click(self, event):
        """Maneja clicks en el canvas."""
        vertex = self.canvas.get_vertex_at_pos(event.x, event.y)
        
        if vertex is None:
            return
        
        # Fase 1: Conectar árbol
        if not self.graph_logic.grafoconexo():
            if self.vertice_1 is None:
                self.vertice_1 = vertex
            else:
                if vertex != self.vertice_1:
                    v1, v2 = self.vertice_1, vertex
                    
                    if not self.graph_logic.agregar_arista(v1, v2):
                        self.estado = 1  # Error: ciclo
                    else:
                        self.estado = 0
                
                self.vertice_1 = None
            
            if self.graph_logic.grafoconexo() and len(self.graph_logic.aristas) == 8:
                self.estado = 2  # Listo para elegir inicio
        
        # Fase 2: Elegir vértice inicial
        elif None in self.funcion:
            if self.vertice_ini is None:
                self.vertice_ini = vertex
                self.estado = 3
            elif self.vertice_fin is None:
                self.vertice_fin = vertex
                self._construir_funcion()
                self.estado = 4
        
        self._update_display()
    
    def _construir_funcion(self):
        """Construye la función a partir del árbol."""
        result = self.graph_logic.construir_funcion_desde_arbol(
            self.vertice_ini,
            self.vertice_fin
        )
        
        self.funcion = result['funcion']
        self.camino_vertebra = result['camino_vertebra']
        self.camino_orden = result['camino_orden']
        self.camino_inv = result['camino_inv']
        self.aristas_vert = result['aristas_vert']
        self.aristas_dir = result['aristas_dir']
        
        # Configurar clave de encriptación
        self.crypto_engine.set_key_from_function(self.funcion)
    
    def _update_display(self):
        """Actualiza la visualización."""
        # Actualizar canvas
        if self.estado < 4:
            self.canvas.draw_graph_tree(
                self.graph_logic.aristas,
                None, None, None
            )
        else:
            self.canvas.draw_graph_tree(
                self.graph_logic.aristas,
                self.aristas_vert,
                self.aristas_dir,
                None
            )
        
        # Actualizar mensaje de estado
        mensajes = [
            "PASO 1: Conecte todos los vértices",
            "ERROR: Se detectó un ciclo. Los árboles no pueden tener ciclos.\nIntente otra conexión.",
            "PASO 2: Árbol completado. Ahora seleccione el VÉRTICE INICIAL",
            "PASO 3: Ahora seleccione el VÉRTICE FINAL\n(puede ser el mismo que el inicial)",
            "COMPLETADO: Función construida exitosamente"
        ]
        
        ayudas = [
            f"Click en un vértice, luego en otro para conectarlos.\nEl árbol debe ser completamente conexo.\nNo se permiten ciclos.",
            "Un ciclo ocurre cuando ya existe un camino entre dos vértices\ny los conecta nuevamente. Reinicie si es necesario.",
            "El vértice inicial será el punto de partida de la vértebra.\nClick en cualquier vértice del árbol.",
            "El vértice final será el punto de llegada de la vértebra.\nSe encontrará el camino entre inicio y fin.",
            "La función f(V) ha sido generada usando la demostración de Joyal.\nAhora puede desencriptar textos con esta función."
        ]
        
        colores = ["#89b4fa", "#f38ba8", "#a6e3a1", "#a6e3a1", "#a6e3a1"]
        
        self.lbl_estado.configure(
            text=mensajes[self.estado],
            text_color=colores[self.estado]
        )
        
        self.lbl_ayuda.configure(
            text=ayudas[self.estado],
            text_color="#a6adc8" if self.estado != 1 else "#f5c2e7"
        )
        
        # Actualizar panel de información
        self._update_info_panel()
    
    def _update_info_panel(self):
        """Actualiza el panel de información."""
        # Limpiar
        for widget in self.info_container.winfo_children():
            widget.destroy()
        
        if self.estado >= 4 and None not in self.funcion:
            # Mostrar función
            lbl = ctk.CTkLabel(
                self.info_container,
                text="Función f(V):",
                font=("Segoe UI", 14, "bold"),
                text_color="#cdd6f4"
            )
            lbl.pack(anchor="w", pady=(5, 2))
            
            func_str = ", ".join(str(f + 1) for f in self.funcion if f is not None)
            lbl_func = ctk.CTkLabel(
                self.info_container,
                text=f"[{func_str}]",
                font=("Consolas", 13),
                text_color="#89b4fa",
                wraplength=0
            )
            lbl_func.pack(anchor="w", pady=(0, 10))
            
            # Vértebra
            if self.camino_vertebra:
                lbl = ctk.CTkLabel(
                    self.info_container,
                    text="Vértebra (inicio → fin):",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#cdd6f4"
                )
                lbl.pack(anchor="w", pady=(5, 2))
                
                vert_str = " → ".join(str(v + 1) for v in self.camino_vertebra)
                lbl_vert = ctk.CTkLabel(
                    self.info_container,
                    text=vert_str,
                    font=("Consolas", 13),
                    text_color="#f38ba8",
                    wraplength=0
                )
                lbl_vert.pack(anchor="w", pady=(0, 10))
            
            # Tabla V y f(V)
            if self.camino_orden and self.camino_inv:
                lbl = ctk.CTkLabel(
                    self.info_container,
                    text="Mapeo (V → f(V)):",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#cdd6f4"
                )
                lbl.pack(anchor="w", pady=(5, 2))
                
                for i in range(len(self.camino_orden)):
                    v = self.camino_orden[i]
                    fv = self.camino_inv[i]
                    
                    map_str = f"{v + 1} → {fv + 1}"
                    lbl_map = ctk.CTkLabel(
                        self.info_container,
                        text=map_str,
                        font=("Consolas", 13),
                        text_color="#a6e3a1"
                    )
                    lbl_map.pack(anchor="w")
    
    def _reset(self):
        """Reinicia la vista."""
        self.graph_logic.reset()
        self.crypto_engine = CryptoEngine(self.n)
        
        self.vertice_1 = None
        self.vertice_ini = None
        self.vertice_fin = None
        self.funcion = [None] * self.n
        self.camino_vertebra = None
        self.camino_orden = None
        self.camino_inv = None
        self.aristas_vert = []
        self.aristas_dir = []
        self.estado = 0
        self.modo_desencriptar = False
        self.texto_resultado = ""
        
        self._update_display()
    
    def _on_back_clicked(self):
        """Maneja el botón de volver."""
        self._reset()
        if self.on_back:
            self.on_back()
