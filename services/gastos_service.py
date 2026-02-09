from datetime import date
import os
from dotenv import load_dotenv
from services.google_sheets_service import agregar_gasto
from config.categorias import CATEGORIES

load_dotenv("config/config.env")

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")


def preparar_gasto(monto: float, texto: str, fecha: date):
    categoria, subcategoria = clasificar_categoria_y_subcategoria(texto)
    medio = detectar_medio_de_pago(texto)

    return {
        "monto": monto,
        "categoria": categoria,
        "subcategoria": subcategoria,
        "descripcion": texto,
        "medio_de_pago": medio,
        "fecha": fecha.isoformat()
    }

def guardar_gasto(gasto: dict):
    """
    Guarda el gasto en Google Sheets.
    """
    if SHEET_ID is None:
        raise ValueError("No se encontró GOOGLE_SHEET_ID en config.env")
    
    fila = [
        gasto["fecha"],
        gasto["categoria"],
        gasto["monto"],
        gasto["subcategoria"],
        gasto["descripcion"],
        gasto["medio_de_pago"]
    ]

    # 👉 ESTA ES LA LÍNEA CORRECTA
    agregar_gasto(SHEET_ID, fila)

    
def clasificar_categoria_y_subcategoria(texto: str):
    texto = texto.lower()

    for categoria_macro, subcats in CATEGORIES.items():
        for subcategoria, keywords in subcats.items():
            if any(kw in texto for kw in keywords):
                return categoria_macro, subcategoria

    return "otros", "otros"


def detectar_medio_de_pago(texto: str) -> str:
    texto = texto.lower()

    if any(p in texto for p in ["tarjeta", "crédito", "credito", "visa", "master", "amex"]):
        return "tarjeta"
    if any(p in texto for p in ["debito", "débito"]):
        return "debito"
    if any(p in texto for p in [" mp", "mercado pago"]):
        return "Mercado pago"
    if any(p in texto for p in ["efvo", "efectivo"]):
        return "Efectivo"
    return "no_especificado"

