import serial
import pandas as pd
import csv
import os
import time
import json
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

# =====================================================
# CONFIGURAÇÕES
# =====================================================

PORTA = "/dev/ttyUSB0"
# PORTA = "COM3"          # Windows

BAUDRATE = 4800

ARQUIVO_CSV = "dados_estacao.csv"
ARQUIVO_CREDENCIAIS = "credenciais.json"

SPREADSHEET_ID = "1nptoDAldIEQ8XesIDjvN_d0gLwEwucx3J5UhGhK4QBo"
NOME_ABA = "Página1"

COLUNAS = [
    "DATE/TIME",
    "IRRADIANCE",
    "PA",
    "RH",
    "TA",
    "RAIN_INT",
    "RAIN_DUR",
    "RAIN_AMOUNT",
    "WD_DIR",
    "WD_SPD"
]

# =====================================================
# GOOGLE SHEETS
# =====================================================

print("Conectando ao Google Sheets...")

scope = [
    "https://www.googleapis.com/auth/spreadsheets"
]

cred = Credentials.from_service_account_file(
    ARQUIVO_CREDENCIAIS,
    scopes=scope
)

gc = gspread.authorize(cred)

planilha = gc.open_by_key(SPREADSHEET_ID)
worksheet = planilha.worksheet(NOME_ABA)

print("Google Sheets conectado.")

# =====================================================
# SERIAL
# =====================================================

ser = serial.Serial(
    port=PORTA,
    baudrate=BAUDRATE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2
)

print(f"Conectado na porta {PORTA}")

# =====================================================
# CSV
# =====================================================

arquivo_existe = os.path.exists(ARQUIVO_CSV)

arquivo = open(
    ARQUIVO_CSV,
    "a",
    newline="",
    encoding="utf-8"
)

writer = csv.DictWriter(
    arquivo,
    fieldnames=COLUNAS
)

if not arquivo_existe:
    writer.writeheader()

print("Aguardando dados...\n")

# =====================================================
# LOOP PRINCIPAL
# =====================================================

while True:

    try:

        linha = ser.readline().decode(
            "ascii",
            errors="ignore"
        ).strip()

        if not linha:
            continue

        print("\nRecebido:")
        print(linha)

        # -------------------------------------------------
        # Converte a linha recebida em um dicionário
        # -------------------------------------------------

        dados = {}

        for campo in linha.split(";"):

            if ":" not in campo:
                continue

            chave, valor = campo.split(":", 1)

            dados[chave.strip()] = valor.strip()

        # -------------------------------------------------
        # GERA O STATUS DOS SENSORES
        # -------------------------------------------------

        estado = {
            "ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "sensores": {}
        }

        for coluna in COLUNAS:

            valor = dados.get(coluna, "")

            # Detecta erro (qualquer quantidade de "/")
            if valor and set(valor) == {"/"}:
                status = "offline"
            else:
                status = "online"

            estado["sensores"][coluna] = {
                "valor": valor,
                "status": status
            }

        # Salva o status atual
        with open("status.json", "w", encoding="utf-8") as arquivo_json:
            json.dump(
                estado,
                arquivo_json,
                indent=4,
                ensure_ascii=False
            )

        print("Status atualizado.")

        # -------------------------------------------------
        # SALVA NO CSV
        # -------------------------------------------------

        writer.writerow({
            coluna: dados.get(coluna, "")
            for coluna in COLUNAS
        })

        arquivo.flush()

        print("CSV atualizado.")

        # -------------------------------------------------
        # ENVIA PARA GOOGLE SHEETS
        # -------------------------------------------------

        try:

            worksheet.append_row(
                [dados.get(coluna, "") for coluna in COLUNAS],
                value_input_option="USER_ENTERED"
            )

            print("Google Sheets atualizado.")

        except Exception as erro:

            print("Erro ao enviar ao Google Sheets:")
            print(erro)

        time.sleep(0.01)

    except KeyboardInterrupt:

        print("\nPrograma encerrado.")
        break

    except Exception as erro:

        print("\nErro:")
        print(erro)

arquivo.close()
ser.close()