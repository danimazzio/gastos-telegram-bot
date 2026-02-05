import gspread
from google.oauth2.service_account import Credentials
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_credentials():
    """
    Devuelve credenciales desde:
    - GOOGLE_CREDENTIALS_JSON (Render)
    - config/google-credentials.json (local)
    """
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if creds_json:
        # Render: la credencial viene como string JSON
        info = json.loads(creds_json)
        return Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        # Local: usamos el archivo físico
        return Credentials.from_service_account_file(
            "config/google-credentials.json",
            scopes=SCOPES
        )

def get_sheet(sheet_id: str):
    creds = get_credentials()
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    return sheet.sheet1

def agregar_gasto(sheet_id: str, gasto: dict):
    ws = get_sheet(sheet_id)
    ws.append_row([gasto["fecha"], gasto["categoria"], gasto["monto"]])