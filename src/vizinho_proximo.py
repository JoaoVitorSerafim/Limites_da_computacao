
"""Implementação do algoritmo do vizinho mais próximo."""

def vizinho_mais_proximo(matriz, inicio=0):
    n = len(matriz)

    visitadas = {inicio}
    rota = [inicio]
    atual = inicio
    custo = 0.0

    while len(visitadas) < n:
        proxima = min(
            (cidade for cidade in range(n) if cidade not in visitadas),
            key=lambda cidade: matriz[atual][cidade]
        )

        custo += matriz[atual][proxima]
        rota.append(proxima)
        visitadas.add(proxima)
        atual = proxima

    custo += matriz[atual][inicio]
    rota.append(inicio)

    return rota, custo


if __name__ == "__main__":
    from src.cidades import gerar_cidades, matriz_distancias

    cidades = gerar_cidades(5)
    matriz = matriz_distancias(cidades)

    rota, custo = vizinho_mais_proximo(matriz)

    print("Vizinho mais próximo")
    print("Rota:", rota)
    print(f"Custo: {custo:.2f}")
