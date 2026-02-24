import os
import logging
import asyncio
import google.generativeai as genai
from telegram import Update, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

# --- Configuration (Professional way: Use Environment Variables) ---
# Jab aap host karenge (Render/Koyeb par), tab ye keys wahan 'Environment Variables' mein dalenge.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YAHAN_APNA_TOKEN_DALO")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YAHAN_APNA_GEMINI_KEY_DALO")

# Gemini Setup with System Instruction
genai.configure(api_key=GEMINI_API_KEY)
# System instruction se AI professional aur funny behave karega
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are a funny, savage Indian bot. Your job is to roast users' photos in Hinglish. Be witty, use trending Indian slang, but don't be extremely offensive or hateful. For Truth or Dare, give spicy and interesting Indian context tasks."
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "🔥 *Roast & Reveal Bot Me Aapka Swagat Hai!* 🔥\n\n"
        "Main is group ka sabse bada dushman hoon!\n\n"
        "✅ *Roast:* Kisi ki photo bhejo aur dekho main kya halat karta hoon.\n"
        "✅ *Truth/Dare:* `/td` likho aur game shuru karo.\n"
        "✅ *Help:* `/help` for more info."
    )
    await update.message.reply_text(welcome_msg, parse_mode=constants.ParseMode.MARKDOWN)

async def roast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Typing indicator dikhane ke liye (Professional feel)
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=constants.ChatAction.TYPING)
    
    if update.message.photo:
        try:
            photo_file = await update.message.photo[-1].get_file()
            photo_bytes = await photo_file.download_as_bytearray()
            
            prompt = "Roast this person's appearance and style in a funny, savage way using Hinglish."
            response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': bytes(photo_bytes)}])
            
            await update.message.reply_text(response.text)
        except Exception as e:
            logging.error(f"Error in roast: {e}")
            await update.message.reply_text("Bhai, mera dimaag thoda garam ho gaya hai (API Error). Thodi der baad try kar!")
    else:
        await update.message.reply_text("Roast karne ke liye photo toh bhej pagle! 🙄")

async def truth_dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # AI se har baar naya Truth/Dare mangwana (Professional & Dynamic)
    try:
        prompt = "Give one random and spicy 'Truth' or 'Dare' task for an Indian friend group. Response should be in 1-2 lines in Hinglish."
        response = model.generate_content(prompt)
        await update.message.reply_text(f"🎲 *Aapka Task:* \n\n{response.text}", parse_mode=constants.ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("Network issue hai, firse try karo!")

# --- Main Deployment Logic ---
if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("td", truth_dare))
    app.add_handler(MessageHandler(filters.PHOTO, roast_handler))
    
    print("Bot is live...")
    app.run_polling()
