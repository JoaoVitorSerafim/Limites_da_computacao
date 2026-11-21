"""Demonstração completa do projeto "Limites da Computação" (Caixeiro Viajante).

Uso (na raiz do projeto, com o ambiente (.venv) ativo):
    python -m src.demo                 demonstração completa, com pausas (Enter)
    python -m src.demo --sem-pausa     roda tudo direto, sem esperar
    python -m src.demo --ate 9         força bruta só até 9 cidades (mais rápido)

Todos os números aparecem calculados na hora. Nada é digitado à mão.
"""

import argparse

from src.cidades import gerar_cidades, matriz_distancias, verificar_matriz
from src.forca_bruta import forca_bruta, custo_rota
from src.permutacoes import permutacoes_sem_espelhos
from src.vizinho_proximo import vizinho_mais_proximo
from src.medicao import cronometrar
from src.crescimento import numero_de_rotas

SEMENTE = 42
SEGUNDOS_POR_ANO = 365.25 * 24 * 3600
IDADE_UNIVERSO_ANOS = 13.8e9


def titulo(texto):
    print("\n" + "=" * 72)
    print(texto)
    print("=" * 72)


def pausa(ativa):
    if ativa:
        input("\n[Enter para continuar] ")


def formatar_tempo(segundos):
    """Escreve o tempo na unidade mais legível."""
    if segundos < 1e-3:
        return f"{segundos * 1e6:.1f} microssegundos"
    if segundos < 60:
        return f"{segundos:.4f} segundos"
    if segundos < 3600:
        return f"{segundos / 60:.1f} minutos"
    if segundos < 86400:
        return f"{segundos / 3600:.1f} horas"
    if segundos < SEGUNDOS_POR_ANO:
        return f"{segundos / 86400:.1f} dias"
    return f"{segundos / SEGUNDOS_POR_ANO:.3e} anos"


# ---------------------------------------------------------------- 1
def parte_testes():
    titulo("1) TESTES AUTOMÁTICOS")
    from tests import test_basico
    testes = [(nome, f) for nome, f in sorted(vars(test_basico).items())
              if nome.startswith("teste_")]
    passaram = 0
    for nome, funcao in testes:
        try:
            funcao()
            print("  OK     ", nome)
            passaram += 1
        except AssertionError:
            print("  FALHOU ", nome)
    print(f"\n{passaram} de {len(testes)} testes passaram.")


# ---------------------------------------------------------------- 2
def parte_exemplo_4_cidades():
    titulo("2) EXEMPLO COM 4 CIDADES (dá para conferir à mão)")
    cidades = gerar_cidades(4, SEMENTE)
    matriz = matriz_distancias(cidades)

    print("Cidades (x, y):")
    for i, (x, y) in enumerate(cidades):
        print(f"  Cidade {i}: ({x:6.2f}, {y:6.2f})")

    print("\nMatriz de distâncias:")
    for linha in matriz:
        print("  " + " ".join(f"{d:7.2f}" for d in linha))
    diagonal_zero, simetrica = verificar_matriz(matriz)
    print(f"Diagonal zero? {diagonal_zero}   Simétrica? {simetrica}")

    print(f"\nRotas distintas, (4 - 1)! / 2 = {numero_de_rotas(4)}:")
    for p in permutacoes_sem_espelhos([1, 2, 3]):
        rota = [0] + p + [0]
        print(f"  {rota}  custo = {custo_rota(rota, matriz):.2f}")

    rota, custo, testadas = forca_bruta(matriz)
    print(f"\nFORÇA BRUTA: melhor rota {rota}, custo {custo:.2f} "
          f"({testadas} rotas testadas)")
    rota_v, custo_v = vizinho_mais_proximo(matriz)
    print(f"VIZINHO MAIS PRÓXIMO: rota {rota_v}, custo {custo_v:.2f}")


