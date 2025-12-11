"""
Módulo de utilidades matemáticas.
Contiene funciones para operaciones matriciales, determinantes y aritmética modular.
"""

import math
import numpy as np


def egcd(a, b):
    """Algoritmo extendido de Euclides."""
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)


def modinv(a, m):
    """Calcula el inverso modular de a módulo m."""
    a = a % m
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    return x % m


def determinante_bareiss(mat):
    """
    Calcula el determinante usando el algoritmo de Bareiss.
    """
    n = len(mat)
    if n == 0:
        return 1
    
    A = [list(map(int, row)) for row in mat]
    prev = 1
    sign = 1
    
    for k in range(n - 1):
        if A[k][k] == 0:
            swap_row = None
            for r in range(k + 1, n):
                if A[r][k] != 0:
                    swap_row = r
                    break
            if swap_row is None:
                return 0
            A[k], A[swap_row] = A[swap_row], A[k]
            sign *= -1
        
        pivot = A[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * pivot - A[i][k] * A[k][j]) // prev
        prev = pivot
    
    return sign * A[n - 1][n - 1]


def det_mod(mat, MOD):
    """Calcula el determinante módulo MOD."""
    return determinante_bareiss(mat) % MOD


def minor_matrix(M, row, col):
    """Calcula la matriz menor eliminando una fila y columna."""
    n = len(M)
    return [[M[r][c] for c in range(n) if c != col] for r in range(n) if r != row]


def adjugate_matrix(M, MOD=30):
    """Calcula la matriz adjunta."""
    n = len(M)
    adj = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            minor = minor_matrix(M, i, j)
            det_minor = determinante_bareiss(minor)
            cofactor = ((-1) ** (i + j)) * det_minor
            adj[j][i] = cofactor % MOD
    
    return adj


def inverse_matrix_mod(M, MOD=30):
    """
    Calcula la matriz inversa módulo MOD.
    Retorna None si la matriz no es invertible.
    """
    n = len(M)
    if any(len(row) != n for row in M):
        raise ValueError("Matrix must be square")
    
    detM = determinante_bareiss(M)
    det_mod_val = detM % MOD
    g, x, y = egcd(det_mod_val, MOD)
    
    if g != 1:
        return None
    
    det_inv = x % MOD
    adj = adjugate_matrix(M, MOD)
    inv = [[(det_inv * adj[i][j]) % MOD for j in range(n)] for i in range(n)]
    
    return inv


def mat_mul_vec_nxn(M, vec, MOD=30):
    """Multiplica una matriz n×n por un vector."""
    n = len(vec)
    out = [0] * n
    
    for i in range(n):
        s = 0
        row = M[i]
        for j in range(n):
            s += row[j] * vec[j]
        out[i] = s % MOD
    
    return out


def is_invertible_mod(mat, mod):
    """Verifica si una matriz es invertible módulo mod."""
    det = int(round(np.linalg.det(mat)))
    return math.gcd(det, mod) == 1


def get_matrix_from_function(funcion, MOD=30, dim=9):
    """
    Genera una matriz invertible 9×9 a partir de una función.
    """
    clean = [(0 if v is None else int(v)) for v in funcion]
    func = [clean[i % len(clean)] for i in range(dim)]
    
    arr = []
    for i in range(dim):
        row = []
        for j in range(dim):
            row.append((func[i] * (j + 1) + (func[j] + 1)) % MOD)
        arr.append(row)
    
    mat = np.array(arr, dtype=int)
    
    if is_invertible_mod(mat, MOD):
        return mat
    
    I = np.eye(dim, dtype=int)
    
    for i in range(dim):
        v = 3 * (func[i] + 1) + 1
        v %= MOD
        
        if v % 2 == 0:
            v = (v + 1) % MOD
        if v % 3 == 0:
            v = (v + 1) % MOD
        if v % 5 == 0:
            v = (v + 1) % MOD
        
        while math.gcd(v, MOD) != 1:
            v = (v + 1) % MOD
        
        I[i][i] = v
    
    return I
