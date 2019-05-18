import networkx as nx
import pandas as pd
from haversine import haversine
from staticmap import StaticMap, CircleMarker, Line
from fuzzywuzzy import fuzz, process

import time
import math
from itertools import repeat

import MyExceptions

def getData():
    # obtenció de dades
    t_start = time.time()
    url = 'https://github.com/jordi-petit/lp-graphbot-2019/blob/master/dades/worldcitiespop.csv.gz?raw=true'
    df = pd.read_csv(url, usecols=['Country', 'City', 'Population', 'Latitude', 'Longitude'], compression='gzip', low_memory=False)
    t_end = time.time()
    t_total = t_end - t_start
    print('Temps en obtenir les dades: ', t_total)
    return df

# retorna un graf amb els nodes i arestes corresponents a la distància
# i població donats
def graph(distance, population, data):
    distance = float(distance)
    population = float(population)

    # creació nou graf
    g = nx.Graph()

    # obtenció de dades
    df = data
    
    # filtrar: quedar-nos amb les poblacions amb població >= population
    df_population = df[df.Population >= population]
    # ordenar per latitud
    df_population.sort_values(by='Latitude', inplace=True, ascending=False)

    # afegir nodes
    t_start = time.time()
    for x in range(len(df_population)):
        g.add_node(x, country=df_population.iloc[x, 0], city=df_population.iloc[x, 1], population=df_population.iloc[x, 2], latitude=df_population.iloc[x, 3], longitude=df_population.iloc[x, 4], visible=True)
    t_end = time.time()
    t_total = t_end - t_start
    print('Temps en afegir nodes: ', t_total)

    # creació dels conjunts en funció de la latitud i distance
    km_per_grade_lat = 111.12
    km_per_grade_lon = 111.32 # fer funció que calculi la lon transformada en funció de cada grau de lon
    n_grades_lat = 180.0
    n_grades_lon = 360.0
    n_conjunts_i = math.ceil(n_grades_lat*km_per_grade_lat/float(distance))
    n_conjunts_j = math.ceil(n_grades_lon*km_per_grade_lon/float(distance))
    conjunts_lat = [[[] for j in repeat(None, n_conjunts_j)] for i in repeat(None, n_conjunts_i)]
    for x in range(len(df_population)):
        i_conjunt = math.floor((df_population.iloc[x, 3] + 90)*km_per_grade_lat/float(distance)) # -90 <= x <= 90 ===> 0 <= x <= 180
        j_conjunt = math.floor((df_population.iloc[x, 4] + 180)*km_per_grade_lon/float(distance))
        conjunts_lat[i_conjunt][j_conjunt].append(x)

    # afegir arestes
    t_start = time.time()
    for i in range(len(conjunts_lat)):
        for j in range(len(conjunts_lat[i])):
            for k in range(len(conjunts_lat[i][j])):
                x = conjunts_lat[i][j][k]
                for t in [i, i+1]:
                    for l in [j, j+1]:
                        if i == t and j == l:
                            _p = k+1
                        else:
                            _p = 0
                        if t < n_conjunts_i and l < n_conjunts_j:
                            for p in range(_p, len(conjunts_lat[t][l])):
                                y = conjunts_lat[t][l][p]
                                dist = haversine((df_population.iloc[x, 3], df_population.iloc[x, 4]), (df_population.iloc[y, 3], df_population.iloc[y, 4]))
                                if dist <= float(distance):
                                    g.add_edge(x, y, weight=dist)
                                    #print('Added edge: ', x, ' ', y)
    t_end = time.time()
    t_total = t_end - t_start
    print('Temps en afegir arestes: ', t_total)

    return g

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
    # crear mapa i setejar visibilitat
    mapa = StaticMap(500, 500)
    g = setVisibilityNodes(g, dist, lat, lon)

    # afegir markers
    mapa = paintNodes(g, mapa, True)

    # crear imatge
    try:
        img = mapa.render()
    except:
        raise MyExceptions.MapRenderException
    
    return img

