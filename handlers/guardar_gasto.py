import logging
import asyncio
from telegram import Update
from telegram.ext import CallbackContext


from config import settings, categorias
from datetime import datetime
from config.categorias import CATEGORIAS_VALIDAS, CATEGORIAS_PALABRAS_CLAVE
from config.settings import USUARIOS_TELEGRAM



def guardar_gasto(usuario, texto, bot=None):
    try:
        partes = texto.strip().split(" ", 2)
        if len(partes) < 2:
            return "⚠️ Formato inválido. Usá: `monto categoría descripción opcional`."

        monto_raw = partes[0].replace(",", ".")
        monto = float(monto_raw)

        if monto <= 0 or monto > 10_000_000:
            return f"⚠️ El monto ${monto:,.2f} parece no ser válido. ¿Seguro que lo escribiste bien?"

        categoria_ingresada = partes[1].capitalize()
        descripcion = partes[2] if len(partes) > 2 else ""

        if categoria_ingresada in CATEGORIAS_VALIDAS:
            categoria = categoria_ingresada
        else:
            texto_para_analizar = f"{categoria_ingresada} {descripcion}".lower()
            categoria = None
            for cat, palabras in CATEGORIAS_PALABRAS_CLAVE.items():
                if any(palabra in texto_para_analizar for palabra in palabras):
                    categoria = cat
                    break

            if not categoria:
                return (
                    "❌ Categoría inválida y no se pudo detectar automáticamente.\n"
                    "Usá una de estas:\n" + ", ".join(sorted(CATEGORIAS_VALIDAS))
                )

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        settings.sheet.append_row([fecha, monto, categoria, descripcion, usuario])

        # 🔔 Notificar al otro usuario si el bot fue pasado
        if bot and usuario in USUARIOS_TELEGRAM: #el usuario existe
            otros = [u for u in USUARIOS_TELEGRAM if u != usuario] #Recorre todas las claves (nombres) del diccionario, y se queda con las que no son el nombre de quien mandó el gasto (usuario).
            if otros:
                otro = otros[0] #de la lista otros agarro Guido Q.
                chat_id = USUARIOS_TELEGRAM[otro] #
                texto_aviso = (
                    f"📢 {usuario} cargó un gasto:\n"
                    f"💰 ${monto:.2f} en *{categoria}*\n"
                    f"📝 {descripcion or 'Sin descripción'}"
                )
                asyncio.create_task(bot.send_message(chat_id=chat_id, text=texto_aviso, parse_mode="Markdown"))

        return f"✅ Gasto guardado. Categoría detectada: *{categoria}*"

    except ValueError:
        return "⚠️ El monto debe ser un número (usá punto o coma decimal)."
    except Exception as e:
        logging.error(f"Error al guardar gasto: {e}")
        return "⚠️ Ocurrió un error al guardar el gasto."