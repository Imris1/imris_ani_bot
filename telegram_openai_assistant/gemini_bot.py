import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# 1. NASTAVENÍ KLÍČŮ (vlož své klíče sem nebo do .env)
TELEGRAM_TOKEN = '8438893458:AAEFi-8amn5L99aDZ8KSO1SmNJ2mG-Nw5_A'
GEMINI_API_KEY = 'AIzaSyANRbIX15ah9TTPG-n8NRSN4orfh1ux75k'

# Konfigurace Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Rychlá a úsporná verze

# Slovník pro uchování historie konverzací pro každého uživatele
chat_sessions = {}

# Logování
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Příkaz /start"""
    await update.message.reply_text("Ahoj! Jsem tvůj Gemini asistent na Telegramu. Napiš mi cokoliv!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Zpracování běžných zpráv"""
    user_id = update.effective_user.id
    user_text = update.message.text

    # Pokud uživatel nemá aktivní chat, vytvoříme mu ho (udržuje kontext)
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])

    try:
        # Pošleme zprávu modelu a získáme odpověď
        response = chat_sessions[user_id].send_message(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Chyba při komunikaci s Gemini: {e}")
        await update.message.reply_text("Omlouvám se, ale došlo k chybě při generování odpovědi.")

if __name__ == '__main__':
    # Vytvoření aplikace Telegramu
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Registrace handlerů
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot běží... Stiskni Ctrl+C pro ukončení.")
    application.run_polling()
