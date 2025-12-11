"""
Vista para construir árbol desde función.
Permite al usuario ingresar una función y visualizar el árbol resultante, con opción de encriptado.
"""

import customtkinter as ctk
from gui.graph_canvas import GraphCanvas
from logic import GraphLogic, CryptoEngine


class FunctionView(ctk.CTkFrame):
    """Vista para construir árbol a partir de función."""
    
    def __init__(self, parent, on_back=None):
        super().__init__(parent, fg_color="#11111b")
        
        self.graph_logic = GraphLogic()
        self.crypto_engine = CryptoEngine()
        self.on_back = on_back
        
        # Estado
        self.funcion = [None] * 9
        self.camino_vertebra = None
        self.camino_orden = None
        self.camino_inv = None
        self.aristas_vert = []
        self.aristas_dir = []
        self.estado = 0  # 0: ingresar, 1: mostrar bosque, 2: mostrar árbol
        self.modo_encriptar = False
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
            text="Construir Árbol desde Función",
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
        
        self.canvas = GraphCanvas(left, width=700, height=600)
        self.canvas.pack(padx=20, pady=(30, 10))
        
        # Instrucciones debajo del canvas
        instr_frame = ctk.CTkFrame(left, fg_color="#313244")
        instr_frame.pack(padx=20, pady=(0, 20), fill="x")
        
        lbl_instr = ctk.CTkLabel(
            instr_frame,
            text="Ingrese f(1), f(2), ... f(9) separados por comas. Ejemplo: 1,2,3,6,6,6,7,8,9",
            font=("Segoe UI", 11),
            text_color="#a6adc8",
            justify="center",
            wraplength=700
        )
        lbl_instr.pack(pady=10, padx=15)
        
        # Panel derecho - Controles
        right = ctk.CTkFrame(main, fg_color="#1e1e2e", width=300)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        
        # Título
        lbl_title = ctk.CTkLabel(
            right,
            text="Ingreso de Función",
            font=("Segoe UI", 18, "bold"),
            text_color="#cdd6f4"
        )
        lbl_title.pack(pady=(20, 10))
        
        # Entry para función
        self.entry_funcion = ctk.CTkEntry(
            right,
            placeholder_text="1,2,3,4,5,6,7,8,9",
            height=40,
            font=("Segoe UI", 13)
        )
        self.entry_funcion.pack(padx=20, pady=10, fill="x")
        
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
        self.btn_construir.pack(padx=20, pady=5, fill="x")
        
        # Mensaje de error
        self.lbl_error = ctk.CTkLabel(
            right,
            text="",
            font=("Segoe UI", 12),
            text_color="#f38ba8",
            wraplength=260
        )
        self.lbl_error.pack(pady=5)
        
        # Panel de información (movido más arriba)
        info_frame = ctk.CTkFrame(right, fg_color="#313244")
        info_frame.pack(padx=20, pady=(5, 10), fill="both", expand=True)
        
        lbl_info = ctk.CTkLabel(
            info_frame,
            text="Información",
            font=("Segoe UI", 15, "bold"),
            text_color="#cdd6f4"
        )
        lbl_info.pack(pady=(10, 5))
        
        self.info_scroll = ctk.CTkScrollableFrame(
            info_frame,
            fg_color="#45475a",
            width=240,
            height=250
        )
        self.info_scroll.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Panel de encriptación
        crypto_frame = ctk.CTkFrame(right, fg_color="#313244")
        crypto_frame.pack(padx=20, pady=10, fill="x")
        
        lbl_crypto = ctk.CTkLabel(
            crypto_frame,
            text="🔒 ENCRIPTACIÓN",
            font=("Segoe UI", 15, "bold"),
            text_color="#cdd6f4"
        )
        lbl_crypto.pack(pady=(10, 5))
        
        self.lbl_crypto_status = ctk.CTkLabel(
            crypto_frame,
            text="Ingrese una función para encriptar",
            font=("Segoe UI", 10),
            text_color="#6c7086"
        )
        self.lbl_crypto_status.pack(pady=(0, 5))
        
        self.btn_encrypt = ctk.CTkButton(
            crypto_frame,
            text="✓ ENCRIPTAR TEXTO",
            fg_color="#a6e3a1",
            hover_color="#94e2d5",
            text_color="#1e1e2e",
            font=("Segoe UI", 13, "bold"),
            height=40,
            command=self._toggle_encrypt,
            state="disabled"
        )
        self.btn_encrypt.pack(pady=5, padx=10, fill="x")
        
        self.entry_crypto = ctk.CTkEntry(
            crypto_frame,
            placeholder_text="Ingrese texto a encriptar aquí...",
            height=40,
            font=("Segoe UI", 13)
        )
        self.entry_crypto.pack(pady=5, padx=10, fill="x")
        self.entry_crypto.pack_forget()
        
        self.btn_process = ctk.CTkButton(
            crypto_frame,
            text="Encriptar",
            fg_color="#89b4fa",
            hover_color="#b4befe",
            text_color="#1e1e2e",
            font=("Segoe UI", 12, "bold"),
            command=self._process_encrypt
        )
        self.btn_process.pack(pady=5, padx=10, fill="x")
        self.btn_process.pack_forget()
        
        self.lbl_resultado = ctk.CTkLabel(
            crypto_frame,
            text="",
            font=("Segoe UI", 12),
            text_color="#a6e3a1",
            wraplength=250
        )
        self.lbl_resultado.pack(pady=5, padx=10)
        
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
        
        self._update_display()
    
    def _construir_bosque(self):
        """Construye el bosque/árbol a partir de la función."""
        texto = self.entry_funcion.get().strip()
        
        if not texto:
            self.lbl_error.configure(text="Por favor ingrese una función")
            return
        
        try:
            valores = [int(x.strip()) for x in texto.split(',')]
            
            if len(valores) != 9:
                self.lbl_error.configure(text="Debe ingresar exactamente 9 valores")
                return
            
            if not all(1 <= x <= 9 for x in valores):
                self.lbl_error.configure(text="Los valores deben estar entre 1 y 9")
                return
            
            # Convertir a índices 0-8
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
            
            # Configurar encriptación
            self.crypto_engine.set_key_from_function(self.funcion)
            self.btn_encrypt.configure(state="normal")
            self.lbl_crypto_status.configure(
                text="✓ Función lista - Ya puede encriptar",
                text_color="#a6e3a1"
            )
            
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
            for i in range(9):
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
        
        if self.estado >= 1 and None not in self.funcion:
            # Mostrar función
            lbl = ctk.CTkLabel(
                self.info_scroll,
                text="Función f(V):",
                font=("Segoe UI", 14, "bold"),
                text_color="#cdd6f4"
            )
            lbl.pack(anchor="w", pady=(5, 2))
            
            func_str = ", ".join(str(f + 1) for f in self.funcion)
            lbl_func = ctk.CTkLabel(
                self.info_scroll,
                text=f"[{func_str}]",
                font=("Consolas", 13),
                text_color="#89b4fa"
            )
            lbl_func.pack(anchor="w", pady=(0, 10))
            
            # Vértices en ciclo
            if self.camino_orden:
                lbl = ctk.CTkLabel(
                    self.info_scroll,
                    text="Vértices en ciclos:",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#cdd6f4"
                )
                lbl.pack(anchor="w", pady=(5, 2))
                
                ciclo_str = ", ".join(str(v + 1) for v in self.camino_orden)
                lbl_ciclo = ctk.CTkLabel(
                    self.info_scroll,
                    text=f"[{ciclo_str}]",
                    font=("Consolas", 13),
                    text_color="#f9e2af"
                )
                lbl_ciclo.pack(anchor="w", pady=(0, 10))
            
            # Vértebra
            if self.camino_vertebra and self.estado >= 2:
                lbl = ctk.CTkLabel(
                    self.info_scroll,
                    text="Vértebra:",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#cdd6f4"
                )
                lbl.pack(anchor="w", pady=(5, 2))
                
                vert_str = " → ".join(str(v + 1) for v in self.camino_vertebra)
                lbl_vert = ctk.CTkLabel(
                    self.info_scroll,
                    text=vert_str,
                    font=("Consolas", 13),
                    text_color="#f38ba8"
                )
                lbl_vert.pack(anchor="w", pady=(0, 10))
                
                # Mapeo
                lbl = ctk.CTkLabel(
                    self.info_scroll,
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
                        self.info_scroll,
                        text=map_str,
                        font=("Consolas", 13),
                        text_color="#a6e3a1"
                    )
                    lbl_map.pack(anchor="w")
    
    def _toggle_encrypt(self):
        """Activa/desactiva el modo encriptación."""
        self.modo_encriptar = not self.modo_encriptar
        
        if self.modo_encriptar:
            self.btn_encrypt.configure(text="✗ Cerrar Encriptación", fg_color="#f38ba8")
            self.entry_crypto.pack(pady=5, padx=10, fill="x")
            self.btn_process.pack(pady=5, padx=10, fill="x")
            self.lbl_crypto_status.configure(
                text="Ingrese texto plano y presione el botón",
                text_color="#89b4fa"
            )
        else:
            self.btn_encrypt.configure(text="✓ ENCRIPTAR TEXTO", fg_color="#a6e3a1")
            self.entry_crypto.pack_forget()
            self.btn_process.pack_forget()
            self.lbl_resultado.configure(text="")
            self.lbl_crypto_status.configure(
                text="✓ Función lista - Ya puede encriptar",
                text_color="#a6e3a1"
            )
    
    def _process_encrypt(self):
        """Procesa la encriptación."""
        texto = self.entry_crypto.get()
        
        if not texto:
            self.lbl_resultado.configure(
                text="Por favor ingrese texto",
                text_color="#f38ba8"
            )
            return
        
        try:
            resultado = self.crypto_engine.encrypt(texto)
            self.lbl_resultado.configure(
                text=f"Encriptado:\n{resultado}",
                text_color="#a6e3a1"
            )
        except Exception as e:
            self.lbl_resultado.configure(
                text=f"Error: {str(e)}",
                text_color="#f38ba8"
            )
    
    def _reset(self):
        """Reinicia la vista."""
        self.graph_logic = GraphLogic()
        self.crypto_engine = CryptoEngine()
        
        self.funcion = [None] * 9
        self.camino_vertebra = None
        self.camino_orden = None
        self.camino_inv = None
        self.aristas_vert = []
        self.aristas_dir = []
        self.estado = 0
        self.modo_encriptar = False
        
        self.entry_funcion.delete(0, "end")
        self.entry_crypto.delete(0, "end")
        self.lbl_error.configure(text="")
        self.lbl_resultado.configure(text="")
        
        self.btn_construir.configure(
            text="Construir Bosque",
            command=self._construir_bosque,
            state="normal"
        )
        self.btn_encrypt.configure(state="disabled")
        self.lbl_crypto_status.configure(
            text="Ingrese una función para encriptar",
            text_color="#6c7086"
        )
        
        if self.modo_encriptar:
            self._toggle_encrypt()
        
        self._update_display()
    
    def _on_back_clicked(self):
        """Maneja el botón de volver."""
        self._reset()
        if self.on_back:
            self.on_back()
