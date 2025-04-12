import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    Defaults,
)

from config.settings import TOKEN, SPREADSHEET_NAME
from config.categorias import CATEGORIAS_VALIDAS, CATEGORIAS_PALABRAS_CLAVE
from handlers.start import start
from handlers.resumen import resumen
from handlers.handle_message import handle_message

# == CONEXION CON SHEETS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from flask import Flask
import threading

# === LOGGING para ver errores en consola ===
logging.basicConfig(level=logging.INFO)


#verificar_encabezados()

        
# ---- Flask para mantener Render despierto ----
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot activo"  # Render necesita esto para no dormirse

def run_flask():
    app_flask.run(host='0.0.0.0', port=10000)

# Ejecutar Flask en segundo plano
threading.Thread(target=run_flask).start()
# ---- Fin del bloque Flask ----

# === CONFIGURACIÓN DEL BOT ===

defaults = Defaults(parse_mode="HTML")
app = ApplicationBuilder().token(TOKEN).defaults(defaults).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("resumen", resumen))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask en segundo plano
threading.Thread(target=run_flask).start()

app.run_polling()

