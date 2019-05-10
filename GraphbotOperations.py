import networkx as nx
import pandas as pd

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
    #print(df_population)
    
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