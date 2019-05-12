import networkx as nx
import pandas as pd
from staticmap import StaticMap, CircleMarker

# retorna un graf amb els nodes i arestes corresponents a la distància
# i població donats
def graph(g, distance, population):
    # creació nou graf
    G = nx.Graph()

    # obtenció de dades
    url = 'https://github.com/jordi-petit/lp-graphbot-2019/blob/master/dades/worldcitiespop.csv.gz?raw=true'
    df = pd.read_csv(url, usecols = ['Country', 'City', 'Population', 'Latitude', 'Longitude'], compression = 'gzip', low_memory = False)
    
    # filtrar: quedar-nos amb les poblacions amb població >= population
    df_population = df[df.Population >= population]

    # afegir nodes
    for x in range(len(df_population)):
        G.add_node(x, country=df_population.iloc[x, 0], city=df_population.iloc[x, 1], population=df_population.iloc[x, 2], latitude=df_population.iloc[x, 3], longitude=df_population.iloc[x, 4])

    return G

# retorna el número de nodes de g
def nodes(g):
    return len(g.nodes)

# retorna el número d'arestes de g
def edges(g):
    return len(g.edges)

# retorna el número de components connexes de g
def components(g):
    return len(list(nx.connected_components(g)))

# retorna la imatge d'un mapa amb totes les ciutats del graf a distància menor o igual que <dist> de <lat>,<lon>
# cada ciutat es mostra amb un cercle, de radi proporcional a la seva població
def plotpop(g, dist, lat, lon):
    # crear mapa
    mapa = StaticMap(500, 500)

    # afegir markers
    mapa = afegirCiutats(g, mapa, dist, lat, lon)

    # crear imatge
    return mapa.render()

# retorna la imatge d'un mapa amb totes les ciutats del graf a distància menor o igual que <dist> de <lat>,<lon> i totes les arestes que les connecten
# cada ciutat es mostra amb un cercle, de radi proporcional a la seva població
# cada aresta es mostra amb una línia blava
def plotgraph(g, dist, lat, lon):
    # crear mapa
    mapa = StaticMap(500, 500)

    # afegir markers i arestes
    mapa = afegirCiutats(g, mapa, dist, lat, lon)
    #mapa = afegirArestes(g, mapa, dist, lat, lon)

    # crear imatge
    return mapa.render()

# retorna la imatge d'un mapa amb les arestes del camí més curt per anar entre dues ciutats <src> i <dst>
def route(g, src, dst):
    # crear mapa
    mapa = StaticMap(500, 500)

    # trobar i pintar ruta

    # crear imatge
    return mapa.render()

# retorna el mapa amb els nodes de <g> amb distància menor o igual que <dist> de <lat>,<lon> pintats
def afegirCiutats(g, mapa, dist, lat, lon):
    for n in list(g.nodes):
        latitude = g.nodes[n]['latitude']
        longitude = g.nodes[n]['longitude']
        population = g.nodes[n]['population']
        mapa.add_marker(CircleMarker((latitude, longitude), 'red', population/(2*1000000)))

    return mapa