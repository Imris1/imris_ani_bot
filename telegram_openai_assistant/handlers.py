import google.generativeai as genai
from telegram import Update
from telegram.ext import ContextTypes

# Nastavení Gemini (toto by mělo být v config.py)
genai.configure(api_key="TVUJ_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

# Paměť pro konverzace (jednoduchá verze)
chat_sessions = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Pokud uživatel ještě nemá chat session, vytvoříme ji
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])

    try:
        # Pošleme zprávu Gemini
        response = chat_sessions[user_id].send_message(user_text)
        
        # Odpovíme uživateli na Telegramu
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Chyba: {str(e)}")
