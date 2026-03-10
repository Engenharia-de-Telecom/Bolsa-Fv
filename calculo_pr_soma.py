import pandas as pd

# Nomeando as variáveis

file_inversor1 = ("/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal-Inversor 1.xlsx")
file_inversor2 = ("/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal-Inversor 2.xlsx")
file_inversor3 = ("/home/tiago-morandi/Documentos/Bolsa/Python/FV-GRAFICOS/PR Mensal-Inversor 3.xlsx")
file_irradiance = ("/home/tiago-morandi/Documentos/Bolsa/Irradiancias/Mensal/irradiacao_media_diaria_periodo_completo.xlsx")

# Lendo as planilhas
df_inversor1 = pd.read_excel(file_inversor1)
df_inversor2 = pd.read_excel(file_inversor2)
df_inversor3 = pd.read_excel(file_inversor3)
df_irradiance = pd.read_excel(file_irradiance, sheet_name="mensal")

# Escolhendo as colunas
cl_inversor1 = df_inversor1["Produção(kWh)"]
cl_inversor2 = df_inversor2["Produção(kWh)"]
cl_inversor3 = df_inversor3["Produção(kWh)"]
cl_irradiance = df_irradiance["Irradiacao [kwh]"]
cl_time = df_inversor1["Tempo atualizado"]
# Soma a produção de cada inversor e armazena na variável
cl_sum = (cl_inversor1 + cl_inversor2 + cl_inversor3)

# Conta do PR Mensal
P = 32 * 3 # Potência de cada inversor
cl_pr = (cl_sum / (P * cl_irradiance)) * 100


# Criação da nova planilha
new_df = pd.DataFrame({
    "Tempo Atualizado": cl_time,
    "Produção Total": cl_sum,
    "Irradiação Mensal[kWh]": cl_irradiance,
    "PR(%)": cl_pr
})

# Arredondar os valores para duas casas decimais
new_df["PR(%)"] = new_df["PR(%)"].round(2)
new_df["Irradiação Mensal[kWh]"] = new_df["Irradiação Mensal[kWh]"].round(2)

# Impressão da nova planilha 
#new_df.to_excel("PR Mensal Soma.xlsx", index=False)

# Filtro
df_filtrado = new_df[(new_df["PR(%)"] > 50) & (new_df["PR(%)"] < 100)]

# Impressão da planilha filtrada
df_filtrado.to_excel("PR Mensal Soma Filtrado.xlsx", index=False)

print("Nova planilha criada com sucesso!")