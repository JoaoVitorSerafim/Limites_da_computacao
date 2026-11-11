"""Caixeiro Viajante por força bruta.

Testa todas as rotas distintas, com a cidade 0 como partida e chegada,
e devolve a de menor custo.
"""

from src.permutacoes import permutacoes, permutacoes_sem_espelhos


def custo_rota(rota, matriz):
    """Soma as distâncias de uma rota (lista de cidades).

    A rota já deve incluir a volta ao início, por exemplo [0, 2, 1, 3, 0].
    """
    total = 0.0
    for i in range(len(rota) - 1):
        total += matriz[rota[i]][rota[i + 1]]
    return total


def _buscar_melhor(matriz, gerador_de_permutacoes):
    """Percorre as permutações geradas e guarda a melhor rota encontrada."""
    n = len(matriz)
    outras = list(range(1, n))  # cidades 1..n-1 (a 0 é fixa)

    melhor_rota = None
    melhor_custo = float("inf")
    rotas_testadas = 0

    for p in gerador_de_permutacoes(outras):
        rota = [0] + p + [0]
        custo = custo_rota(rota, matriz)
        rotas_testadas += 1
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_rota = rota

    return melhor_rota, melhor_custo, rotas_testadas


def forca_bruta(matriz):
    """Versão oficial: testa (n-1)!/2 rotas (sem espelhadas).

    Retorna (melhor_rota, melhor_custo, rotas_testadas).
    Requer n >= 3 cidades.
    """
    return _buscar_melhor(matriz, permutacoes_sem_espelhos)


def forca_bruta_todas(matriz):
    """Versão de verificação: testa as (n-1)! rotas, inclusive as espelhadas."""
    return _buscar_melhor(matriz, permutacoes)


if __name__ == "__main__":
    # Verificação: python -m src.forca_bruta
    import math
    from src.cidades import gerar_cidades, matriz_distancias

    # 1) Instância de 4 cidades, para conferir à mão
    cidades = gerar_cidades(4)
    matriz = matriz_distancias(cidades)
    rota, custo, testadas = forca_bruta(matriz)
    print("=== 4 cidades ===")
    print(f"Melhor rota: {rota}")
    print(f"Custo:       {custo:.2f}")
    print(f"Rotas testadas: {testadas}")

    print("\nTodas as rotas distintas (para conferir à mão):")
    for p in permutacoes_sem_espelhos([1, 2, 3]):
        r = [0] + p + [0]
        print(f"  {r}  custo = {custo_rota(r, matriz):.2f}")

    # 2) Contagem e ótimo: sem espelhos x todas
    print("\n=== Verificação: sem espelhos x todas ===")
    print(f"{'n':>3} {'testadas':>9} {'(n-1)!/2':>9} {'custo':>9} {'custo (todas)':>14} {'iguais?':>8}")
    for n in range(4, 10):
        m = matriz_distancias(gerar_cidades(n))
        _, c1, t1 = forca_bruta(m)
        _, c2, t2 = forca_bruta_todas(m)
        esperado = math.factorial(n - 1) // 2
        print(f"{n:>3} {t1:>9} {esperado:>9} {c1:>9.2f} {c2:>14.2f} {str(abs(c1 - c2) < 1e-9):>8}")