# ---------------------------------------------------------------- 3
def parte_forca_bruta(ate):
    titulo(f"3) FORÇA BRUTA: TEMPO DE 4 A {ate} CIDADES")
    print(f"{'n':>3} {'rotas testadas':>15} {'(n-1)!/2':>10} {'bate?':>6} "
          f"{'tempo (s)':>11} {'us/rota':>9} {'custo':>8}")
    resultados = {}
    for n in range(4, ate + 1):
        if n >= 10:
            print(f"    ... medindo n = {n}, aguarde ...", flush=True)
        matriz = matriz_distancias(gerar_cidades(n, SEMENTE))
        (rota, custo, testadas), tempo = cronometrar(forca_bruta, matriz)
        esperado = numero_de_rotas(n)
        print(f"{n:>3} {testadas:>15,} {esperado:>10,} {str(testadas == esperado):>6} "
              f"{tempo:>11.6f} {tempo / testadas * 1e6:>9.3f} {custo:>8.2f}")
        resultados[n] = {"matriz": matriz, "custo": custo, "tempo": tempo,
                         "testadas": testadas}
    return resultados


# ---------------------------------------------------------------- 4
def parte_comparacao(resultados):
    titulo("4) VIZINHO MAIS PRÓXIMO x FORÇA BRUTA (mesmas cidades)")
    print(f"{'n':>3} {'custo ótimo':>12} {'custo vizinho':>14} {'pior que ótimo':>15} "
          f"{'t força bruta':>14} {'t vizinho':>12} {'vezes mais rápido':>18}")
    for n, r in resultados.items():
        (rota, custo_v), t_v = cronometrar(vizinho_mais_proximo, r["matriz"])
        if custo_v < r["custo"] - 1e-9:
            print(f"ERRO: vizinho melhor que o ótimo em n = {n} (impossível)")
        dif = (custo_v - r["custo"]) / r["custo"] * 100
        vezes = r["tempo"] / t_v if t_v > 0 else float("inf")
        print(f"{n:>3} {r['custo']:>12.2f} {custo_v:>14.2f} {dif:>14.2f}% "
              f"{r['tempo']:>14.6f} {t_v:>12.8f} {vezes:>18,.0f}")

    # várias sementes (instâncias diferentes), para não concluir a partir de um caso só
    n = min(8, max(resultados))
    difs, acertos = [], 0
    for semente in range(1, 11):
        matriz = matriz_distancias(gerar_cidades(n, semente))
        _, otimo, _ = forca_bruta(matriz)
        _, custo_v = vizinho_mais_proximo(matriz)
        difs.append((custo_v - otimo) / otimo * 100)
        if abs(custo_v - otimo) < 1e-9:
            acertos += 1
    print(f"\nCom {n} cidades e 10 mapas diferentes (sementes 1 a 10): "
          f"o vizinho achou o ótimo em {acertos} de 10;")
    print(f"diferença média {sum(difs) / len(difs):.2f}%, pior caso {max(difs):.2f}%.")


# ---------------------------------------------------------------- 5
def parte_crescimento():
    titulo("5) QUANTAS ROTAS EXISTEM: (n - 1)! / 2")
    print(f"{'n':>3} {'rotas':>40}")
    for n in (4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30):
        print(f"{n:>3} {numero_de_rotas(n):>40,}")


# ---------------------------------------------------------------- 6
def parte_estimativa(resultados):
    titulo("6) ESTIMATIVA PARA 20 E 30 CIDADES (não é medição)")
    base = [n for n in resultados if n >= 8] or list(resultados)
    por_rota = {n: resultados[n]["tempo"] / resultados[n]["testadas"] for n in base}
    n_rapido = min(por_rota, key=por_rota.get)
    n_lento = max(por_rota, key=por_rota.get)
    print("Tempo por rota medido nesta execução:")
    for n in base:
        print(f"  n = {n}: {por_rota[n] * 1e6:.3f} microssegundos")
    print(f"\nCenário 1: {por_rota[n_rapido] * 1e6:.3f} us/rota (menor, n = {n_rapido})")
    print(f"Cenário 2: {por_rota[n_lento] * 1e6:.3f} us/rota (maior, n = {n_lento})")
    print("Estimativa = número de rotas x tempo por rota.")

    for n in (20, 30):
        rotas = numero_de_rotas(n)
        print(f"\n{n} cidades: {rotas:,} rotas")
        print(f"  cenário 1: {formatar_tempo(rotas * por_rota[n_rapido])}")
        print(f"  cenário 2: {formatar_tempo(rotas * por_rota[n_lento])}")
    anos = numero_de_rotas(30) * por_rota[n_lento] / SEGUNDOS_POR_ANO
    print(f"\n30 cidades (cenário 2) = {anos / IDADE_UNIVERSO_ANOS:.3e} vezes "
          f"a idade do universo (13,8 bilhões de anos).")
    print("Atenção: é estimativa; o custo por rota tende a subir com n.")


