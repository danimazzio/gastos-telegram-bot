from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# Importar handlers desde la carpeta handlers
from handlers.start import start
from handlers.gasto import gasto


# Cargar variables desde config/config.env
load_dotenv("config/config.env")

# Leemos el token desde una variable de entorno
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def main():
    if TOKEN is None:
        raise ValueError("No se encontró la variable de entorno TELEGRAM_BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    # Registrar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gasto", gasto))

    print("Bot iniciado…")
    app.run_polling()

if __name__ == "__main__":
    main()