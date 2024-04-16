import networkx as nx
import json
from pathlib import Path

CACHE_DIR = Path('./cache')

CACHE_DIR.mkdir(exist_ok=True)


get_cache_file = lambda cache_key: CACHE_DIR / f'cache_{cache_key}.json'

def generate_cache_key(edges: list[float], dimension: str):
    key = ''.join(sorted([str(edge) for edge in edges])) + '_' + str(dimension)
    
    return hash(key)


def read_from_cache(cache_key: str):
    cache_file = get_cache_file(cache_key)

    if cache_file.exists():
        return json.loads(cache_file.read_text())
    
    return None


def write_to_cache(cache_key: str, data: list[float]):
    cache_file = get_cache_file(cache_key)

    cache_file.write_text(json.dumps(data, indent=4))

# Receiving 'from' and 'to' node lists and coordinate type from Tableau
from_nodes = _arg1
to_nodes = _arg2

dimension = str(_arg3).lower()
dim_ix = 0 if dimension == 'x' else 1

edges = list(zip(from_nodes, to_nodes))

input_path = CACHE_DIR / 'input.json'
input_path.write_text(json.dumps(edges, indent=4))

# Protect against empty or invalid input
if not edges or edges[0][0] is None or edges[0][1] is None:
    return [None] * len(from_nodes)

# Generate a cache key and attempt to read from cache
cache_key = generate_cache_key(edges=edges, dimension=dimension)
cached_result = read_from_cache(cache_key=cache_key)

if cached_result is not None:
    return cached_result

G = nx.Graph()
G.add_edges_from(edges)

positions = nx.spring_layout(G, iterations=2)  # Calculate node positions

# Map 'from' nodes to their coordinates
coords = [positions[node][dim_ix] if node in positions else None for node in from_nodes]

write_to_cache(cache_key=cache_key, data=coords)

return coords