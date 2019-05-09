# importa l'API de Telegram
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

# /start
def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = 'Hola! Benvingut al Graphbot v0.1')

# /help
def help(bot, update):
    t = text_help()
    bot.send_message(chat_id = update.message.chat_id, text = t)

def text_help():
    text = '/start\n' + '/help\n' + '/author\n' + '/graph <distance> <population>\n' + '/nodes\n' + '/edges\n' + '/components\n' + '/plotpop <dist> [<lat> <lon>]\n' + '/plotgraph <dist> [<lat> <lon>]\n' + '/route <src> <dst>'
    return text

# /author
def author(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = 'Albert Teira Osuna\n' + 'albert.teira@est.fib.upc.edu')

# /graph <distance> <population>

# /nodes

# /edges

# /components

# /plotpop <dist> [<lat> <lon>]

# /plotgraph <dist> [<lat> <lon>]

# /route <src> <dst>

# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))

# engega el bot
updater.start_polling()