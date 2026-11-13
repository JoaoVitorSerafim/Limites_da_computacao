"""Testes automáticos de correção.

Uso (na raiz do projeto): python -m tests.test_basico
Se tudo estiver certo, aparece 'Todos os testes passaram.'
"""

import math

from src.cidades import gerar_cidades, matriz_distancias, verificar_matriz
from src.permutacoes import permutacoes, permutacoes_sem_espelhos
from src.forca_bruta import forca_bruta, forca_bruta_todas, custo_rota
from src.vizinho_proximo import vizinho_mais_proximo
from src.crescimento import fatorial, numero_de_rotas


def teste_matriz():
    m = matriz_distancias(gerar_cidades(6))
    diagonal_zero, simetrica = verificar_matriz(m)
    assert diagonal_zero and simetrica


def teste_cidades_reprodutiveis():
    assert gerar_cidades(5) == gerar_cidades(5)
    assert gerar_cidades(11)[:5] == gerar_cidades(5)


def teste_permutacoes_contagem():
    for k in range(2, 7):
        itens = list(range(1, k + 1))
        assert sum(1 for _ in permutacoes(itens)) == math.factorial(k)
        assert sum(1 for _ in permutacoes_sem_espelhos(itens)) == math.factorial(k) // 2


def teste_fatorial():
    for k in range(0, 12):
        assert fatorial(k) == math.factorial(k)


def teste_numero_de_rotas():
    assert numero_de_rotas(4) == 3
    assert numero_de_rotas(11) == 1814400


def teste_rotas_testadas_igual_formula():
    for n in range(4, 9):
        m = matriz_distancias(gerar_cidades(n))
        _, _, testadas = forca_bruta(m)
        assert testadas == numero_de_rotas(n)


def teste_otimo_preservado():
    for n in range(4, 9):
        for semente in (1, 2, 3):
            m = matriz_distancias(gerar_cidades(n, semente))
            _, c1, _ = forca_bruta(m)
            _, c2, _ = forca_bruta_todas(m)
            assert abs(c1 - c2) < 1e-9


def teste_instancia_conhecida():
    # Quadrado de lado 1: a melhor rota percorre o perímetro (custo 4).
    pontos = [(0, 0), (1, 0), (1, 1), (0, 1)]
    m = matriz_distancias(pontos)
    rota, custo, _ = forca_bruta(m)
    assert abs(custo - 4.0) < 1e-9
    assert abs(custo_rota(rota, m) - custo) < 1e-9


def teste_vizinho_valido_e_nunca_melhor_que_otimo():
    for n in range(4, 9):
        for semente in range(1, 6):
            m = matriz_distancias(gerar_cidades(n, semente))
            _, otimo, _ = forca_bruta(m)
            rota, custo = vizinho_mais_proximo(m)
            assert rota[0] == 0 and rota[-1] == 0
            assert sorted(rota[:-1]) == list(range(n))
            assert custo >= otimo - 1e-9


if __name__ == "__main__":
    testes = [v for k, v in sorted(globals().items()) if k.startswith("teste_")]
    for t in testes:
        t()
        print("OK  ", t.__name__)
    print("\nTodos os testes passaram.")