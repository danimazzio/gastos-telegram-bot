import gspread
from google.oauth2.service_account import Credentials

# Alcances necesarios para Sheets y Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet(sheet_id: str):
    """
    Devuelve un objeto worksheet listo para escribir.
    """
    creds = Credentials.from_service_account_file(
        "config/google-credentials.json",
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1  # primera hoja
    return worksheet

def agregar_gasto(sheet_id: str, gasto: dict):
    """
    Agrega una fila a la hoja con el gasto.
    gasto = { "fecha": "...", "categoria": "...", "monto": ... }
    """
    ws = get_sheet(sheet_id)
    ws.append_row([gasto["fecha"], gasto["categoria"], gasto["monto"]])