"""Gera os gráficos (PNG) a partir dos CSVs da pasta resultados/.

Nenhum valor medido é digitado aqui: tudo é lido dos arquivos.
Uso: python -m src.graficos
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")  # só salva imagens, não abre janela
import matplotlib.pyplot as plt

from src.crescimento import numero_de_rotas

PASTA = "resultados"

# Rodada A (combinada com o grupo) para os tempos da força bruta
ARQUIVOS_TEMPOS = [
    "tempos_forca_bruta.csv",
    "tempos_forca_bruta_9_a_10.csv",
    "tempos_forca_bruta_11_a_11.csv",
]

ARQUIVOS_COMPARACAO = [
    "comparacao_resumo_4_a_9.csv",
    "comparacao_resumo_10_a_11.csv",
]


def ler_csv(nome):
    """Lê um CSV da pasta resultados/ e devolve uma lista de dicionários."""
    caminho = os.path.join(PASTA, nome)
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


def grafico_crescimento():
    """Número de rotas (n-1)!/2 para 4 a 30 cidades, em escala logarítmica."""
    ns = list(range(4, 31))
    rotas = [numero_de_rotas(n) for n in ns]

    plt.figure(figsize=(8, 5))
    plt.semilogy(ns, rotas, marker="o")
    for n in (11, 20, 30):
        r = numero_de_rotas(n)
        plt.annotate(f"n={n}: {r:.1e}", (n, r),
                     textcoords="offset points", xytext=(-70, 8))
    plt.title("Crescimento do número de rotas: (n - 1)! / 2")
    plt.xlabel("Número de cidades (n)")
    plt.ylabel("Número de rotas (escala logarítmica)")
    plt.grid(True, which="both", alpha=0.3)
    caminho = os.path.join(PASTA, "grafico_crescimento_rotas.png")
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    return caminho


def grafico_tempo():
    """Tempo medido da força bruta (Rodada A), em escala logarítmica."""
    pontos = {}
    for nome in ARQUIVOS_TEMPOS:
        for linha in ler_csv(nome):
            pontos[int(linha["n"])] = float(linha["tempo_segundos"])
    ns = sorted(pontos)
    tempos = [pontos[n] for n in ns]

    plt.figure(figsize=(8, 5))
    plt.semilogy(ns, tempos, marker="o")
    for n, t in zip(ns, tempos):
        plt.annotate(f"{t:.4g} s", (n, t),
                     textcoords="offset points", xytext=(-10, 8), fontsize=8)
    plt.title("Tempo medido da força bruta (Rodada A)")
    plt.xlabel("Número de cidades (n)")
    plt.ylabel("Tempo em segundos (escala logarítmica)")
    plt.grid(True, which="both", alpha=0.3)
    caminho = os.path.join(PASTA, "grafico_tempo_forca_bruta.png")
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    return caminho


def grafico_qualidade():
    """Quanto o vizinho mais próximo fica pior que o ótimo (média e pior caso)."""
    ns, medias, maximos = [], [], []
    for nome in ARQUIVOS_COMPARACAO:
        for linha in ler_csv(nome):
            ns.append(int(linha["n"]))
            medias.append(float(linha["diferenca_media_pct"]))
            maximos.append(float(linha["diferenca_max_pct"]))

    plt.figure(figsize=(8, 5))
    plt.plot(ns, medias, marker="o", label="Diferença média")
    plt.plot(ns, maximos, marker="s", label="Pior caso (máxima)")
    plt.title("Vizinho mais próximo × ótimo (10 mapas por tamanho)")
    plt.xlabel("Número de cidades (n)")
    plt.ylabel("Quanto mais cara que a rota ótima (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    caminho = os.path.join(PASTA, "grafico_qualidade_vizinho.png")
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    return caminho


if __name__ == "__main__":
    for funcao in (grafico_crescimento, grafico_tempo, grafico_qualidade):
        print("Gerado:", funcao())