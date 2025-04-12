from telegram import Update
from telegram.ext import ContextTypes
from config.categorias import CATEGORIAS_VALIDAS

# === FUNCIONES DEL BOT ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "👋 ¡Hola! Poné el gasto así:\n'2500 supermercado compra del día'\n"
        "y lo voy a guardar si la categoría es válida.\n\n"
        "📌 Categorías válidas:\n" + "\n".join(sorted(CATEGORIAS_VALIDAS))
    )
    await update.message.reply_text(mensaje)   
    

