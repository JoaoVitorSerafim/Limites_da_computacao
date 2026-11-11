"""Cronômetro para medir quanto tempo uma função leva para rodar."""

import time


def cronometrar(funcao, *argumentos):
    """Executa funcao(*argumentos) e mede o tempo gasto.

    Retorna (resultado_da_funcao, tempo_em_segundos).
    """
    inicio = time.perf_counter()
    resultado = funcao(*argumentos)
    fim = time.perf_counter()
    return resultado, fim - inicio