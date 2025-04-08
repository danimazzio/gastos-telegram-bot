📌 Nombre del proyecto
Gastos Telegram Bot
Un bot de Telegram que permite interactuar con una hoja de cálculo de Google Sheets para registrar y consultar gastos.

⚙️ Tecnologías usadas
Python 3.11
python-telegram-bot
gspread
oauth2client
Render (para desplegar el bot)
Git y GitHub (para control de versiones)

🚀 Cómo ejecutar el proyecto localmente
Clonar el repositorio:
  git clone https://github.com/tu-usuario/gastos-telegram-bot.git
cd gastos-telegram-bot

Crear y activar entorno virtual
  python -m venv .env
  .\.env\Scripts\activate   # En Windows

Instalar dependencias
  pip install -r requirements.txt

Crear archivo .env
En la raíz del proyecto, crear un archivo .env con las siguientes variables:
TELEGRAM_TOKEN=tu_token_de_botfather
GOOGLE_CREDS={"type": "...", "project_id": "...", ...}  # Todo el contenido del JSON en una sola linea

Ejecutar el bot
  python main.py

🌍 Despliegue en Render
  Subí tu código a un repositorio en GitHub.
  Ingresá a Render y creá un nuevo Web Service.
  Conectá tu GitHub.
  Seleccioná el repositorio del bot.
  En Build Command, poné:
    pip install -r requirements.txt
  En Start Command, poné:
    python main.py

En el apartado Environment, cargá estas variables:
  TELEGRAM_TOKEN: el token del bot de Telegram.
  GOOGLE_CREDS: todo el contenido del archivo .json como una sola línea.

✅ Funcionalidades
Comando /start: saluda al usuario.
Comando /agregar: registra un gasto en la hoja de cálculo.
Comando /consultar: devuelve los últimos gastos registrados.
(Podés ajustar esto según lo que ya tengas implementado.)  
