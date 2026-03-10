import pandas as pd

# Arquivos a ser lidos
file_geral = "/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal.xlsx"
file_inversor1 = "/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal-Inversor 1.xlsx"
file_inversor2 = "/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal-Inversor 2.xlsx"
file_inversor3 = "/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal-Inversor 3.xlsx"
file_soma = "/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal Soma.xlsx"
file_irradiance = ("/home/tiago-morandi/Documentos/Bolsa/Irradiancias/Mensal/irradiacao_media_diaria_periodo_completo.xlsx")

# Lendo as planilhas

df_geral = pd.read_excel(file_geral)
df_inversor1 = pd.read_excel(file_inversor1)
df_inversor2 = pd.read_excel(file_inversor2)
df_inversor3 = pd.read_excel(file_inversor3)
df_soma = pd.read_excel(file_soma)
df_irradiance = pd.read_excel(file_irradiance, sheet_name="mensal")

# Escolhendo as colunas

cl_time = df_geral["Tempo atualizado"]
cl_production = df_geral["Produção(kWh)"]
cl_production1 = df_inversor1["Produção(kWh)"]
cl_production2 = df_inversor2["Produção(kWh)"]
cl_production3 = df_inversor3["Produção(kWh)"]
cl_production_soma = df_soma["Produção Total"]
cl_irradiance = df_irradiance["Irradiacao [kwh]"]
cl_pr_geral = df_geral["PR(%)"]
cl_pr_inversor1 = df_inversor1["PR(%)"]
cl_pr_inversor2 = df_inversor2["PR(%)"]
cl_pr_inversor3 = df_inversor3["PR(%)"]
cl_pr_soma = df_soma["PR(%)"]
cl_media = (cl_production1 + cl_production2 + cl_production3 ) / 3

# Criação da nova planilha
new_df = pd.DataFrame({
    "Tempo Atualizado": cl_time,
    "prod_planta[kWh]": cl_production,
    "prod_inv1[kWh]": cl_production1,
    "prod_inv2[kWh]": cl_production2,
    "prod_inv3[kWh]": cl_production3,
    "prod_soma[kWh]": cl_production_soma,
    "Irradiação [kwh]": cl_irradiance,
    "pr_planta[%]": cl_pr_geral,
    "pr_inv1[%]": cl_pr_inversor1,
    "pr_inv2[%]": cl_pr_inversor2,
    "pr_inv3[%]": cl_pr_inversor3,
    "pr_soma[%]": cl_pr_soma,
    "pr_media[%]": cl_media
})

# Impressão da nova planilha 
new_df.to_excel("planilha_unificada.xlsx", index=False)

# Filtro
# df_filtrado = new_df[(new_df["PR(%)"] > 50) & (new_df["PR(%)"] < 100)]

# Impressão da planilha filtrada
# df_filtrado.to_excel("PR Mensal Soma Filtrado.xlsx", index=False)

print("Nova planilha criada com sucesso!")