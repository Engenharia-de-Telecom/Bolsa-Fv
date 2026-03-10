import pandas as pd

# Nomeando as variáveis

file_production = ("/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal Inversor 1.xlsx")
file_irradiance = ("/home/tiago-morandi/Documentos/Bolsa/Irradiancias/Mensal/irradiacao_media_diaria_periodo_completo.xlsx")

# Lendo as planilhas
df_production = pd.read_excel(file_production)
df_irradiance = pd.read_excel(file_irradiance, sheet_name="mensal")

# Coluna desejada é: Produção(kWh), Tempo atualizado e Irradiacao [kwh].

coluna_producao = df_production["Produção(kWh)"]
coluna_tempo = df_production["Tempo atualizado"]
coluna_irradianca = df_irradiance["Irradiacao [kwh]"]
# coluna_pr = df_production["PR(%)"]

# Calculo do PR
P = 32
coluna_pr = (coluna_producao / (P * coluna_irradianca)) * 100



new_df = pd.DataFrame({
    "Tempo atualizado": coluna_tempo,
    "Produção(kWh)": coluna_producao,
    "Irradiação [kwh]": coluna_irradianca,
    "PR(%)": coluna_pr
})

new_df["PR(%)"] = new_df["PR(%)"].round(2)
new_df["Irradiação [kwh]"] = new_df["Irradiação [kwh]"].round(2)

# Filtrando dados

df_filtrado = new_df[(new_df["PR(%)"] > 50) & (new_df["PR(%)"] < 100)]


# Salvando em uma nova planilha.
# new_df.to_excel("PR Mensal-Inversor 3 teste.xlsx", index=False)
df_filtrado.to_excel("PR Mensal-Inversor 1 Filtrado.xlsx", index=False)
# new_df.to_excel("PR Mensal Inversor 1.xlsx", index=False)

print("Nova planilha criada com sucesso!")