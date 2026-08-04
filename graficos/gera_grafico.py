import pandas as pd 
import matplotlib.pyplot as plt 

file = "/home/tiago/Área de trabalho/Bolsa/Bolsa-Fv/PRs.xlsx"

df = pd.read_excel(file)
df['Tempo Atualizado'] = pd.to_datetime(df['Tempo Atualizado'])

plt.figure(figsize=(20,15))
plt.plot(df['Tempo Atualizado'], df['PR(%)'])
plt.xlabel('Data (aa-mm)')
plt.ylabel('PR [%] mensal')
titulo = "PR mensal da planta"
plt.title(titulo)
plt.grid(True)
plt.show()