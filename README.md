# Limites da Computação

Projeto acadêmico desenvolvido para a disciplina de **Fundamentos da Computação**, com o objetivo de estudar problemas computacionais e compreender como o crescimento da complexidade afeta a execução de algoritmos.

## Tema

**Problema do Caixeiro Viajante (Traveling Salesperson Problem — TSP)**, comparação entre os algoritmos de força bruta e vizinho mais próximo, Problema da Parada e classes P e NP.

## Objetivos

- Implementar uma solução de força bruta para o Problema do Caixeiro Viajante.
- Implementar a heurística do vizinho mais próximo.
- Comparar o tempo de execução e a qualidade das soluções.
- Observar o crescimento do número de possibilidades conforme aumenta a quantidade de cidades.
- Discutir os limites computacionais relacionados ao Problema da Parada e às classes P e NP.

## Tecnologias utilizadas

- Python
- Matplotlib

## Algoritmos implementados

### Força bruta

Testa todas as rotas possíveis, considerando uma cidade inicial fixa e eliminando rotas espelhadas, para encontrar a rota de menor custo.

Para uma matriz de distâncias simétrica, o número de rotas testadas é:

\[
\frac{(n-1)!}{2}
\]

### Vizinho mais próximo

Constrói uma rota começando pela cidade inicial e escolhendo, a cada etapa, a cidade não visitada mais próxima.

É uma heurística rápida, mas não garante encontrar a rota de menor custo.

## Experimentos realizados

1. **Crescimento das possibilidades:** cálculo do número de rotas para diferentes quantidades de cidades.
2. **Desempenho:** medição do tempo de execução da força bruta para instâncias de 4 a 11 cidades.
3. **Qualidade das soluções:** comparação entre a heurística do vizinho mais próximo e a solução ótima, utilizando 10 sementes por tamanho de instância.
4. **Desafio extra:** execução do vizinho mais próximo para instâncias de 50 e 100 cidades.

Os resultados estão disponíveis na pasta `resultados/`, incluindo arquivos CSV e gráficos PNG.

## Estrutura do projeto

```text
limites_computacao/
├── src/
│   ├── cidades.py
│   ├── permutacoes.py
│   ├── forca_bruta.py
│   ├── vizinho_proximo.py
│   ├── medicao.py
│   ├── comparacao.py
│   ├── comparacao_estatistica.py
│   ├── crescimento.py
│   ├── estimativa.py
│   ├── desafio_extra.py
│   ├── graficos.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_basico.py
├── resultados/
│   ├── arquivos CSV
│   └── gráficos PNG
├── docs/
│   └── pseudocodigo.md
├── .gitignore
└── README.md
```

## Como executar

É necessário ter Python instalado.

Na pasta principal do projeto, crie e ative um ambiente virtual e instale o Matplotlib:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install matplotlib
```

### Testes automáticos

```powershell
python -m tests.test_basico
```

### Medições da força bruta

Execute os três comandos para gerar os arquivos de medição utilizados nos gráficos:

```powershell
python -m src.main 4 8
python -m src.main 9 10
python -m src.main 11 11
```

### Comparações entre os algoritmos

```powershell
python -m src.comparacao
python -m src.comparacao_estatistica 4 9
python -m src.comparacao_estatistica 10 11
```

### Crescimento e estimativas

```powershell
python -m src.crescimento
python -m src.estimativa
```

### Desafio extra

```powershell
python -m src.desafio_extra
```

### Geração dos gráficos

```powershell
python -m src.graficos
```

Os resultados gerados são armazenados na pasta `resultados/`.

**Observação:** os gráficos dependem dos arquivos CSV de medição e comparação. Execute primeiro os experimentos correspondentes ou utilize os resultados já disponibilizados no repositório.

## Documentação

O arquivo `docs/pseudocodigo.md` apresenta o pseudocódigo dos principais algoritmos implementados, permitindo compreender a lógica antes de analisar o código-fonte.

## Integrantes

- João Vitor Genesio da Silva Serafim
- [Nome do integrante 2]
- [Nome do integrante 3]

## Disciplina

**Fundamentos da Computação**

## Considerações finais

O projeto permite observar, na prática, como diferentes estratégias de resolução influenciam o desempenho e a qualidade das soluções.

Enquanto a força bruta encontra a solução ótima, seu custo computacional cresce rapidamente. Já o vizinho mais próximo consegue produzir rotas em pouco tempo, mas pode apresentar resultados superiores ao custo da solução ótima.
