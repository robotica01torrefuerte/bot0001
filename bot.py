from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from fpdf import FPDF

# Diccionario para guardar palabras por usuario
user_words = {}

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Primero envíame una lista de palabras a ocultar (separadas por comas).")

# Recibir mensajes de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text.strip()

    # Si es la primera parte (palabras a ocultar)
    if user_id not in user_words:
        palabras = [p.strip().lower() for p in message.split(",")]
        user_words[user_id] = palabras
        await update.message.reply_text("Gracias. Ahora envíame el texto.")
        return

    # Segunda parte: ya hay palabras, ahora se espera el texto
    palabras = user_words.pop(user_id)  # Borrar la lista luego de usarla
    texto = message

    for palabra in palabras:
        texto = texto.replace(palabra, "______")

    # Crear el PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in texto.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output("salida.pdf")

    # Enviar PDF
    with open("salida.pdf", "rb") as f:
        await update.message.reply_document(f)

    await update.message.reply_text("Aquí tienes tu PDF con las palabras ocultas.")

# Main
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
