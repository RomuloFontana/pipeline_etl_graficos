import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import json 

#importa o arquivo .csv
try:
    dados = pd.read_csv("dados_vendas.csv", sep=";")
except:
    print("Arquivo não encontrado!")

#uma conferida rápida para ver o resultado a importação
dados.head()

df = DataFrame(dados)

#confere quantos valores ausentes há no dataframe
df.isna().sum()

#conta os valores mais repetidos e salva numa variável como se fosse uma moda
moda_quant = df["Quantidade"].value_counts().index[0]
moda_preco = df["Preco_Unitario"].value_counts().index[0]
moda_total = df["Total_Venda"].value_counts().index[0]

#preenche os dados ausente usando moda_...
df.fillna(value={"Preco_Unitario":moda_preco, "Total_Venda":moda_total, 
                "Quantidade":moda_quant}, inplace=True)
df.isna().sum()

#faz análise dos dados como faturamento, média de quantidade por produtos, produto mais vendido
#e a quantidade de produtos vendidos
faturamento = df["Total_Venda"].sum()
media_prod = df[["Produto", "Quantidade"]].groupby(["Produto"]).agg("mean").round(0)
prod_vendidos = df.groupby(["Produto"])["Quantidade"].sum()
prod_mais_vend = df.groupby(["Produto"])["Quantidade"].sum().index[0]

#monta o gráfico em barra dos produtos vendidos
plt.bar(prod_vendidos.index, prod_vendidos.values, color="skyblue")
plt.title("Quantidade Total Vendida por Produto")
plt.xlabel("Produtos")
plt.ylabel("Quantidade")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

#salva o gráfico
plt.savefig("gráfico_de_vendas.png")
# plt.show()

#modela os dados para o formato dicionário
df_limpo = {
    "Faturamento": faturamento,
    "Média dos Produtos": media_prod.to_dict(),
    "Produto mais vendido": prod_mais_vend,
    "Quantidade de Produtos Vendidos": prod_vendidos.to_dict()
}
#salva os dados em .json
with open("relatorio.json", "w", encoding="utf-8") as arquivo:
    json.dump(df_limpo, arquivo, indent=4, ensure_ascii=False)