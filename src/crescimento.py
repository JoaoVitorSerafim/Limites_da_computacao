"""Cálculo de quantas rotas existem no Caixeiro Viajante: (n - 1)! / 2."""


def fatorial(k):
    """Calcula k! = k * (k-1) * ... * 2 * 1, com um laço simples."""
    resultado = 1
    for i in range(2, k + 1):
        resultado *= i
    return resultado


def numero_de_rotas(n):
    """Número de rotas distintas para n cidades: (n - 1)! / 2."""
    return fatorial(n - 1) // 2


def tabela_crescimento(valores_de_n):
    """Devolve uma lista de (n, rotas) para cada n da lista."""
    return [(n, numero_de_rotas(n)) for n in valores_de_n]


if __name__ == "__main__":
    # Verificação: python -m src.crescimento
    print(f"{'n':>3} {'rotas = (n-1)!/2':>45}")
    for n, rotas in tabela_crescimento([4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30]):
        print(f"{n:>3} {rotas:>45,}")