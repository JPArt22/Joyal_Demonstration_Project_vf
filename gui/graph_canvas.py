"""
Canvas personalizado para visualización de grafos.
Dibuja vértices, aristas, aristas dirigidas y vértebras con estilo moderno.
"""

import math
import tkinter as tk
from tkinter import Canvas


class GraphCanvas(Canvas):
    """Canvas especializado para dibujar grafos de manera elegante."""
    
    # Colores de la paleta minimalista
    COLOR_BG = "#1e1e2e"
    COLOR_VERTEX = "#89b4fa"
    COLOR_VERTEX_HOVER = "#b4befe"
    COLOR_VERTEX_TEXT = "#1e1e2e"
    COLOR_EDGE = "#585b70"
    COLOR_DIRECTED = "#cba6f7"
    COLOR_VERTEBRA = "#f38ba8"
    COLOR_ARROW = "#cba6f7"
    COLOR_LOOP = "#a6e3a1"
    
    def __init__(self, parent, width=700, height=700, **kwargs):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=self.COLOR_BG,
            highlightthickness=0,
            **kwargs
        )
        
        self.vertice_rad = 24
        # Ajustar el centro hacia abajo para evitar corte del vértice superior
        self.vertice_pos = self._calculate_positions(width // 2, height // 2 + 30, 250)
        self.hover_vertex = None
        
        self.bind("<Motion>", self._on_mouse_move)
    
    def _calculate_positions(self, cx, cy, radius):
        """Calcula las posiciones de los vértices en círculo."""
        positions = []
        for i in range(9):
            angle = math.radians(i * 40)
            x = cx + radius * math.sin(angle)
            y = cy - radius * math.cos(angle)
            positions.append((x, y))
        return positions
    
    def _on_mouse_move(self, event):
        """Maneja el hover sobre vértices."""
        old_hover = self.hover_vertex
        self.hover_vertex = None
        
        for i, (x, y) in enumerate(self.vertice_pos):
            if math.hypot(event.x - x, event.y - y) <= self.vertice_rad:
                self.hover_vertex = i
                break
        
        if old_hover != self.hover_vertex:
            self.event_generate("<<VertexHover>>")
    
    def clear_graph(self):
        """Limpia el canvas."""
        self.delete("all")
    
    def draw_edge(self, v1, v2, color=None):
        """Dibuja una arista simple entre dos vértices."""
        if color is None:
            color = self.COLOR_EDGE
        
        x1, y1 = self.vertice_pos[v1]
        x2, y2 = self.vertice_pos[v2]
        
        self.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=3,
            tags="edge"
        )
    
    def draw_directed_edge(self, v1, v2, color=None):
        """Dibuja una arista dirigida con flecha."""
        if color is None:
            color = self.COLOR_DIRECTED
        
        x1, y1 = self.vertice_pos[v1]
        x2, y2 = self.vertice_pos[v2]
        
        # Calcular puntos ajustados por el radio
        total = math.hypot(x2 - x1, y2 - y1)
        if total == 0:
            return
        
        sx = x1 + (self.vertice_rad / total) * (x2 - x1)
        sy = y1 + (self.vertice_rad / total) * (y2 - y1)
        ex = x2 - (self.vertice_rad / total) * (x2 - x1)
        ey = y2 - (self.vertice_rad / total) * (y2 - y1)
        
        # Línea
        self.create_line(
            sx, sy, ex, ey,
            fill=color,
            width=3,
            arrow=tk.LAST,
            arrowshape=(12, 15, 6),
            tags="directed"
        )
    
    def draw_vertebra_edge(self, v1, v2):
        """Dibuja una arista de vértebra (línea punteada roja)."""
        x1, y1 = self.vertice_pos[v1]
        x2, y2 = self.vertice_pos[v2]
        
        self.create_line(
            x1, y1, x2, y2,
            fill=self.COLOR_VERTEBRA,
            width=4,
            dash=(8, 6),
            tags="vertebra"
        )
    
    def draw_loop(self, vertex):
        """
        Dibuja un bucle (self-loop) en un vértice.
        Método desarrollado con apoyo de IA (ChatGPT, Deepseek).
        """
        x, y = self.vertice_pos[vertex]
        
        # Crear un arco elíptico arriba del vértice
        offset_x = 6
        offset_y = -self.vertice_rad + 2
        center_x = x + offset_x
        center_y = y + offset_y
        
        rx = 22
        ry = 16
        
        # Dibujar arco
        bbox = [
            center_x - rx, center_y - ry,
            center_x + rx, center_y + ry
        ]
        
        self.create_arc(
            bbox,
            start=20,
            extent=320,
            outline=self.COLOR_LOOP,
            width=3,
            style=tk.ARC,
            tags="loop"
        )
        
        # Flecha en el extremo
        angle = math.radians(200)
        tip_x = center_x + rx * math.cos(angle)
        tip_y = center_y + ry * math.sin(angle)
        
        # Triángulo de flecha
        arrow_size = 8
        self.create_polygon(
            tip_x, tip_y,
            tip_x - arrow_size, tip_y - arrow_size * 0.5,
            tip_x - arrow_size * 0.7, tip_y + arrow_size * 0.3,
            fill=self.COLOR_LOOP,
            outline=self.COLOR_LOOP,
            tags="loop"
        )
    
    def draw_vertex(self, vertex, label=None, highlight=False):
        """Dibuja un vértice con su etiqueta."""
        x, y = self.vertice_pos[vertex]
        
        if label is None:
            label = str(vertex + 1)
        
        # Color según hover
        color = self.COLOR_VERTEX_HOVER if highlight else self.COLOR_VERTEX
        
        # Círculo con sombra
        shadow_offset = 3
        self.create_oval(
            x - self.vertice_rad + shadow_offset,
            y - self.vertice_rad + shadow_offset,
            x + self.vertice_rad + shadow_offset,
            y + self.vertice_rad + shadow_offset,
            fill="#11111b",
            outline="",
            tags="shadow"
        )
        
        # Círculo principal
        self.create_oval(
            x - self.vertice_rad,
            y - self.vertice_rad,
            x + self.vertice_rad,
            y + self.vertice_rad,
            fill=color,
            outline="#cdd6f4",
            width=2,
            tags=f"vertex_{vertex}"
        )
        
        # Etiqueta
        self.create_text(
            x, y,
            text=label,
            fill=self.COLOR_VERTEX_TEXT,
            font=("Segoe UI", 14, "bold"),
            tags=f"label_{vertex}"
        )
    
    def draw_graph_tree(self, aristas, aristas_vert=None, aristas_dir=None, funcion=None):
        """Dibuja un grafo completo con todas sus componentes."""
        self.clear_graph()
        
        # Primero dibujar aristas simples
        if aristas:
            for v1, v2 in aristas:
                # Verificar si es parte de la vértebra
                is_vertebra = False
                if aristas_vert:
                    for a, b in aristas_vert:
                        if (v1 == a and v2 == b) or (v1 == b and v2 == a):
                            is_vertebra = True
                            break
                
                if not is_vertebra:
                    self.draw_edge(v1, v2)
        
        # Luego vértebras
        if aristas_vert:
            for v1, v2 in aristas_vert:
                self.draw_vertebra_edge(v1, v2)
        
        # Aristas dirigidas
        if aristas_dir:
            for v1, v2 in aristas_dir:
                self.draw_directed_edge(v1, v2)
        
        # Función (para modo función)
        if funcion:
            for i, f in enumerate(funcion):
                if f is not None:
                    if i != f:
                        self.draw_directed_edge(i, f)
                    else:
                        self.draw_loop(i)
        
        # Finalmente vértices (siempre encima)
        for i in range(9):
            highlight = (i == self.hover_vertex)
            self.draw_vertex(i, highlight=highlight)
    
    def get_vertex_at_pos(self, x, y):
        """Obtiene el vértice en una posición del mouse."""
        for i, (vx, vy) in enumerate(self.vertice_pos):
            if math.hypot(x - vx, y - vy) <= self.vertice_rad:
                return i
        return None
