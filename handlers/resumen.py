import logging

from telegram import Update
from telegram.ext import ContextTypes
from config import settings
from datetime import datetime

async def resumen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        registros = settings.sheet.get_all_records()
        ahora = datetime.now()
        mes_actual = ahora.strftime("%Y-%m")

        totales = {}
        total_general = 0

        for fila in registros:
            fecha = fila.get("Fecha", "")
            usuario = fila.get("Usuario", "desconocido")
            try:
                monto = float(fila.get("Monto", 0))
            except ValueError:
                continue  # salta filas con errores

            if fecha.startswith(mes_actual):
                total_general += monto
                if usuario not in totales:
                    totales[usuario] = 0
                totales[usuario] += monto

        if total_general == 0:
            await update.message.reply_text("📭 No hay gastos registrados este mes.")
            return

        texto = f"📊 <b>Resumen de {ahora.strftime('%B %Y')}</b>\nTotal: ${total_general:.2f}\n\n"
        for usuario, total in totales.items():
            porcentaje = 0.4 if "daniela" in usuario.lower() else 0.6
            deberia = total_general * porcentaje
            diferencia = total - deberia
            estado = "✅" if abs(diferencia) < 100 else ("⬆️" if diferencia > 0 else "⬇️")
            texto += f"{estado} <b>{usuario}</b>: gastó ${total:.2f} / debería: ${deberia:.2f} → diferencia: ${diferencia:.2f}\n"

        await update.message.reply_text(texto)
    except Exception as e:
        logging.error(f"Error en resumen: {e}")
        await update.message.reply_text("⚠️ Error al calcular el resumen.")