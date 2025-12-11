"""
Módulo de lógica de grafos para la demostración de la Fórmula de Cayley.
Contiene funciones para manipulación de grafos, árboles y vértebras.
"""

from collections import deque


class GraphLogic:
    """Clase para manejar toda la lógica de grafos y árboles."""
    
    def __init__(self, n=9):
        """
        Inicializa la lógica de grafos.
        
        Args:
            n: Número de vértices (default 9)
        """
        self.n = n
        self.parent = list(range(n))
        self.grafo = [[] for _ in range(n)]
        self.aristas = []
        
    def reset(self):
        """Reinicia el estado del grafo."""
        self.parent = list(range(self.n))
        self.grafo = [[] for _ in range(self.n)]
        self.aristas = []
    
    def find(self, x):
        """Encuentra la raíz del conjunto disjunto."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, a, b):
        """Une dos conjuntos disjuntos."""
        rootA = self.find(a)
        rootB = self.find(b)
        if rootA != rootB:
            self.parent[rootB] = rootA
            return True
        return False
    
    def grafoconexo(self):
        """Verifica si el grafo es conexo."""
        root0 = self.find(0)
        return all(self.find(i) == root0 for i in range(self.n))
    
    def agregar_arista(self, v1, v2):
        """Agrega una arista al grafo si no forma ciclo."""
        if self.find(v1) == self.find(v2):
            return False  # Formaría un ciclo
        
        self.aristas.append((v1, v2))
        self.union(v1, v2)
        self.grafo[v1].append(v2)
        self.grafo[v2].append(v1)
        return True
    
    def depthfirstsearch(self, vertice_ini, vertice_fin, path=None, visited=None):
        """Búsqueda en profundidad para encontrar un camino."""
        if path is None:
            path = []
        if visited is None:
            visited = set()
        
        path = path + [vertice_ini]
        visited.add(vertice_ini)
        
        if vertice_ini == vertice_fin:
            return path
        
        for neighbor in self.grafo[vertice_ini]:
            if neighbor not in visited:
                newpath = self.depthfirstsearch(neighbor, vertice_fin, path, visited)
                if newpath:
                    return newpath
        
        return None
    
    def vertices_en_ciclo(self, aristas_func):
        """Encuentra los vértices que forman ciclos en una función."""
        grafo = {}
        for u, v in aristas_func:
            grafo.setdefault(u, []).append(v)
            grafo.setdefault(v, [])
        
        vertices_cic = set()
        
        for u, p in grafo.items():
            for v in p:
                grafo[u].remove(v)
                camino = self._dfs_dict(grafo, v, u)
                grafo[u].append(v)
                
                if camino:
                    vertices_cic.add(u)
                    vertices_cic.add(v)
        
        return sorted(vertices_cic)
    
    def _dfs_dict(self, graph, start, end, path=None, visited=None):
        """DFS auxiliar para diccionarios."""
        if path is None:
            path = []
        if visited is None:
            visited = set()
        
        path = path + [start]
        visited.add(start)
        
        if start == end:
            return path
        
        if start in graph:
            for neighbor in graph[start]:
                if neighbor not in visited:
                    newpath = self._dfs_dict(graph, neighbor, end, path, visited)
                    if newpath:
                        return newpath
        
        return None
    
    def dirigir_vertices(self, aristas, aristas_vert, vertice_fin):
        """Dirige las aristas hacia el vértice final."""
        distancia_a_fin = [-1] * len(self.grafo)
        queue = deque([vertice_fin])
        distancia_a_fin[vertice_fin] = 0
        
        while queue:
            vertice = queue.popleft()
            for ady in self.grafo[vertice]:
                if distancia_a_fin[ady] == -1:
                    distancia_a_fin[ady] = distancia_a_fin[vertice] + 1
                    queue.append(ady)
        
        aristas_dir = []
        for v1, v2 in aristas:
            en_vert = False
            for a, b in aristas_vert:
                if (v1 == a and v2 == b) or (v1 == b and v2 == a):
                    en_vert = True
                    break
            
            if not en_vert:
                disv1 = distancia_a_fin[v1]
                disv2 = distancia_a_fin[v2]
                
                if disv1 > disv2:
                    aristas_dir.append((v1, v2))
                else:
                    aristas_dir.append((v2, v1))
        
        return aristas_dir
    
    def construir_funcion_desde_arbol(self, vertice_ini, vertice_fin):
        """Construye una función a partir de un árbol con vértices inicial y final."""
        funcion = [None] * self.n
        
        if vertice_ini == vertice_fin:
            aristas_vert = []
            funcion[vertice_ini] = vertice_fin
            camino_vertebra = camino_inv = camino_orden = [vertice_fin]
            aristas_dir = []
        else:
            camino_vertebra = self.depthfirstsearch(vertice_ini, vertice_fin)
            aristas_vert = [(camino_vertebra[i], camino_vertebra[i + 1]) 
                           for i in range(len(camino_vertebra) - 1)]
            camino_orden = sorted(camino_vertebra)
            camino_inv = list(reversed(camino_vertebra))
            
            for i in range(len(camino_orden)):
                funcion[camino_orden[i]] = camino_inv[i]
            
            aristas_dir = self.dirigir_vertices(self.aristas, aristas_vert, vertice_fin)
            for a, b in aristas_dir:
                funcion[a] = b
        
        return {
            'funcion': funcion,
            'camino_vertebra': camino_vertebra,
            'camino_orden': camino_orden,
            'camino_inv': camino_inv,
            'aristas_vert': aristas_vert,
            'aristas_dir': aristas_dir
        }
    
    def construir_arbol_desde_funcion(self, funcion):
        """Construye un árbol a partir de una función."""
        aristas_func = list(enumerate(funcion))
        camino_orden = self.vertices_en_ciclo(aristas_func)
        
        camino_inv = []
        for i in range(len(camino_orden)):
            camino_inv.append(funcion[camino_orden[i]])
        
        camino_vertebra = list(reversed(camino_inv))
        aristas_vert = [(camino_vertebra[i], camino_vertebra[i + 1]) 
                       for i in range(len(camino_vertebra) - 1)]
        
        aristas_dir = []
        for i in range(self.n):
            en_vert = False
            for f in range(len(camino_orden)):
                if i == camino_orden[f]:
                    en_vert = True
                    break
            
            if not en_vert:
                aristas_dir.append((i, funcion[i]))
        
        return {
            'camino_vertebra': camino_vertebra,
            'camino_orden': camino_orden,
            'camino_inv': camino_inv,
            'aristas_vert': aristas_vert,
            'aristas_dir': aristas_dir
        }
