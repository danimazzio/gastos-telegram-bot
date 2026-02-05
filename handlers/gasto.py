from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from services.gastos_service import preparar_gasto, guardar_gasto

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Necesitamos al menos monto y categoría
    if len(context.args) < 2:
        await update.message.reply_text(
            "Formato incorrecto.\nUsá: /gasto monto categoría [fecha opcional YYYY-MM-DD]"
        )
        return

    monto = context.args[0]

    # Validar que el monto sea un número
    try:
        monto = float(monto)
    except ValueError:
        await update.message.reply_text("El monto debe ser un número.")
        return

    # Si hay fecha, la tomamos. Si no, usamos hoy.
    if len(context.args) >= 3:
        fecha_str = context.args[-1]
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            categoria = " ".join(context.args[1:-1])
        except ValueError:
            # Si la fecha no es válida, asumimos que no era fecha
            fecha = datetime.today().date()
            categoria = " ".join(context.args[1:])
    else:
        fecha = datetime.today().date()
        categoria = " ".join(context.args[1:])

    # 👉 Aquí usamos el servicio
    gasto_data = preparar_gasto(monto, categoria, fecha)
    guardar_gasto(gasto_data)

    await update.message.reply_text(
        f"Gasto registrado:\n"
        f"Monto: {gasto_data['monto']}\n"
        f"Categoría: {gasto_data['categoria']}\n"
        f"Fecha: {gasto_data['fecha']}"
    )
