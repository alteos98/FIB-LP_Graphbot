# Graphbot

This is the Python project I made in LP (Programming Languages) subject. It consists in a Telegram bot with a set of funcionalities. Below you have all the things that you can do with it.

## Getting Started

### Prerequisites

To install the prerequisities, you only have to run:

```
pip install -r requirements.txt
```

You also have to create a token for your bot and put it into **token.txt**.

### Running

To use the Graphbot you only have to follow these steps:

Run the Graphbot.py.

```
python Graphbot.py
```

Make sure you have a Telegram account and click this [link](https://telegram.me/aleta001_bot) to open the bot.

Now you are ready to start using the bot.

## How to use it?

- /start: starts the conversation with the bot, downloads the data and creates the initial graph
- /help: shows this help panel
- /author: shows who made this bot
- /graph \<distance> \<population>: creates a graph with nodes representing cities with more or equal \<population> and edges representing paths between two nodes that are closer than \<distance>
- /nodes: number of nodes of the graph
- /edges: number of edges of the graph
- /components: number of components of the graph
- /plotpop \<dist> \[\<lat> \<lon>]: paints a map with all the nodes that are visible
- /plotgraph \<dist> \[\<lat> \<lon>]: paints a map with all the nodes and edges that are visible
- /route \<src> \<dst>: paints a map with the shortest route between \<src> and \<dst>. Example of usage: /route "Barcelona, es" "Paris, fr"

*The initial graph is: /graph 300 100000  
*One node/edge is visible if it is inside the circle formed by \<lat> \<lon> as the center and \<dist> as the radius

## Author

* **Albert Teira Osuna** - [My Github](https://github.com/alteos98)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
