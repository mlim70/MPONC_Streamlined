# graph_handler

import osmnx as ox
import networkx as nx
import pickle
import os
from helper import GRAPH_CACHE_DIR
from hasher import hash_function

# =========================
# GRAPH FILE INITIALIZATION
# =========================

def create_graph(gdf):
    """ Initialize graph from Geodataframe"""
    print("Creating [GRAPH] from OSM.")
    # Combine all shapes
    combined_geom = gdf.unary_union
    
    # Generate the graph from the combined geometry
    g = ox.graph_from_polygon(combined_geom, network_type='drive', simplify=True
    )
    
    # Ensure the graph is strongly connected
    if not nx.is_strongly_connected(g):
        print("Graph is not strongly connected. Isolating the largest strongly connected component.")
        g = g.subgraph(
            max(nx.strongly_connected_components(g), key=len)
        ).copy()
    
    # Convert node labels to integers
    g = nx.convert_node_labels_to_integers(g)
    return g

def save_graph(g, layer_urls, cache_dir=GRAPH_CACHE_DIR):
    """ Save graph to cache """
    cache_key = f"graph_{hash_function(layer_urls)}.pkl"
    cache_path = os.path.join(cache_dir, cache_key)
    
    with open(cache_path, 'wb') as file:
        pickle.dump(g, file)

    print(f"[GRAPH] saved to '{cache_path}'.")

def load_graph(layer_urls, cache_dir=GRAPH_CACHE_DIR):
    """ Load graph from cache """
    cache_key = f"graph_{hash_function(layer_urls)}.pkl"
    cache_path = os.path.join(cache_dir, cache_key)
    try:
        with open(cache_path, 'rb') as file:
            g = pickle.load(file)
            print(f"[GRAPH] loaded from cache.")
        return g
    except:
        print("[load_graph] File not found.")
        return None