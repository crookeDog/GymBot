import os
import json
import firebase_admin
from firebase_admin import credentials

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    CallbackContext,
    filters
)

from Firebase import (
    get_scheda,
    modifica_scheda_gym,
    aumenta_settimana_gym,
    resetta_settimana_gym,
    visualizza_settimana_gym
)

# 🔐 Firebase config da variabile d'ambiente
firebase_cred_json = os.getenv("FIREBASE_CRED")

if firebase_cred_json:
    cred_dict = json.loads(firebase_cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
else:
    print("Firebase credentials not found in environment.")

TOKEN = os.getenv("TOKEN")

change_scheda = False
giorno = ""

# === HANDLER ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.first_name.lower()
    keyboard = [
        [
            InlineKeyboardButton("View workout", callback_data="visualizza"),
            InlineKeyboardButton("Edit workout", callback_data="modifica"),
            InlineKeyboardButton("View week", callback_data="settimana"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Hi {username}, what would you like to do?",
        reply_markup=reply_markup
    )

async def visualizza_settimana(update: Update, context: CallbackContext):
    username = update.effective_user.first_name.lower()
    query = update.callback_query
    await query.answer()
    week = visualizza_settimana_gym(username)
    keyboard = [
        [
            InlineKeyboardButton("Reset", callback_data="resetta"),
            InlineKeyboardButton("Next week", callback_data="aumenta"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        f"You are currently on week {week}. Do you want to move to the next one or reset?",
        reply_markup=reply_markup
    )

async def visualizza_scheda(update: Update, context: CallbackContext):
    query = update.callback_query  
    await query.answer()  
    keyboard = [
        [
            InlineKeyboardButton("Day A", callback_data="a"),
            InlineKeyboardButton("Day B", callback_data="b"),
            InlineKeyboardButton("Day C", callback_data="c"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Select the day:", reply_markup=reply_markup)

async def manda_scheda(update: Update, context: CallbackContext):
    username = update.effective_user.first_name.lower()
    query = update.callback_query
    giorno = query.data
    await query.answer()  
    scheda = get_scheda(username, giorno)
    await query.message.reply_text(
        f"Your workout for day {giorno.upper()} is: {scheda}"
    )

async def modifica_scheda(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Day A", callback_data="1"),
            InlineKeyboardButton("Day B", callback_data="2"),
            InlineKeyboardButton("Day C", callback_data="3"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Select the day:", reply_markup=reply_markup)

async def cambio_scheda(update: Update, context: CallbackContext):
    global change_scheda, giorno
    query = update.callback_query
    await query.answer()
    change_scheda = True
    giorno = {"1": "a", "2": "b", "3": "c"}.get(query.data, "")
    await query.message.reply_text(f"Enter the new workout for day {giorno.upper()}:")

async def ricevi_testo(update: Update, context: CallbackContext):
    global change_scheda, giorno
    username = update.effective_user.first_name.lower()
    if change_scheda:
        text = update.message.text
        modifica_scheda_gym(username, giorno, text)
        change_scheda = False 
        await update.message.reply_text("Workout updated successfully!")
    else:
        await update.message.reply_text("You haven’t selected a workout to edit.")

async def aumenta_settimana(update: Update, context: CallbackContext):
    username = update.effective_user.first_name.lower()
    query = update.callback_query
    await query.answer()
    aumenta_settimana_gym(username)
    week = visualizza_settimana_gym(username)
    await query.message.reply_text(f"You are now on week {week}.")

async def resetta_settimana(update: Update, context: CallbackContext):
    username = update.effective_user.first_name.lower()
    query = update.callback_query
    await query.answer()
    resetta_settimana_gym(username)
    week = visualizza_settimana_gym(username)
    await query.message.reply_text(f"You are now on week {week}.")

# === AVVIO ===
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(visualizza_scheda, pattern="^visualizza$"))
    application.add_handler(CallbackQueryHandler(modifica_scheda, pattern="^modifica$")) 
    application.add_handler(CallbackQueryHandler(visualizza_settimana, pattern="^settimana$"))
    application.add_handler(CallbackQueryHandler(manda_scheda, pattern="^(a|b|c)$"))
    application.add_handler(CallbackQueryHandler(cambio_scheda, pattern="^(1|2|3)$"))
    application.add_handler(CallbackQueryHandler(aumenta_settimana, pattern="^aumenta$"))
    application.add_handler(CallbackQueryHandler(resetta_settimana, pattern="^resetta$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ricevi_testo))

    application.run_polling()

if __name__ == "__main__":
    main()
