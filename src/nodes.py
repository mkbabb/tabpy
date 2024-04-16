import networkx as nx
import os
import json

def generate_cache_key(edges: list[float], coord_type: str):
    t_key = ''.join(sorted([str(edge) for edge in edges])) + '_' + str(coord_type)
    
    return hash(t_key)


# Function to check and read from cache
def read_from_cache(cache_key: str):
    cache_file = f'./cache/cache_{cache_key}.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
        
    return None


# Function to write to cache
def write_to_cache(cache_key: str, data: list[float]):
    cache_file = f'./cache/cache_{cache_key}.json'
    with open(cache_file, 'w') as f:
        json.dump(data, f)

# Receiving 'from' and 'to' node lists and coordinate type from Tableau
from_nodes = _arg1
to_nodes = _arg2
coord_type = _arg3  # 'X' or 'Y'

edges = list(zip(from_nodes, to_nodes))

# Generate a cache key and attempt to read from cache
cache_key = generate_cache_key(edges=edges, coord_type=coord_type)
cached_result = read_from_cache(cache_key=cache_key)

if cached_result is not None:
    return cached_result

# Receiving 'from' and 'to' node lists from Tableau
from_nodes: list[str] = _arg1
to_nodes: list[str] = _arg2

dimension: str = str(_arg3).lower()

coord_ix = 0 if dimension == 'x' else 1

edges = list(zip(from_nodes, to_nodes))

# Protect against empty or invalid input
if not edges or edges[0][0] is None or edges[0][1] is None:
    return [None] * len(from_nodes) # Return a list of Nones matching the input size

G = nx.Graph()
G.add_edges_from(edges)

positions = nx.spring_layout(G)  # Calculate node positions

# Map 'from' nodes to their coordinates
coords = [positions[node][coord_ix] if node in positions else None for node in from_nodes]

write_to_cache(cache_key=cache_key, data=coords)

return coords