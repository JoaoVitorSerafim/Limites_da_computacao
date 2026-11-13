
"""Estimativa do tempo da força bruta para muitas cidades.

ATENÇÃO: os resultados para n grande são ESTIMATIVAS (regra de três),
nunca medições. Tempos de referência (segundos) vindos de resultados/:
  n=8:  tempos_forca_bruta.csv           (11/11, 14:53)
  n=9, n=10: tempos_forca_bruta_9_a_10.csv  (11/11, 15:04)
  n=11: tempos_forca_bruta_11_a_11.csv   (11/11, 15:06)
Python 3.13.14.
"""

from src.crescimento import numero_de_rotas

# Tempos medidos (segundos) pela força bruta: {n: tempo}
MEDIDOS = {
    8: 0.006233,
    9: 0.083986,
    10: 0.875496,
    11: 5.960303
}

SEGUNDOS_POR_ANO = 365.25 * 24 * 3600
IDADE_UNIVERSO_ANOS = 13.8e9


def segundos_por_rota(n_referencia):
    """Tempo médio por rota, medido para n_referencia cidades."""
    return MEDIDOS[n_referencia] / numero_de_rotas(n_referencia)


def estimar_tempo(n, s_por_rota):
    """Tempo estimado (segundos) = nº de rotas x tempo por rota."""
    return numero_de_rotas(n) * s_por_rota


def formatar_tempo(segundos):
    """Escreve o tempo na unidade mais legível."""
    if segundos < 60:
        return f"{segundos:.3f} segundos"
    if segundos < 3600:
        return f"{segundos / 60:.1f} minutos"
    if segundos < 86400:
        return f"{segundos / 3600:.1f} horas"
    if segundos < SEGUNDOS_POR_ANO:
        return f"{segundos / 86400:.1f} dias"
    return f"{segundos / SEGUNDOS_POR_ANO:.3e} anos"


if __name__ == "__main__":
    # Dois cenários: menor e maior tempo por rota medido.
    rapido = segundos_por_rota(8)
    lento = segundos_por_rota(11)

    print(f"Tempo por rota (n=8):  {rapido * 1e6:.3f} us")
    print(f"Tempo por rota (n=11): {lento * 1e6:.3f} us")

    print("\n--- Teste da regra: estimado x medido (referência n=11) ---")
    print(f"{'n':>3} {'medido (s)':>12} {'estimado (s)':>13}")

    for n in (8, 9, 10, 11):
        print(
            f"{n:>3} {MEDIDOS[n]:>12.6f} "
            f"{estimar_tempo(n, lento):>13.6f}"
        )

    print("\n--- ESTIMATIVAS (não são medições) ---")

    for n in (12, 15, 20, 25, 30):
        t_min = estimar_tempo(n, rapido)
        t_max = estimar_tempo(n, lento)

        print(f"\nn = {n}: {numero_de_rotas(n):,} rotas")
        print(f"  com tempo por rota de n=8:  {formatar_tempo(t_min)}")
        print(f"  com tempo por rota de n=11: {formatar_tempo(t_max)}")

    anos_30 = estimar_tempo(30, lento) / SEGUNDOS_POR_ANO

    print(
        f"\nn = 30 (cenário n=11) equivale a "
        f"{anos_30 / IDADE_UNIVERSO_ANOS:.3e} vezes a idade do universo "
        f"(13,8 bilhões de anos)."
    )
