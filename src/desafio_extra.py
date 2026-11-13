"""Desafio extra: vizinho mais próximo com 50 e 100 cidades.

Não há comparação com o ótimo (a força bruta é inviável nesse tamanho).
Uso: python -m src.desafio_extra
"""

import csv
import os

from src.cidades import gerar_cidades, matriz_distancias
from src.vizinho_proximo import vizinho_mais_proximo
from src.medicao import cronometrar

PASTA_RESULTADOS = "resultados"
TAMANHOS = [50, 100]
SEMENTES = list(range(1, 11))


def rodar():
    print(f"{'n':>4} {'semente':>8} {'custo':>10} {'tempo (s)':>12}")
    linhas = []
    for n in TAMANHOS:
        for semente in SEMENTES:
            matriz = matriz_distancias(gerar_cidades(n, semente))
            (rota, custo), tempo = cronometrar(vizinho_mais_proximo, matriz)

            # Conferências: visita todas as cidades uma vez, começa e termina em 0
            assert rota[0] == 0 and rota[-1] == 0
            assert sorted(rota[:-1]) == list(range(n))

            print(f"{n:>4} {semente:>8} {custo:>10.2f} {tempo:>12.8f}")
            linhas.append([n, semente, custo, tempo])

    print("\nResumo por tamanho:")
    for n in TAMANHOS:
        custos = [l[2] for l in linhas if l[0] == n]
        tempos = [l[3] for l in linhas if l[0] == n]
        print(f"  n={n}: custo médio {sum(custos)/len(custos):.2f} "
              f"(min {min(custos):.2f}, max {max(custos):.2f}); "
              f"tempo médio {sum(tempos)/len(tempos):.8f} s")

    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    caminho = os.path.join(PASTA_RESULTADOS, "desafio_extra_50_100.csv")
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "semente", "custo", "tempo_s"])
        w.writerows(linhas)
    print(f"\nSalvo em: {caminho}")


if __name__ == "__main__":
    rodar()