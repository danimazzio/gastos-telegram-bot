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
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from flask import Flask
import threading


# === CONFIGURACIÓN ===
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

SPREADSHEET_NAME = "Gastos_telegram"
CATEGORIAS_VALIDAS = {
    "Alquiler",
    "Expensas",
    "Supermercado",
    "Internet",
    "Luz",
    "Gas",
    "YouTube",
    "Almacén",
    "Salidas",
    "Varios",
    "Auto",
    "Limpieza",
    "Italia",
    "Vacaciones",
}

CATEGORIAS_PALABRAS_CLAVE = {
    "Alquiler": ["alquiler"],
    "Expensas": ["expensa", "expensas", "exp"],
    "Supermercado": ["super", "coto", "carrefour", "dia"],
    "Internet": ["internet", "fibertel", "telecentro", "wifi"],
    "Luz": ["luz", "edenor"],
    "Gas": ["gas", "metrogas"],
    "YouTube": ["youtube", "yt", "premium"],
    "Almacén": ["verdu", "almacen", "pan", "verdura", "fruta", "huevo", "carniceria", "carni","cerveza","birra","escabio","alcohol","chino"],
    "Salidas": ["salida", "bar", "cena", "restaurante", "salir", "kermo", "hambur", "hamburguesa","comida","delivery"],
    "Varios": ["varios", "extra", "mercado libre","otro", ],
    "Auto": ["auto", "nafta", "service", "garage", "taller", "patente", "lavado"],
    "Limpieza": ["limpieza"],
    "Italia": ["escribania","inmobiliaria","arquitecta","italia","casa"],
    "Vacaciones": ["vacaciones", "viaje", "hotel", "pasaje",],
}

USUARIOS_TELEGRAM = {
    "Daniela M.": 5426240124,  # Reemplazá con tu chat_id real
    "Guido Q.": 1385320932     # Reemplazá con el de Guido
}

# === LOGGING para ver errores en consola ===
logging.basicConfig(level=logging.INFO)

# === CONECTAR CON GOOGLE SHEETS ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
creds_dict = json.loads(os.getenv("GOOGLE_CREDS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# === VERIFICAR ENCABEZADOS ===
def verificar_encabezados():
    encabezados = sheet.row_values(1)
    esperados = ["Fecha", "Monto", "Categoría", "Descripción", "Usuario"]
    if encabezados != esperados:
        sheet.insert_row(esperados, 1)
        print("✅ Encabezados corregidos.")

verificar_encabezados()

# === FUNCIONES DEL BOT ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(
        #f"👋 ¡Hola! Tu chat_id es: {chat_id}\n"
        "Poné el gasto así:\n`2500 supermercado compra del día`\n"
        "y lo voy a guardar si la categoría es válida.\n\n"
        "📌 Categorías válidas:\n" + "\n".join(sorted(CATEGORIAS_VALIDAS))
    )

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
        sheet.append_row([fecha, monto, categoria, descripcion, usuario])

        # 🔔 Notificar al otro usuario si el bot fue pasado
        if bot and usuario in USUARIOS_TELEGRAM:
            otros = [u for u in USUARIOS_TELEGRAM if u != usuario]
            if otros:
                otro = otros[0]
                chat_id = USUARIOS_TELEGRAM[otro]
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.from_user.first_name or ""
    last_name = update.message.from_user.last_name or ""
    apellido = f" {last_name[0]}." if last_name else ""
    usuario = f"{first_name}{apellido}"

    texto = update.message.text
    respuesta = guardar_gasto(usuario, texto, bot=context.bot)
    await update.message.reply_text(respuesta)

async def resumen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        registros = sheet.get_all_records()
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
            porcentaje = 0.4 if "sofia" in usuario.lower() else 0.6
            deberia = total_general * porcentaje
            diferencia = total - deberia
            estado = "✅" if abs(diferencia) < 100 else ("⬆️" if diferencia > 0 else "⬇️")
            texto += f"{estado} <b>{usuario}</b>: gastó ${total:.2f} / debería: ${deberia:.2f} → diferencia: ${diferencia:.2f}\n"

        await update.message.reply_text(texto)
    except Exception as e:
        logging.error(f"Error en resumen: {e}")
        await update.message.reply_text("⚠️ Error al calcular el resumen.")
        
        
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

