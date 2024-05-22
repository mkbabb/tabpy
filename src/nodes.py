import functools
import hashlib
import json
import pickle
from pathlib import Path
from typing import Any, Callable, Literal

import networkx as nx  # type: ignore

CACHE_DIR = Path('cache/')

CACHE_DIR.mkdir(exist_ok=True)

Layouts = Literal[
    'spring', 'circular', 'random', 'shell', 'kamada_kawai', 'spectral', 'spiral'
]

SEED = 42


def cache_pickle(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        input_data = {'args': args, 'kwargs': kwargs}

        # Create a hash of the input data using pickle for serialization
        input_hash = hashlib.md5(pickle.dumps(input_data)).hexdigest()

        output_path = CACHE_DIR / f'{input_hash}_output.pkl'

        # Check if the result is already cached and return it if so
        if output_path.exists():
            with output_path.open('rb') as f:
                return pickle.load(f)

        # Compute the function's result if not cached
        output_data = func(*args, **kwargs)

        # Cache the result using pickle
        with output_path.open('wb') as f:
            pickle.dump(output_data, f)

        return output_data

    return wrapper


# @cache_pickle
def compute_layout(
    from_nodes: list[str],
    to_nodes: list[str],
    bases: list[str],
    layout: str,
    k: float = 0.5,
):
    t_edges = list(zip(from_nodes, to_nodes, bases))

    # edges_path = CACHE_DIR / 'input.json'

    # with edges_path.open('w') as f:
    #     json.dump(t_edges, f, indent=4)

    edges = [
        (from_node, to_node)
        for from_node, to_node, base in t_edges
        if base == 'original'
    ]

    # Protect against empty or invalid input
    if not len(edges) or edges[0] is None or edges[0] is None:
        return [None] * len(to_nodes)

    edges = [(f, t) for f, t, b in zip(from_nodes, to_nodes, bases) if b == 'original']

    G = nx.Graph()
    G.add_edges_from(edges)

    def get_mapping():
        if layout == 'spring':
            return nx.spring_layout(G, k=k, seed=SEED)
        elif layout == 'circular':
            return nx.circular_layout(G)
        elif layout == 'random':
            return nx.random_layout(G, seed=SEED)
        elif layout == 'shell':
            return nx.shell_layout(G)
        elif layout == 'kamada_kawai':
            return nx.kamada_kawai_layout(G)
        elif layout == 'spectral':
            return nx.spectral_layout(G)
        elif layout == 'spiral':
            return nx.spiral_layout(G)

    positions = get_mapping()

    if positions is None:
        return [None] * len(to_nodes)

    coords = []
    coords_set = set()

    for from_node, to_node, base in t_edges:
        coord = {
            'x': 0.0,
            'y': 0.0,
            'weight': 0.0,
        }

        if from_node not in positions or to_node not in positions:
            coords.append(coord)
            continue

        if base == 'mirrored' and dimension != 'weight':
            from_node, to_node = to_node, from_node

        x = positions[from_node][0]
        y = positions[from_node][1]
        weight = G.degree(from_node)

        if base != 'mirrored':
            weight = 0.0

        coord |= {
            'x': x,
            'y': y,
            'weight': weight,
        }

        coords.append(coord)
        coords_set.add((x, y))

    return coords


def main(
    from_nodes: list[str],
    to_nodes: list[str],
    bases: list[str],
    dimension: str,
    k: float = 0.5,
    layout: str = 'spring',
) -> list[float | None]:

    positions = compute_layout(
        from_nodes=from_nodes, to_nodes=to_nodes, bases=bases, layout=layout, k=k
    )

    dimension = dimension.lower()

    return [coord[dimension] for coord in positions]


# Example usage would be similar, but now the main function utilizes the separate compute_layout function to get the layout and then extracts dimension-specific data.

from_nodes = _arg1
to_nodes = _arg2
bases = _arg3
dimension = _arg4
layout = _arg5
k = _arg6


# edges = json.loads(open('./data/input.json').read())
# from_nodes, to_nodes, bases = zip(*edges)
# dimension = 'Y'
# layout = 'spring'
# k = 0.5

if isinstance(dimension, list):
    dimension = dimension[0]

if isinstance(layout, list):
    layout = layout[0]

if isinstance(k, list):
    k = k[0]


result = main(
    from_nodes=from_nodes,
    to_nodes=to_nodes,
    bases=bases,
    dimension=dimension,
    k=k,
    layout=layout,
)

return result
