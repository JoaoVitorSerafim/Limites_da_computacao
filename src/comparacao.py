
"""Compara força bruta e vizinho mais próximo."""

from src.cidades import gerar_cidades, matriz_distancias
from src.forca_bruta import forca_bruta
from src.vizinho_proximo import vizinho_mais_proximo
from src.medicao import cronometrar


def comparar(n):
    cidades = gerar_cidades(n)
    matriz = matriz_distancias(cidades)

    (rota_bruta, custo_bruta, rotas_testadas), tempo_bruta = (
        cronometrar(forca_bruta, matriz)
    )

    (rota_vizinho, custo_vizinho), tempo_vizinho = (
        cronometrar(vizinho_mais_proximo, matriz)
    )

    diferenca = ((custo_vizinho - custo_bruta) / custo_bruta) * 100

    print(f"\n=== Comparação: {n} cidades ===")

    print("\nFORÇA BRUTA")
    print("Rota:", rota_bruta)
    print(f"Custo: {custo_bruta:.2f}")
    print(f"Tempo: {tempo_bruta:.6f} segundos")
    print("Rotas testadas:", rotas_testadas)

    print("\nVIZINHO MAIS PRÓXIMO")
    print("Rota:", rota_vizinho)
    print(f"Custo: {custo_vizinho:.2f}")
    print(f"Tempo: {tempo_vizinho:.6f} segundos")

    print("\nDIFERENÇA")
    print(f"Rota do vizinho mais próximo: {diferenca:.2f}% mais cara")


if __name__ == "__main__":
    for n in range(4, 12):
        comparar(n)
