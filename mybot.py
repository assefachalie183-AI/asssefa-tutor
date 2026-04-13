import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import google.generativeai as genai

# ሎግ ፋይል ለማየት (Debugging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ሚስጥራዊ ቁልፎችን ከ Render Environment Variables መቀበል
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini AI ማዋቀር
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = f"ሰላም {user_name}! 👋\nእኔ Assefa's ቴክ AI ቦት ነኝ። እንዴት ልረዳህ እችላለሁ?"
    
    keyboard = [[InlineKeyboardButton("ስለ እኔ እወቅ", callback_data='about')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    waiting_msg = await update.message.reply_text("በማሰብ ላይ ነኝ... 🤔")
    
    try:
        # Gemini AI መልስ እንዲያመጣ ማድረግ
        response = model.generate_content(user_text)
        await waiting_msg.edit_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await waiting_msg.edit_text("ይቅርታ አሁን ላይ መልስ መስጠት አልቻልኩም። በኋላ ይሞክሩ።")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'about':
        await query.message.reply_text("እኔ ለጎንደር ዩኒቨርሲቲ ተማሪዎች ፈተና እንዲያጠኑ የተሰራሁ AI ቦት ነኝ።")

def main():
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN አልተገኘም!")
        return

    # ቦቱን መገንባት
    app = Application.builder().token(TOKEN).build()

    # ትዕዛዞችን ማገናኘት
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_chat))

    print("--- AI Bot is Running on Server! ---")
    app.run_polling()

if __name__ == '__main__':
    main()
