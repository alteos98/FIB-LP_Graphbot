# imports
import pandas as pd

import networkx as nx

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

import GraphbotOperations as gbOp

# /start
def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = 'Hola! Benvingut al Graphbot v0.1')

# /help
def help(bot, update):
    missatge = '/start\n' + '/help\n' + '/author\n' + '/graph <distance> <population>\n' + '/nodes\n' + '/edges\n' + '/components\n' + '/plotpop <dist> [<lat> <lon>]\n' + '/plotgraph <dist> [<lat> <lon>]\n' + '/route <src> <dst>'
    bot.send_message(chat_id = update.message.chat_id, text = missatge)

# /author
def author(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = 'Albert Teira Osuna\n' + 'albert.teira@est.fib.upc.edu')

# /graph <distance> <population>
# args[0] = distance
# args[1] = population
def graph(bot, update, args):
    try:
        global G
        G = gbOp.graph(G, args[0], args[1])
    except IndexError:
        print('IndexError')
        bot.send_message(chat_id = update.message.chat_id, text = 'Usage: /graph <distance> <population>')
    except Exception as e:
        print(e)
        bot.send_message(chat_id = update.message.chat_id, text = 'No response')

# /nodes
def nodes(bot, update):
    try:
        n_nodes = gbOp.nodes(G)
        bot.send_message(chat_id = update.message.chat_id, text = n_nodes)
    except Exception as e:
        print(e)
        bot.send_message(chat_id = update.message.chat_id, text = 'No response')

# /edges
def edges(bot, update):
    try:
        n_edges = gbOp.edges(G)
        bot.send_message(chat_id = update.message.chat_id, text = n_edges)
    except Exception as e:
        print(e)
        bot.send_message(chat_id = update.message.chat_id, text = 'No response')

# /components
def components(bot, update):
    try:
        n_components = gbOp.components(G)
        bot.send_message(chat_id = update.message.chat_id, text = n_components)
    except Exception as e:
        print(e)
        bot.send_message(chat_id = update.message.chat_id, text = 'No response')

# /plotpop <dist> [<lat> <lon>]
# args[0] = dist
# args[1] = lat
# args[2] = lon
def plotpop(bot, update, args):
    try:
        print('plotpop')
        # creació imatge del mapa
        # enviament de la imatge al bot
    except IndexError:
        print('IndexError')
        bot.send_message(chat_id = update.message.chat_id, text = 'Usage: /plotpop <dist> [<lat> <lon>]')
    except Exception as e:
        print(e)
        bot.send_message(chat_id = update.message.chat_id, text = 'No response')

# /plotgraph <dist> [<lat> <lon>]
# args[0] = dist
# args[1] = lat
# args[2] = lon
def plotgraph(bot, update, args):
    try:
        print('plotgraph')
        # creació imatge del mapa
        # enviament de la imatge al bot
    except IndexError:
        print('IndexError')
        bot.send_message(chat_id = update.message.chat_id, text = 'Usage: /plotgraph <dist> [<lat> <lon>]')
    except Exception as e:
        print(e)
        bot.send_message(chat_id = update.message.chat_id, text = 'No response')

# /route <src> <dst>
# args[0] = src
# args[1] = dst
def route(bot, update, args):
    try:
        print('route')
        # creació imatge del mapa
        # enviament de la imatge al bot
    except IndexError:
        print('IndexError')
        bot.send_message(chat_id = update.message.chat_id, text = 'Usage: /route <src> <dst>')
    except Exception as e:
        print(e)
        bot.send_message(chat_id = update.message.chat_id, text = 'No response')


## MAIN
# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args = True))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('components', components))
dispatcher.add_handler(CommandHandler('plotpop', plotpop, pass_args = True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_args = True))
dispatcher.add_handler(CommandHandler('route', route, pass_args = True))

# engega el bot
updater.start_polling()

# creem el graf inicial
G = nx.Graph()
G = gbOp.graph(G, 300, 100000)
