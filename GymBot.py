import Firebase 
from Firebase import (
    get_scheda,
    modifica_scheda_gym,
    aumenta_settimana_gym,
    resetta_settimana_gym,
    visualizza_settimana_gym
)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, ContextTypes, filters

white_list = ["name1", "name2", "name3", "name4"]
username = None
change_scheda = False
giorno = ""



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.first_name.lower()
    tastiera = [
        [
            InlineKeyboardButton("Visualizza scheda", callback_data="visualizza"),
            InlineKeyboardButton("Modifica scheda", callback_data="modifica"),
            InlineKeyboardButton("Visualizza settimana", callback_data="settimana"),
        ]
    ]
    tastiera_markup = InlineKeyboardMarkup(tastiera)
    await update.message.reply_text(
        f"Ciao {username}, cosa vuoi fare?",
        reply_markup=tastiera_markup
    )

async def visualizza_settimana(update: Update, context: CallbackContext):
    
    query = update.callback_query
    await query.answer()
    sett = visualizza_settimana_gym(username)
    tastiera = [
        [
            InlineKeyboardButton("Resetta", callback_data="resetta"),
            InlineKeyboardButton("Aumenta", callback_data="aumenta"),
        ]
    ]
    tastiera_markup = InlineKeyboardMarkup(tastiera)
    await query.message.reply_text(
        f"Attualmente stai facendo la {sett}ª settimana. Vuoi passare alla successiva o tornare alla prima?",
        reply_markup=tastiera_markup
    )

async def visualizza_scheda(update: Update, context: CallbackContext):
    username = update.effective_user.first_name.lower()
    query = update.callback_query  
    await query.answer()  
    tastiera = [
        [
            InlineKeyboardButton("Giorno A", callback_data="a"),
            InlineKeyboardButton("Giorno B", callback_data="b"),
            InlineKeyboardButton("Giorno C", callback_data="c"),
        ]
    ]
    tastiera_markup = InlineKeyboardMarkup(tastiera)
    await query.message.reply_text(
        "Seleziona il giorno:",
        reply_markup=tastiera_markup
    )

async def manda_scheda(update: Update, context: CallbackContext):
    username = update.effective_user.first_name.lower()
    query = update.callback_query
    giorno = query.data
    await query.answer()  
    scheda = get_scheda(username, giorno)
    await query.message.reply_text(
        f"La tua scheda per il giorno {giorno.upper()} è: {scheda}"
    )

async def modifica_scheda(update: Update, context: CallbackContext):
    username = update.effective_user.first_name.lower()
    query = update.callback_query
    await query.answer()
    tastiera = [
        [
            InlineKeyboardButton("Giorno A", callback_data="1"),
            InlineKeyboardButton("Giorno B", callback_data="2"),
            InlineKeyboardButton("Giorno C", callback_data="3"),
        ]
    ]
    tastiera_markup = InlineKeyboardMarkup(tastiera)
    await query.message.reply_text(
        "Seleziona il giorno:",
        reply_markup=tastiera_markup
    )

async def cambio_scheda(update: Update, context: CallbackContext):
    global change_scheda, giorno
    username = update.effective_user.first_name.lower()
    query = update.callback_query
    await query.answer()
    change_scheda = True
    giorno = {"1": "a", "2": "b", "3": "c"}.get(query.data, "")
    await query.message.reply_text(f"Inserisci la nuova scheda per il giorno {giorno.upper()}:")

async def ricevi_testo(update: Update, context: CallbackContext):
    global change_scheda, giorno
    username = update.effective_user.first_name.lower()
    if change_scheda:
        testo = update.message.text
        modifica_scheda_gym(username, giorno, testo)
        change_scheda = False 
        await update.message.reply_text("Scheda modificata con successo!")
    else:
        await update.message.reply_text("Non hai selezionato una scheda da modificare.")

async def aumenta_settimana(update: Update, context: CallbackContext):
    query = update.callback_query
    username = update.effective_user.first_name.lower()
    await query.answer()
    aumenta_settimana_gym(username)
    sett = visualizza_settimana_gym(username)
    await query.message.reply_text(f"Attualmente stai facendo la {sett}ª settimana.")

async def resetta_settimana(update: Update, context: CallbackContext):
    query = update.callback_query
    username = update.effective_user.first_name.lower()
    await query.answer()
    resetta_settimana_gym(username)
    sett = visualizza_settimana_gym(username)
    await query.message.reply_text(f"Attualmente stai facendo la {sett}ª settimana.")

def main():
    TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
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
