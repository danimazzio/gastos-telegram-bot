from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from services.gastos_service import preparar_gasto, guardar_gasto


async def gasto_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().strip()

    # Intentamos detectar monto
    palabras = texto.split()
    monto = None
    descripcion = []
    fecha = datetime.today().date()

    for p in palabras:
        # Detectar monto
        try:
            monto = float(p.replace(",", "."))
            continue
        except ValueError:
            pass

        # Detectar fecha YYYY-MM-DD
        try:
            fecha = datetime.strptime(p, "%Y-%m-%d").date()
            continue
        except ValueError:
            pass

        descripcion.append(p)

    if monto is None:
        await update.message.reply_text("No encontré un monto en tu mensaje.")
        return

    descripcion = " ".join(descripcion)

    gasto_data = preparar_gasto(monto, descripcion, fecha)  # 'categoria' pasa a ser 'texto'
    guardar_gasto(gasto_data)

    await update.message.reply_text(
    f"📝<b>Gasto registrado:</b>\n\n"
    f"💰Monto: <b>${gasto_data['monto']}</b>\n"
    f"🏷Categoría: {gasto_data['categoria']} / {gasto_data['subcategoria']}\n"
    f"💳Medio de pago: {gasto_data['medio_de_pago']}\n"
    f"📅Fecha: {gasto_data['fecha']}",
    parse_mode="HTML"
    )