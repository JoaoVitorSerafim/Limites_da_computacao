"""Geração de permutações feita à mão (sem itertools).

Usada pela força bruta para enumerar todas as ordens possíveis de visita.
"""


def permutacoes(itens):
    """Gera (uma de cada vez) todas as permutações da lista 'itens'.

    Ideia recursiva: escolha cada elemento para ser o primeiro e
    permute o resto.
      - Caso base: com 0 ou 1 elemento, só existe uma permutação.
      - Passo: para cada posição i, fixe itens[i] na frente e combine
        com cada permutação dos elementos restantes.
    Usa 'yield' (gerador): não guarda todas as permutações na memória.
    """
    if len(itens) <= 1:
        yield list(itens)
        return
    for i in range(len(itens)):
        resto = itens[:i] + itens[i + 1:]
        for p in permutacoes(resto):
            yield [itens[i]] + p


def permutacoes_sem_espelhos(itens):
    """Gera as permutações mantendo só uma de cada par (rota, rota inversa).

    Critério: fica a permutação cujo primeiro elemento é menor que o último.
    Vale para listas com 2 ou mais elementos de valores distintos.
    """
    for p in permutacoes(itens):
        if p[0] < p[-1]:
            yield p


if __name__ == "__main__":
    # Demonstração e verificação: python -m src.permutacoes
    print("Permutações de [1, 2, 3]:")
    for p in permutacoes([1, 2, 3]):
        print("  ", p)

    print("\nSem espelhos (p[0] < p[-1]):")
    for p in permutacoes_sem_espelhos([1, 2, 3]):
        print("  ", p)

    print("\nContagens (k = nº de itens permutados = n - 1):")
    print(f"{'k':>3} {'todas':>8} {'k!':>8} {'sem espelhos':>14} {'k!/2':>8}")
    fatorial = 1
    for k in range(2, 8):
        fatorial *= k
        itens = list(range(1, k + 1))
        todas = sum(1 for _ in permutacoes(itens))
        sem = sum(1 for _ in permutacoes_sem_espelhos(itens))
        print(f"{k:>3} {todas:>8} {fatorial:>8} {sem:>14} {fatorial // 2:>8}")

    # Sem duplicatas e sem par (rota, inversa) ao mesmo tempo
    mantidas = [tuple(p) for p in permutacoes_sem_espelhos([1, 2, 3, 4, 5])]
    sem_duplicatas = len(mantidas) == len(set(mantidas))
    sem_inversas = all(tuple(reversed(p)) not in set(mantidas) for p in mantidas)
    print(f"\nSem duplicatas?              {sem_duplicatas}")
    print(f"Nenhuma inversa presente?    {sem_inversas}")