# Pseudocódigo

## 1. Distância e matriz de distâncias

```
função DISTANCIA(a, b):
    dx ← a.x − b.x
    dy ← a.y − b.y
    retornar raiz_quadrada(dx² + dy²)

função MATRIZ_DISTANCIAS(cidades):
    n ← quantidade de cidades
    para i de 0 até n−1:
        para j de i+1 até n−1:
            d ← DISTANCIA(cidades[i], cidades[j])
            matriz[i][j] ← d
            matriz[j][i] ← d
    retornar matriz        (diagonal = 0)
```

## 2. Permutações (recursivo)

```
função PERMUTACOES(itens):
    se tamanho(itens) ≤ 1:                 // caso base
        devolver itens
        retornar
    para i de 0 até tamanho(itens)−1:
        resto ← itens sem o elemento i
        para cada p em PERMUTACOES(resto):
            devolver [itens[i]] + p
```

## 3. Permutações sem espelhos

```
função PERMUTACOES_SEM_ESPELHOS(itens):
    para cada p em PERMUTACOES(itens):
        se p[primeiro] < p[último]:
            devolver p
```

## 4. Caixeiro Viajante por força bruta

```
função FORCA_BRUTA(matriz):
    n ← número de cidades
    melhor_custo ← infinito
    melhor_rota ← vazio
    rotas_testadas ← 0

    para cada p em PERMUTACOES_SEM_ESPELHOS([1, 2, ..., n−1]):
        rota ← [0] + p + [0]
        custo ← 0
        para i de 0 até tamanho(rota)−2:
            custo ← custo + matriz[rota[i]][rota[i+1]]
        rotas_testadas ← rotas_testadas + 1
        se custo < melhor_custo:
            melhor_custo ← custo
            melhor_rota ← rota

    retornar melhor_rota, melhor_custo, rotas_testadas
```

Número de rotas testadas: (n − 1)! / 2.

## 5. Vizinho mais próximo

```
função VIZINHO_MAIS_PROXIMO(matriz):
    n ← número de cidades
    atual ← 0
    rota ← [0]
    visitadas ← {0}
    custo ← 0

    enquanto tamanho(visitadas) < n:
        proxima ← cidade não visitada com menor matriz[atual][cidade]
        custo ← custo + matriz[atual][proxima]
        rota ← rota + [proxima]
        visitadas ← visitadas + {proxima}
        atual ← proxima

    custo ← custo + matriz[atual][0]       // volta ao início
    rota ← rota + [0]
    retornar rota, custo
```

## 6. Número de rotas e estimativa de tempo

```
função NUMERO_DE_ROTAS(n):
    retornar FATORIAL(n − 1) / 2

função ESTIMAR_TEMPO(n, segundos_por_rota):
    retornar NUMERO_DE_ROTAS(n) × segundos_por_rota
```

`segundos_por_rota` = tempo medido ÷ rotas testadas, para um n medido.