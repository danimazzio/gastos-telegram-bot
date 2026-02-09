import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
from dotenv import load_dotenv


# Importar handlers desde la carpeta handlers
from handlers.start import start
#from handlers.gasto import gasto
from handlers.gasto_texto import gasto_texto

# Cargar variables desde config/config.env
load_dotenv("config/config.env")

# Leemos el token desde una variable de entorno
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

#print("TOKEN QUE ESTÁ USANDO EL BOT:", TOKEN) -- para chequear token

# ---- Flask para mantener Render despierto ----
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot activo"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# ---- Fin bloque Flask ----

def main():
    if TOKEN is None:
        raise ValueError("No se encontró la variable de entorno TELEGRAM_BOT_TOKEN")

    # Ejecutar Flask en segundo plano
    threading.Thread(target=run_flask, daemon=True).start()

    # Bot Telegram
    app = ApplicationBuilder().token(TOKEN).build()
    

    # Registrar handlers
    app.add_handler(CommandHandler("start", start))
    #app.add_handler(CommandHandler("gasto", gasto))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gasto_texto))

    print("Bot iniciado…")
    app.run_polling()

if __name__ == "__main__":
    main()