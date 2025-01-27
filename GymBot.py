from Firebase import get_scheda, modifica_scheda_gym
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, ContextTypes, filters

white_list = ["al3ssandro", "francesco", "the skanner", "1234"]
username = None
change_scheda = False
giorno = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global username
    username = update.effective_user.first_name.lower()
    tastiera = [
        [
            InlineKeyboardButton("Visualizza scheda", callback_data="visualizza"),
            InlineKeyboardButton("Modifica scheda", callback_data="modifica"),
        ]
    ]
    tastiera_markup = InlineKeyboardMarkup(tastiera)
    await update.message.reply_text(
        f"ciao {username}, cosa vuoi fare?",
        reply_markup=tastiera_markup
    )

async def visualizza_scheda(update: Update, context: CallbackContext):
    query = update.callback_query  
    if query:
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
    query = update.callback_query
    giorno = query.data
    await query.answer()  
    scheda = get_scheda(username, giorno)
    await query.message.reply_text(
        f"La tua scheda per il giorno {giorno.upper()} è: {scheda}"
    )

async def modifica_scheda(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
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
    query = update.callback_query
    if query:
        await query.answer()
        change_scheda = True
        if query.data == "1":
            giorno = "a"
        elif query.data == "2":
            giorno = "b"
        elif query.data == "3":
            giorno = "c"
        await query.message.reply_text(
            f"Inserisci la nuova scheda per il giorno {giorno.down()}:"
        )

async def ricevi_testo(update: Update, context: CallbackContext):
    global change_scheda, giorno
    if change_scheda:
        testo = update.message.text
        modifica_scheda_gym(username, giorno, testo)
        change_scheda = False 
        await update.message.reply_text(
            "Scheda modificata con successo!"
        )
    else:
        await update.message.reply_text(
            "Non hai selezionato una scheda da modificare."
        )

def main():
    TOKEN = "TOKEN"
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(visualizza_scheda, pattern="^visualizza$"))
    application.add_handler(CallbackQueryHandler(modifica_scheda, pattern="^modifica$")) 
    application.add_handler(CallbackQueryHandler(manda_scheda, pattern="^(a|b|c)$"))
    application.add_handler(CallbackQueryHandler(cambio_scheda, pattern="^(1|2|3)$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ricevi_testo))

    application.run_polling()

if __name__ == "__main__":
    main()
