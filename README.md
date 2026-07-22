# ClearBank — Análise Financeira com Python

Projeto desenvolvido para o desafio prático de Análise de Dados e Inteligência de Negócios com IA. O notebook processa um CSV de transações bancárias, descarta registros inválidos, calcula métricas mensais, identifica movimentações suspeitas e exporta o relatório em JSON.

## O que o projeto entrega

- leitura com `csv.DictReader`, sem `pandas` na solução principal;
- validação independente de cada registro, sem interromper o processamento;
- agrupamento por mês, totais de crédito e débito, saldo, média, maior e menor transação;
- período analisado e quantidade de dias entre a primeira e a última transação;
- identificação de transações acima de R$ 10.000,00;
- relatório formatado no terminal;
- geração de `relatorio.json`;
- gráfico de saldo mensal em `grafico.png`;
- comparação opcional das métricas com `pandas`.

## Estrutura

```text
clearbank-analise/
├── desafio-final.ipynb   # notebook principal, executado e com saídas salvas
├── transacoes.csv        # 16 registros válidos e 7 inválidos
├── relatorio.json        # relatório gerado pelo notebook
├── grafico.png           # visualização opcional gerada com matplotlib
├── analise_pandas.py     # comparação opcional com pandas
└── README.md
```

## Como executar no Google Colab

1. Abra `desafio-final.ipynb` no Google Colab.
2. Envie `transacoes.csv` para o diretório da sessão.
3. Execute todas as células em ordem com **Runtime → Run all**.
4. Confira as saídas e baixe `relatorio.json` e `grafico.png`, se necessário.

## Como executar localmente

Requisitos: Python 3.10 ou superior, Jupyter Notebook e `matplotlib`.

```bash
pip install jupyter matplotlib pandas
jupyter notebook desafio-final.ipynb
```

No Jupyter, execute **Kernel → Restart & Run All**. Para validar a implementação opcional com `pandas`, depois de executar o notebook:

```bash
python analise_pandas.py
```

## Resultado validado

| Métrica | Resultado |
|---|---:|
| Linhas lidas | 23 |
| Transações válidas | 16 |
| Transações inválidas | 7 |
| Meses analisados | 4 |
| Transações suspeitas | 2 |
| Período | 05/01/2026 a 25/04/2026 |

O notebook foi executado integralmente e salvo com todas as saídas relevantes visíveis.
