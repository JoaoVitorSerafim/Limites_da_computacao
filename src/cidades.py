"""Geração de cidades e da matriz de distâncias.

Todos os outros módulos (força bruta, vizinho mais próximo, medições)
usam as funções deste arquivo, para que os algoritmos sejam comparados
exatamente nas mesmas instâncias.
"""

import math
import random


def gerar_cidades(n, semente=42, limite=100.0):
    """Gera n cidades com coordenadas (x, y) aleatórias entre 0 e limite.

    Com a mesma semente, o resultado é sempre o mesmo (reprodutível).
    Retorna uma lista de tuplas: [(x0, y0), (x1, y1), ...].
    """
    gerador = random.Random(semente)
    cidades = []
    for _ in range(n):
        x = gerador.uniform(0, limite)
        y = gerador.uniform(0, limite)
        cidades.append((x, y))
    return cidades


def distancia(a, b):
    """Distância euclidiana entre dois pontos a e b, cada um no formato (x, y)."""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx * dx + dy * dy)


def matriz_distancias(cidades):
    """Constrói a matriz n x n onde matriz[i][j] é a distância entre as cidades i e j."""
    n = len(cidades)
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = distancia(cidades[i], cidades[j])
            matriz[i][j] = d
            matriz[j][i] = d
    return matriz


def verificar_matriz(matriz):
    """Confere as duas propriedades esperadas: diagonal zero e simetria."""
    n = len(matriz)
    diagonal_zero = all(matriz[i][i] == 0.0 for i in range(n))
    simetrica = all(matriz[i][j] == matriz[j][i] for i in range(n) for j in range(n))
    return diagonal_zero, simetrica


if __name__ == "__main__":
    # Demonstração rápida: python -m src.cidades
    cidades = gerar_cidades(5)
    print("Cidades (x, y):")
    for i, (x, y) in enumerate(cidades):
        print(f"  Cidade {i}: ({x:6.2f}, {y:6.2f})")

    matriz = matriz_distancias(cidades)
    print("\nMatriz de distâncias:")
    for linha in matriz:
        print("  " + " ".join(f"{d:7.2f}" for d in linha))

    diagonal_zero, simetrica = verificar_matriz(matriz)
    print(f"\nDiagonal zero? {diagonal_zero}")
    print(f"Simétrica?     {simetrica}")

    # As 5 primeiras cidades de uma instância maior devem ser as mesmas
    maior = gerar_cidades(11)
    print(f"Primeiras 5 de 11 iguais às de 5? {maior[:5] == cidades}")