# retorna la imatge d'un mapa amb totes les ciutats del graf a distància menor o igual que <dist> de <lat>,<lon> i totes les arestes que les connecten
# cada ciutat es mostra amb un cercle, de radi proporcional a la seva població
# cada aresta es mostra amb una línia blava
def plotgraph(g, dist, lat, lon):
    # crear mapa i setejar visibilitat
    mapa = StaticMap(500, 500)
    g = setVisibilityNodes(g, dist, lat, lon)

    # afegir markers i arestes
    mapa = paintEdges(g, mapa)
    mapa = paintNodes(g, mapa, False)

    # crear imatge
    try:
        img = mapa.render()
    except:
        raise MyExceptions.MapRenderException
    
    return img

# retorna la imatge d'un mapa amb les arestes del camí més curt per anar entre dues ciutats <src> i <dst>
def route(g, src, dst):
    # crear mapa
    mapa = StaticMap(500, 500)

    # trobar els dos nodes fent servir Levenshtein
    src = src[1:-1]
    dst = dst[1:-1]
    cities_list = []
    for i_city in list(g.nodes):
        city = str(g.nodes[i_city]['city']) + ', ' + str(g.nodes[i_city]['country'])
        cities_list.append(city)
    src_city = process.extractOne(str(src), cities_list)[0].split(', ')
    dst_city = process.extractOne(str(dst), cities_list)[0].split(', ')
    i_src = 0
    i_dst = 0
    src_found = False
    dst_found = False
    for i_city in list(g.nodes):
        if not src_found and g.nodes[i_city]['city'] == src_city[0] and g.nodes[i_city]['country'] == src_city[1]:
            i_src = i_city
            src_found = True
        if not dst_found and g.nodes[i_city]['city'] == dst_city[0] and g.nodes[i_city]['country'] == dst_city[1]:
            i_dst = i_city
            dst_found = True

    # dijkstra
    try:
        path = nx.dijkstra_path(g, i_src, i_dst, weight='weight')
    except:
        raise MyExceptions.NoPathFoundException
    for i in range(len(path)):
        if i+1 < len(path):
            mapa.add_line(Line(((g.nodes[path[i]]['longitude'], g.nodes[path[i]]['latitude']), (g.nodes[path[i+1]]['longitude'], g.nodes[path[i+1]]['latitude'])), 'blue', 1))
        mapa.add_marker(CircleMarker((g.nodes[path[i]]['longitude'], g.nodes[path[i]]['latitude']), 'red', 2))

    # crear imatge
    try:
        img = mapa.render()
        return img
    except:
        raise MyExceptions.MapRenderException

# retorna el graf amb l'atribut 'visible' de cada node ajustat segons convingui
# un node és visible si es troba a menys o igual de 'dist' km de (lat, lon)
def setVisibilityNodes(g, dist, lat, lon):
    for n in list(g.nodes):
        latitude_node = float(g.nodes[n]['latitude'])
        longitude_node = float(g.nodes[n]['longitude'])
        population_node = float(g.nodes[n]['population'])
        g.nodes[n]['visible'] = haversine((latitude_node, longitude_node), (float(lat), float(lon))) <= float(dist)
    return g

# retorna el mapa amb els nodes de <g> amb distància menor o igual que <dist> de <lat>,<lon> pintats
def paintNodes(g, mapa, custom_size):
    for n in list(g.nodes):
        latitude_node = float(g.nodes[n]['latitude'])
        longitude_node = float(g.nodes[n]['longitude'])
        population_node = float(g.nodes[n]['population'])
        if g.nodes[n]['visible']:
            if custom_size:
                mapa.add_marker(CircleMarker((longitude_node, latitude_node), 'red', population_node/(2*100000)))
            else:
                mapa.add_marker(CircleMarker((longitude_node, latitude_node), 'red', 2))
    return mapa

def paintEdges(g, mapa):
    for m in list(g.edges):
        first_node = m[0]
        second_node = m[1]
        if g.nodes[first_node]['visible'] and g.nodes[second_node]['visible']:
            mapa.add_line(Line(((g.nodes[first_node]['longitude'], g.nodes[first_node]['latitude']), (g.nodes[second_node]['longitude'], g.nodes[second_node]['latitude'])), 'blue', 1))
    return mapa

def checkUserData(user_data):
    if 'graph' not in user_data:
        raise MyExceptions.NoGraphLoadedException

def checkData(user_data):
    if 'data' not in user_data:
        raise MyExceptions.NoGraphLoadedException