import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from handlers.guardar_gasto import guardar_gasto 



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.from_user.first_name or ""
    last_name = update.message.from_user.last_name or ""
    apellido = f" {last_name[0]}." if last_name else ""
    usuario = f"{first_name}{apellido}"

    texto = update.message.text
    respuesta = guardar_gasto(usuario, texto, bot=context.bot)
    await update.message.reply_text(respuesta)


