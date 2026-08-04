from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)


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
# Inicialização do servidor
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )