"""Comparação opcional das métricas do notebook usando pandas."""

import json
from pathlib import Path

import pandas as pd


ARQUIVO_CSV = Path("transacoes.csv")
ARQUIVO_JSON = Path("relatorio.json")


def carregar_dados_validos(caminho=ARQUIVO_CSV):
    dados = pd.read_csv(caminho, dtype=str, keep_default_na=False)
    dados["id_num"] = pd.to_numeric(dados["id"].str.strip(), errors="coerce")
    dados["valor_num"] = pd.to_numeric(dados["valor"].str.strip(), errors="coerce")
    dados["data_dt"] = pd.to_datetime(dados["data"].str.strip(), format="%Y-%m-%d", errors="coerce")
    dados["tipo_limpo"] = dados["tipo"].str.strip().str.lower()

    mascara_valida = (
        dados["id_num"].notna()
        & dados["id_num"].gt(0)
        & ~dados["id_num"].duplicated(keep="first")
        & dados["cliente_id"].str.strip().ne("")
        & dados["data_dt"].notna()
        & dados["tipo_limpo"].isin(["credito", "debito"])
        & dados["valor_num"].notna()
        & dados["valor_num"].gt(0)
    )

    validos = dados.loc[mascara_valida].copy()
    validos["mes"] = validos["data_dt"].dt.strftime("%Y-%m")
    return validos, len(dados) - len(validos)


def gerar_resumo_pandas(dados):
    resumo = dados.groupby("mes").agg(
        quantidade=("id_num", "size"),
        media_transacao=("valor_num", "mean"),
        maior_valor=("valor_num", "max"),
        menor_valor=("valor_num", "min"),
    )
    creditos = dados.loc[dados["tipo_limpo"].eq("credito")].groupby("mes")["valor_num"].sum()
    debitos = dados.loc[dados["tipo_limpo"].eq("debito")].groupby("mes")["valor_num"].sum()
    resumo["total_credito"] = creditos
    resumo["total_debito"] = debitos
    resumo[["total_credito", "total_debito"]] = resumo[["total_credito", "total_debito"]].fillna(0)
    resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]
    return resumo.round(2)


def comparar_com_solucao_nativa(resumo, caminho=ARQUIVO_JSON):
    relatorio = json.loads(caminho.read_text(encoding="utf-8"))
    for mes, linha in resumo.iterrows():
        esperado = relatorio["resumo_mensal"][mes]
        assert int(linha["quantidade"]) == esperado["quantidade"]
        for metrica in ("total_credito", "total_debito", "saldo", "media_transacao"):
            assert abs(float(linha[metrica]) - esperado[metrica]) < 0.01


if __name__ == "__main__":
    dados_validos, total_invalidas = carregar_dados_validos()
    resumo_pandas = gerar_resumo_pandas(dados_validos)
    comparar_com_solucao_nativa(resumo_pandas)
    print(resumo_pandas.to_string())
    print(f"\nRegistros válidos: {len(dados_validos)}")
    print(f"Registros inválidos: {total_invalidas}")
    print("Comparação aprovada: pandas e solução nativa produziram as mesmas métricas.")
