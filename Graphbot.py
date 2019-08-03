import os
import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import GraphbotOperations as gbOp
import MyExceptions


# /start
def start(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text='Hello! Welcome to Graphbot v1.0')
    bot.send_message(chat_id=update.message.chat_id, text='Starting to download the data...')
    try:
        user_data['data'] = gbOp.getData()
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='No response')
    bot.send_message(chat_id=update.message.chat_id, text='Data downloaded successfully')
    graph(bot, update, [300, 100000], user_data)


# /help
def help(bot, update):
    missatge = '/start: starts the conversation with the bot, downloads the data and creates the initial graph\n'
    missatge += '/help: shows this help panel\n'
    missatge += '/author: shows who made this bot\n'
    missatge += '/graph <distance> <population>: creates a graph with nodes representing cities with more or equal <population> and edges representing paths between two nodes that are closer than <distance>\n'
    missatge += '/nodes: number of nodes of the graph\n'
    missatge += '/edges: number of edges of the graph\n'
    missatge += '/components: number of components of the graph\n'
    missatge += '/plotpop <dist> [<lat> <lon>]: paints a map with all the nodes that are visible\n'
    missatge += '/plotgraph <dist> [<lat> <lon>]: paints a map with all the nodes and edges that are visible\n'
    missatge += '/route <src> <dst>: paints a map with the shortest route between <src> and <dst>. Example of usage: /route "Barcelona, es" "Paris, fr"\n'
    missatge += '*The initial graph is: /graph 300 100000\n'
    missatge += '*One node/edge is visible if it is inside the circle formed by <lat> <lon> as the center and <dist> as the radius'
    bot.send_message(chat_id=update.message.chat_id, text=missatge)


# /author
def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Albert Teira Osuna\n' + 'albert.teira@est.fib.upc.edu')


# /graph <distance> <population>
# args[0] = distance
# args[1] = population
def graph(bot, update, args, user_data):
    try:
        gbOp.checkData(user_data)
        if len(args) == 2:
            bot.send_message(chat_id=update.message.chat_id, text='Please, wait until the graph is made. Thanks!')
            user_data['graph'] = gbOp.graph(args[0], args[1], user_data['data'])
            bot.send_message(chat_id=update.message.chat_id, text='The graph has been updated')
        else:
            raise IndexError()
    except ValueError:
        print('ValueError')
        bot.send_message(chat_id=update.message.chat_id, text='Value error')
    except IndexError:
        print('IndexError')
        bot.send_message(chat_id=update.message.chat_id, text='Usage: /graph <distance> <population>')
    except MyExceptions.NoGraphLoadedException as e:
        print(e.text)
        bot.send_message(chat_id=update.message.chat_id, text=e.text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='No response')


# /nodes
def nodes(bot, update, user_data):
    try:
        gbOp.checkUserData(user_data)
        n_nodes = gbOp.nodes(user_data['graph'])
        bot.send_message(chat_id=update.message.chat_id, text=n_nodes)
    except MyExceptions.NoGraphLoadedException as e:
        print(e.text)
        bot.send_message(chat_id=update.message.chat_id, text=e.text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='No response')


# /edges
def edges(bot, update, user_data):
    try:
        gbOp.checkUserData(user_data)
        n_edges = gbOp.edges(user_data['graph'])
        bot.send_message(chat_id=update.message.chat_id, text=n_edges)
    except MyExceptions.NoGraphLoadedException as e:
        print(e.text)
        bot.send_message(chat_id=update.message.chat_id, text=e.text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='No response')


# /components
def components(bot, update, user_data):
    try:
        gbOp.checkUserData(user_data)
        n_components = gbOp.components(user_data['graph'])
        bot.send_message(chat_id=update.message.chat_id, text=n_components)
    except MyExceptions.NoGraphLoadedException as e:
        print(e.text)
        bot.send_message(chat_id=update.message.chat_id, text=e.text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='No response')


