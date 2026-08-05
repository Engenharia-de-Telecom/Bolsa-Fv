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

    arquivo = "status.json"

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
    df = pd.read_csv("dados_estacao.csv")

    print(df.columns)
    if coluna not in df.columns:
        return jsonify({
            "erro": "Coluna inexistente."
        }), 400
    
    resposta = {
        "tempo": df["DATE/TIME"].tolist(),
        "valores": df[coluna].tolist()
    }

    return jsonify(resposta)

# =====================================================
# Inicialização do servidor
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )