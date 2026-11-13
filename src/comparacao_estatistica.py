"""Comparação entre a força bruta (ótimo) e o vizinho mais próximo.

Uso: python -m src.comparacao [n_inicial] [n_final]
"""

import csv
import os
import sys

from src.cidades import gerar_cidades, matriz_distancias
from src.forca_bruta import forca_bruta
from src.vizinho_proximo import vizinho_mais_proximo
from src.medicao import cronometrar

PASTA_RESULTADOS = "resultados"
SEMENTES = list(range(1, 11))  # sementes 1 a 10


def comparar(n_inicial, n_final):
    """Compara os dois algoritmos para cada n, usando várias sementes."""
    print(f"{'n':>3} {'dif. média %':>13} {'dif. máx %':>11} "
          f"{'acertou ótimo':>14} {'t força bruta (s)':>18} {'t vizinho (s)':>14}")

    detalhes = []   # uma linha por (n, semente)
    resumo = []     # uma linha por n

    for n in range(n_inicial, n_final + 1):
        diferencas = []
        tempos_fb = []
        tempos_vz = []
        acertos = 0

        for semente in SEMENTES:
            matriz = matriz_distancias(gerar_cidades(n, semente))

            (_, custo_otimo, _), t_fb = cronometrar(forca_bruta, matriz)
            (_, custo_viz), t_vz = cronometrar(vizinho_mais_proximo, matriz)

            diferenca = (custo_viz - custo_otimo) / custo_otimo * 100
            if abs(custo_viz - custo_otimo) < 1e-9:
                acertos += 1

            # Teste de sanidade: heurística nunca pode ganhar do ótimo
            if custo_viz < custo_otimo - 1e-9:
                raise ValueError(
        f"Vizinho melhor que o ótimo: n={n}, semente={semente}"
    )

            diferencas.append(diferenca)
            tempos_fb.append(t_fb)
            tempos_vz.append(t_vz)
            detalhes.append([n, semente, custo_otimo, custo_viz,
                             diferenca, t_fb, t_vz])

        media = sum(diferencas) / len(diferencas)
        maxima = max(diferencas)
        t_fb_medio = sum(tempos_fb) / len(tempos_fb)
        t_vz_medio = sum(tempos_vz) / len(tempos_vz)

        print(f"{n:>3} {media:>13.2f} {maxima:>11.2f} "
              f"{acertos:>10}/{len(SEMENTES)} {t_fb_medio:>18.6f} {t_vz_medio:>14.8f}")
        resumo.append([n, media, maxima, acertos, t_fb_medio, t_vz_medio])

    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    sufixo = f"{n_inicial}_a_{n_final}"

    with open(os.path.join(PASTA_RESULTADOS, f"comparacao_detalhes_{sufixo}.csv"),
              "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "semente", "custo_otimo", "custo_vizinho",
                    "diferenca_percentual", "tempo_forca_bruta_s", "tempo_vizinho_s"])
        w.writerows(detalhes)

    with open(os.path.join(PASTA_RESULTADOS, f"comparacao_resumo_{sufixo}.csv"),
              "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "diferenca_media_pct", "diferenca_max_pct",
                    "acertos_do_otimo", "tempo_medio_forca_bruta_s",
                    "tempo_medio_vizinho_s"])
        w.writerows(resumo)

    print(f"\nArquivos salvos em: {PASTA_RESULTADOS}/ (sufixo {sufixo})")


if __name__ == "__main__":
    n_inicial = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    n_final = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    comparar(n_inicial, n_final)