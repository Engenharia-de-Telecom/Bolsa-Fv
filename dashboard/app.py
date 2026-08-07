from flask import Flask, jsonify, render_template, request
import json
import pandas as pd
import os

app = Flask(__name__)

# =====================================================
# Página principal do dashboard
# =====================================================



# =====================================================
# Página principal do dashboard
# =====================================================

@app.route("/")
def index():
    return render_template("index.html")


# =====================================================
# API que retorna o status dos sensores
# =====================================================

@app.route("/status")
def status():

    arquivo = "dados/status.json"

    if not os.path.exists(arquivo):
        return jsonify({
            "erro": "Arquivo status.json ainda não foi criado"
        })

    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return jsonify(dados)

# =====================================================
# Página dos gráficos
# =====================================================
@app.route("/graficos")
def graficos():
    return render_template("graficos.html")

# =====================================================
# Página dos gráficos
# =====================================================
@app.route("/api/dados")
def api_dados():

    coluna = request.args.get("coluna")
    inicio = request.args.get("inicio")
    fim = request.args.get("fim")

    df = pd.read_csv("dados/dados_estacao.csv")

    # Converte a coluna de datas
    df["DATE-TIME"] = pd.to_datetime(df["DATE-TIME"])

    # Verifica se a coluna existe
    if coluna not in df.columns:
        return jsonify({
            "erro": "Coluna inexistente."
        }), 400

    # Converte a coluna escolhida para número
    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )

    # Remove linhas inválidas
    df = df.dropna(subset=[coluna])

    # Aplica filtro somente se o usuário informou as duas datas
    if inicio and fim:

        inicio = pd.to_datetime(inicio)

        fim = pd.to_datetime(fim) + pd.Timedelta(days=1)

        df = df[
            (df["DATE-TIME"] >= inicio) &
            (df["DATE-TIME"] < fim)
        ]
        
    print("--------------------------------")

    print("Coluna:", coluna)
    print("Início:", inicio)
    print("Fim:", fim)

    print("Primeira data:")
    print(df["DATE-TIME"].min())

    print("Última data:")
    print(df["DATE-TIME"].max())

    print("Quantidade de linhas:")
    print(len(df))

    print("--------------------------------")

    return jsonify({

        "tempo": df["DATE-TIME"]
                    .dt.strftime("%d/%m/%Y %H:%M")
                    .tolist(),

        "valores": df[coluna].tolist()

    })

# =====================================================
# Inicialização do servidor
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
    )