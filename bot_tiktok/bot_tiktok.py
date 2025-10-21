from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = "8345052102:AAGW2f-GdW30pT3HKtj2LS62iaLP_azqW_k"

# Función para obtener el video desde TikTok
def get_tiktok_video(url):
    api_url = "https://www.tikwm.com/api/"
    response = requests.get(api_url, params={"url": url})
    data = response.json()
    if data.get("data") and data["data"].get("play"):
        return data["data"]["play"]
    return None

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola! Envíame un link de TikTok y te descargo el video."
    )

# Cuando alguien envía un mensaje con un link
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "tiktok.com" in text:
        await update.message.reply_text("Descargando video... ⏳")
        video_url = get_tiktok_video(text)
        if video_url:
            await update.message.reply_video(video_url)
        else:
            await update.message.reply_text("❌ No pude descargar el video, revisa el link.")
    else:
        await update.message.reply_text("Envíame un link válido de TikTok.")

# Configurar el bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Ejecutar el bot
app.run_polling()