# ---------------------------------------------------------------- 7
def parte_desafio():
    titulo("7) DESAFIO EXTRA: VIZINHO MAIS PRÓXIMO COM 50 E 100 CIDADES")
    for n in (50, 100):
        custos, tempos = [], []
        for semente in range(1, 11):
            matriz = matriz_distancias(gerar_cidades(n, semente))
            (rota, custo), tempo = cronometrar(vizinho_mais_proximo, matriz)
            assert rota[0] == 0 and rota[-1] == 0          # começa e termina em 0
            assert sorted(rota[:-1]) == list(range(n))     # visita cada cidade 1 vez
            custos.append(custo)
            tempos.append(tempo)
        print(f"n = {n:>3}: custo médio {sum(custos) / 10:.2f} "
              f"(min {min(custos):.2f}, max {max(custos):.2f}); "
              f"tempo médio {sum(tempos) / 10:.6f} s; rotas válidas: sim")
    print("\nSem o ótimo nesses tamanhos, não dá para dizer o quão boa é a rota.")


# ---------------------------------------------------------------- fim
def resumo(resultados):
    titulo("RESUMO")
    n = max(resultados)
    r = resultados[n]
    _, custo_v = vizinho_mais_proximo(r["matriz"])
    _, t_v = cronometrar(vizinho_mais_proximo, r["matriz"])
    print(f"- Força bruta garante o ótimo, mas testa (n - 1)! / 2 rotas: "
          f"{r['testadas']:,} rotas com {n} cidades.")
    print(f"- Com {n} cidades: força bruta {r['tempo']:.4f} s; "
          f"vizinho mais próximo {t_v:.8f} s.")
    dif = (custo_v - r["custo"]) / r["custo"] * 100
    if dif < 1e-9:
        print("- Neste mapa o vizinho achou o ótimo, mas isso não é garantido "
              "(veja os 10 mapas da parte 4).")
    else:
        print(f"- O vizinho ficou {dif:.2f}% acima do ótimo neste mapa: "
              f"rápido, mas sem garantia.")
    print("- Cada cidade a mais multiplica o trabalho da força bruta: "
          "por isso ela não escala.")


def main():
    ap = argparse.ArgumentParser(description="Demonstração do projeto TSP.")
    ap.add_argument("--sem-pausa", action="store_true", help="não espera Enter")
    ap.add_argument("--ate", type=int, default=11,
                    help="maior n da força bruta (padrão 11; 4 a 11)")
    args = ap.parse_args()
    if args.ate < 4:
        ap.error("--ate precisa ser pelo menos 4")
    com_pausa = not args.sem_pausa

    print("LIMITES DA COMPUTAÇÃO: CAIXEIRO VIAJANTE")
    print("Força bruta x vizinho mais próximo")
    if args.ate >= 11:
        print("(com 11 cidades a força bruta leva alguns segundos)")
    pausa(com_pausa)

    parte_testes();                              pausa(com_pausa)
    parte_exemplo_4_cidades();                   pausa(com_pausa)
    resultados = parte_forca_bruta(args.ate);    pausa(com_pausa)
    parte_comparacao(resultados);                pausa(com_pausa)
    parte_crescimento();                         pausa(com_pausa)
    parte_estimativa(resultados);                pausa(com_pausa)
    parte_desafio();                             pausa(com_pausa)
    resumo(resultados)
    print("\nFim da demonstração.")


if __name__ == "__main__":
    main()