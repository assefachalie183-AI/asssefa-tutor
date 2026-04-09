import logging
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# --- Config ---
TOKEN = '8516173625:AAH5SBhzFs2vSM-_JyoqMPQ6KTsi0Vn3ehs'
CHANNEL_USERNAME = '@Gondarmarketlink1221' # ያንተ ቻናል ዩዘርኔም
GEMINI_API_KEY = 'ያንተ_GEMINI_API_KEY_እዚህ_ይግባ' # ከላይ የወሰድከው ቁጥር

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            await update.message.reply_text(f"Welcome {update.effective_user.first_name}! 👋\nአሁን ማንኛውንም የትምህርት ጥያቄ እዚህ መጠየቅ ትችላለህ። AI መልስ ይሰጥሃል።")
        else:
            keyboard = [[InlineKeyboardButton("Join Channel 📢", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                        [InlineKeyboardButton("✅ I Joined", callback_data='check_sub')]]
            await update.message.reply_text("መጀመሪያ ቻናላችንን ይቀላቀሉ!", reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await update.message.reply_text("Error: Make sure the bot is Admin in your channel.")

# ተማሪዎች ጥያቄ ሲጠይቁ በ AI የሚመልስ ክፍል
async def handle_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    # መጀመሪያ ሰብስክራይብ ማድረጉን ቼክ እናደርጋለን
    member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    if member.status not in ['member', 'administrator', 'creator']:
        await update.message.reply_text("ጥያቄ ለመጠየቅ መጀመሪያ ቻናሉን ይቀላቀሉ!")
        return

    # ለተማሪው መልስ ማዘጋጀት
    waiting_msg = await update.message.reply_text("Thinking... 🤔")
    try:
        response = model.generate_content(user_text)
        await waiting_msg.edit_text(response.text)
    except:
        await waiting_msg.edit_text("ይቅርታ፣ አሁን ላይ መልስ መስጠት አልቻልኩም። በኋላ ይሞክሩ።")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    # ጽሁፍ ሲላክ ወደ AI የሚወስድ መስመር
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_chat))
    
    print("--- AI Bot is Running! ---")
    app.run_polling()

if __name__ == '__main__':
    main()