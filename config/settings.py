import os
from dotenv import load_dotenv
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

# Cargar las variables de entorno
load_dotenv()

# Leer token de Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Nombre de la hoja de cálculo
SPREADSHEET_NAME = "Gastos_test_pareja"

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.getenv("GOOGLE_CREDS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Acceso a la hoja
sheet = client.open(SPREADSHEET_NAME).sheet1

# === VERIFICAR ENCABEZADOS ===
def verificar_encabezados():
    encabezados = sheet.row_values(1)
    esperados = ["Fecha", "Monto", "Categoría", "Descripción", "Usuario"]
    if encabezados != esperados:
        sheet.insert_row(esperados, 1)
        print("✅ Encabezados corregidos.")

verificar_encabezados()


USUARIOS_TELEGRAM = {
    "Daniela M.": 5426240124,  # Reemplazá con tu chat_id real
    "Guido Q.": 1385320932     # Reemplazá con el de Guido
}
