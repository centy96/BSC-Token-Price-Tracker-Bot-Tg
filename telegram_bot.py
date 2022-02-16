from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from dotenv import load_dotenv
import os
import logging
import price_calculator as pc

#LOAD PRIVATE APIKEY
load_dotenv()
MY_API_KEY = os.getenv("MY_API_KEY")

#VARIABLE
coin_address = 0
interest_point = 0
last_price = 0
prezzo_riferimento = 0
TOKEN_ADDRESS_STORAGE, INTEREST_POINT_STORAGE, GET_INFO,MAIN_LOOP = range(4)

def start(update:Update, context:CallbackContext):
    update.message.reply_text("Invia l'address del token che vuoi seguire",)
    return TOKEN_ADDRESS_STORAGE

def token_address_storage (update, context):
    global coin_address
    update.message.reply_text("Percentuale di riferimento")
    coin_address = update.message.text
    return  INTEREST_POINT_STORAGE
    
def interest_point_storage(update, context):
    global interest_point
    interest_point = int(update.message.text)
    update.message.reply_text("Per iniziare a traccaire il token e ottenere le informazioni del token:\n\n Clicca qui ----> /get_info")
    print(interest_point)
    return GET_INFO

def get_info(update, context):
    update.message.reply_text(pc.get_info(coin_address) + f"\n Percentuale di interesse: {interest_point}%\n\nClicca qui per iniziare ad usare il bot: /get_start")
    return MAIN_LOOP

def done(update, context):
    update.message.reply_text(
        f'Grazie per aver usato il nostro bot!', reply_markup= ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main_loop(update, context):
    global prezzo_riferimento, last_price, coin_address
    prezzo_riferimento = pc.get_price(coin_address)
    pc.main_loop(update,context,coin_address,interest_point,prezzo_riferimento,)


def main(): 
    updater = Updater(token=MY_API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            TOKEN_ADDRESS_STORAGE: [MessageHandler(Filters.text, token_address_storage)],
            INTEREST_POINT_STORAGE: [MessageHandler(Filters.text, interest_point_storage)],
            GET_INFO: [CommandHandler('get_info',get_info)],
            MAIN_LOOP:[CommandHandler("get_start",main_loop)]
        },
        fallbacks=[CommandHandler('done', done)],
    )
    dispatcher.add_handler(conv_handler)


    updater.start_polling()

if __name__ == "__main__":
    main()


