from flask import Flask, jsonify, render_template, request
import json
import pandas as pd
import os

app = Flask(__name__)

# =====================================================
# Página principal do dashboard
# =====================================================

@app.route("/")
def index():
    return render_template("index.html")

# =====================================================
# Página dedicada
# =====================================================
@app.route("/vitrine")
def vitrine():
    return render_template("vitrine.html")

# =====================================================
# API da página dedicada
# =====================================================

@app.route("/api/vitrine")
def api_vitrine():

    df = pd.read_csv("dados/dados_estacao.csv")

    # -----------------------------------------
    # CONVERTE DATE-TIME
    # -----------------------------------------

    df["DATE-TIME"] = pd.to_datetime(
        df["DATE-TIME"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["DATE-TIME"]
    )


    # -----------------------------------------
    # CONVERTE IRRADIÂNCIA
    # -----------------------------------------

    df["IRRADIANCE"] = pd.to_numeric(
        df["IRRADIANCE"],
        errors="coerce"
    )

    df_validos = df.dropna(
        subset=["IRRADIANCE"]
    )


    if df_validos.empty:

        return jsonify({
            "erro": "Não existem dados de irradiância."
        }), 404


    # -----------------------------------------
    # ÚLTIMA LEITURA
    # -----------------------------------------

    ultimo = df_validos.iloc[-1]

    ultima_data = ultimo["DATE-TIME"]

    ultima_irradiancia = ultimo["IRRADIANCE"]


    # -----------------------------------------
    # DIA DA ÚLTIMA LEITURA
    # -----------------------------------------

    dia = ultima_data.normalize()

    proximo_dia = dia + pd.Timedelta(days=1)


    # -----------------------------------------
    # PEGA SOMENTE OS DADOS:
    #
    # - do mesmo dia da última leitura
    # - até a última leitura
    # -----------------------------------------

    df_hoje = df_validos[
        (df_validos["DATE-TIME"] >= dia) &
        (df_validos["DATE-TIME"] <= ultima_data)
    ].copy()


    # -----------------------------------------
    # AGRUPA POR HORA
    # -----------------------------------------

    df_hoje["HORA"] = (
        df_hoje["DATE-TIME"]
        .dt.floor("h")
    )


    df_horario = (
        df_hoje
        .groupby("HORA")["IRRADIANCE"]
        .mean()
        .reset_index()
    )


    # -----------------------------------------
    # RESPOSTA
    # -----------------------------------------

    return jsonify({

        "ultima_atualizacao":
            ultima_data.strftime(
                "%d/%m/%Y %H:%M:%S"
            ),

        "irradiancia_atual":
            float(ultima_irradiancia),

        "data_grafico":
            dia.strftime("%d/%m/%Y"),

        "grafico": {

            "tempo":
                df_horario["HORA"]
                .dt.strftime("%H:%M")
                .tolist(),

            "irradiancia":
                df_horario["IRRADIANCE"]
                .round(2)
                .tolist()

        }

    })

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
    intervalo = request.args.get("intervalo", "minuto")


    # ==========================================
    # LÊ O CSV
    # ==========================================

    df = pd.read_csv(
        "dados/dados_estacao.csv"
    )


    # ==========================================
    # CONVERTE DATA
    # ==========================================

    df["DATE-TIME"] = pd.to_datetime(
        df["DATE-TIME"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["DATE-TIME"]
    )


    # ==========================================
    # VERIFICA A COLUNA
    # ==========================================

    if coluna not in df.columns:

        return jsonify({
            "erro": "Coluna inexistente."
        }), 400


    # ==========================================
    # CONVERTE VALORES PARA NÚMERO
    # ==========================================

    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )

    df = df.dropna(
        subset=[coluna]
    )


    # ==========================================
    # FILTRO DE DATA
    # ==========================================

    if inicio:

        inicio = pd.to_datetime(
            inicio
        )

        df = df[
            df["DATE-TIME"] >= inicio
        ]


    if fim:

        fim = pd.to_datetime(
            fim
        )

        # inclui o dia inteiro
        fim = fim + pd.Timedelta(days=1)

        df = df[
            df["DATE-TIME"] < fim
        ]


    # ==========================================
    # ORDENA POR DATA
    # ==========================================

    df = df.sort_values(
        "DATE-TIME"
    )


    # ==========================================
    # AGRUPAMENTO
    # ==========================================

    if intervalo == "minuto":

        # Mantém os dados originais
        pass


    elif intervalo == "5min":

        df = (
            df.set_index("DATE-TIME")
            .resample("5min")[coluna]
            .mean()
            .dropna()
            .reset_index()
        )


    elif intervalo == "15min":

        df = (
            df.set_index("DATE-TIME")
            .resample("15min")[coluna]
            .mean()
            .dropna()
            .reset_index()
        )


    elif intervalo == "30min":

        df = (
            df.set_index("DATE-TIME")
            .resample("30min")[coluna]
            .mean()
            .dropna()
            .reset_index()
        )


    elif intervalo == "hora":

        df = (
            df.set_index("DATE-TIME")
            .resample("1h")[coluna]
            .mean()
            .dropna()
            .reset_index()
        )


    elif intervalo == "dia":

        df = (
            df.set_index("DATE-TIME")
            .resample("1D")[coluna]
            .mean()
            .dropna()
            .reset_index()
        )


    # ==========================================
    # FORMATO DA DATA NO GRÁFICO
    # ==========================================

    if intervalo == "dia":

        formato_data = "%d/%m/%Y"

    elif intervalo == "minuto":

        formato_data = "%d/%m %H:%M"

    else:

        formato_data = "%d/%m %H:%M"


    # ==========================================
    # RETORNA JSON
    # ==========================================

    return jsonify({

        "tempo":
            df["DATE-TIME"]
            .dt.strftime(formato_data)
            .tolist(),

        "valores":
            df[coluna]
            .round(2)
            .tolist()

    })
# =====================================================
# Inicialização do servidor
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
    )