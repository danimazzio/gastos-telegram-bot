from datetime import date
import os
from dotenv import load_dotenv
from services.google_sheets_service import agregar_gasto

load_dotenv("config/config.env")

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def preparar_gasto(monto: float, categoria: str, fecha: date):
    return {
        "monto": monto,
        "categoria": categoria,
        "fecha": fecha.isoformat()
    }

def guardar_gasto(gasto: dict):
    """
    Guarda el gasto en Google Sheets.
    """
    if SHEET_ID is None:
        raise ValueError("No se encontró GOOGLE_SHEET_ID en config.env")

    agregar_gasto(SHEET_ID, gasto)