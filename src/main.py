"""Ponto de entrada: roda os experimentos e grava os resultados.

Uso: python -m src.main
"""

import csv
import math
import os

from src.cidades import gerar_cidades, matriz_distancias
from src.forca_bruta import forca_bruta
from src.medicao import cronometrar

PASTA_RESULTADOS = "resultados"


def medir_forca_bruta(n_inicial, n_final):
    """Mede o tempo da força bruta para cada número de cidades no intervalo.

    Para n pequeno (até 9), repete a medição 3 vezes e guarda o MENOR tempo,
    porque o computador faz outras coisas ao mesmo tempo e isso atrapalha
    um pouco. Para n maior, mede uma vez só, porque já demora bastante.
    """
    linhas = []
    print(f"{'n':>3} {'rotas':>9} {'esperado':>9} {'bate?':>6} "
          f"{'tempo (s)':>11} {'us/rota':>9} {'custo':>8}")

    for n in range(n_inicial, n_final + 1):
        matriz = matriz_distancias(gerar_cidades(n))
        repeticoes = 3 if n <= 9 else 1

        menor_tempo = None
        for _ in range(repeticoes):
            (rota, custo, testadas), segundos = cronometrar(forca_bruta, matriz)
            if menor_tempo is None or segundos < menor_tempo:
                menor_tempo = segundos

        esperado = math.factorial(n - 1) // 2
        micros_por_rota = menor_tempo / testadas * 1_000_000
        print(f"{n:>3} {testadas:>9} {esperado:>9} {str(testadas == esperado):>6} "
              f"{menor_tempo:>11.6f} {micros_por_rota:>9.3f} {custo:>8.2f}")
        linhas.append([n, testadas, esperado, menor_tempo, micros_por_rota, custo])

    # Grava o resultado num arquivo CSV (tabela) dentro de resultados/
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    caminho = os.path.join(PASTA_RESULTADOS,
                       f"tempos_forca_bruta_{n_inicial}_a_{n_final}.csv")
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["n", "rotas_testadas", "rotas_esperadas",
                           "tempo_segundos", "microssegundos_por_rota", "custo"])
        escritor.writerows(linhas)
    print(f"\nTabela salva em: {caminho}")


if __name__ == "__main__":
    import sys

    # Uso: python -m src.main [n_inicial] [n_final]
    # Sem números, mede de 4 a 8 cidades.
    n_inicial = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    n_final = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    medir_forca_bruta(n_inicial, n_final)