# /plotpop <dist> [<lat> <lon>]
# args[0] = dist
# args[1] = lat
# args[2] = lon
def plotpop(bot, update, args, user_data):
    try:
        # inicialitzacions
        lat, lon = 0, 0
        # creació imatge del mapa i enviament al bot
        image_file = '_plotpop.png'
        if len(args) == 1:
            if 'latitude' in user_data and 'longitude' in user_data:
                lat = user_data['latitude']
                lon = user_data['longitude']
            else:
                raise MyExceptions.LocationException
        elif len(args) == 3:
            lat, lon = args[1], args[2]
        else:
            raise IndexError()
        gbOp.checkUserData(user_data)
        image = gbOp.plotpop(user_data['graph'], args[0], lat, lon)
        image.save(image_file)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(image_file, 'rb'))
        os.remove(image_file)
    except ValueError:
        print('ValueError')
        bot.send_message(chat_id=update.message.chat_id, text='Value error')
    except IndexError:
        print('IndexError')
        bot.send_message(chat_id=update.message.chat_id, text='Usage: /plotpop <dist> [<lat> <lon>]')
    except (MyExceptions.LocationException, MyExceptions.MapRenderException, MyExceptions.NoGraphLoadedException) as e:
        print(e.text)
        bot.send_message(chat_id=update.message.chat_id, text=e.text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='No response')


# /plotgraph <dist> [<lat> <lon>]
# args[0] = dist
# args[1] = lat
# args[2] = lon
def plotgraph(bot, update, args, user_data):
    try:
        # creació imatge del mapa i enviament al bot
        image_file = '_plotgraph.png'
        if len(args) == 1:
            if 'latitude' in user_data and 'longitude' in user_data:
                lat = user_data['latitude']
                lon = user_data['longitude']
            else:
                raise MyExceptions.LocationException
        elif len(args) == 3:
            lat, lon = args[1], args[2]
        else:
            raise IndexError()
        gbOp.checkUserData(user_data)
        image = gbOp.plotgraph(user_data['graph'], args[0], lat, lon)
        image.save(image_file)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(image_file, 'rb'))
        os.remove(image_file)
    except ValueError:
        print('ValueError')
        bot.send_message(chat_id=update.message.chat_id, text='Value error')
    except IndexError:
        print('IndexError')
        bot.send_message(chat_id=update.message.chat_id, text='Usage: /plotgraph <dist> [<lat> <lon>]')
    except (MyExceptions.LocationException, MyExceptions.MapRenderException, MyExceptions.NoGraphLoadedException) as e:
        print(e.text)
        bot.send_message(chat_id=update.message.chat_id, text=e.text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='No response')


# /route <src> <dst>
# args[0] = src
# args[1] = dst
def route(bot, update, args, user_data):
    try:
        # creació imatge del mapa i enviament al bot
        image_file = '_route.png'
        gbOp.checkUserData(user_data)
        image = gbOp.route(user_data['graph'], args[0] + ' ' + args[1], args[2] + ' ' + args[3])
        image.save(image_file)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(image_file, 'rb'))
        os.remove(image_file)
    except ValueError:
        print('ValueError')
        bot.send_message(chat_id=update.message.chat_id, text='Value error')
    except IndexError:
        print('IndexError')
        bot.send_message(chat_id=update.message.chat_id, text='Usage: /route <src> <dst>\n<src>/<dst> format: "<city>, <country code>"')
    except (MyExceptions.MapRenderException, MyExceptions.NoGraphLoadedException, MyExceptions.NoPathFoundException) as e:
        print(e.text)
        bot.send_message(chat_id=update.message.chat_id, text=e.text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='No response')


def user_location(bot, update, user_data):
    lat, lon = update.message.location.latitude, update.message.location.longitude
    user_data['latitude'] = lat
    user_data['longitude'] = lon
    bot.send_message(chat_id=update.message.chat_id, text='Your location is ready')

# MAIN
# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# add_handler
dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args=True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotpop', plotpop, pass_args=True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_args=True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', route, pass_args=True, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.location, user_location, pass_user_data=True))

# engega el bot
updater.start_polling()
