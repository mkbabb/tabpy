import functools
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Literal

import networkx as nx  # type: ignore

CACHE_DIR = Path("./cache")

Layouts = Literal[
    "spring", "circular", "random", "shell", "kamada_kawai", "spectral", "spiral"
]


SEED = 42


def cache_json(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Hash the input arguments
        input_data = {"args": args, "kwargs": kwargs}

        input_hash = hashlib.md5(json.dumps(input_data).encode()).hexdigest()

        output_path = CACHE_DIR / f"{input_hash}_output.json"

        # Check if the output file exists
        if output_path.exists():
            # Load the cached output from the file
            with output_path.open("r") as f:
                return json.load(f)

        # Call the original function
        output_data = func(*args, **kwargs)

        # Save the output input_data to the output file
        with output_path.open("w") as f:
            json.dump(output_data, f, indent=4)

        return output_data

    return wrapper


# @cache_json
def main(
    from_nodes: list[str],
    to_nodes: list[str],
    bases: list[str],
    dimension: str,
    k: float = 0.5,
    layout: str = "spring",
) -> list[float | None]:
    dimension = str(dimension).lower()
    dim_ix = 0 if dimension == "x" else 1

    t_edges = list(zip(from_nodes, to_nodes, bases))

    edges_path = CACHE_DIR / "input.json"
    edges_path.write_text(json.dumps(t_edges, indent=4))

    edges = [
        (from_node, to_node)
        for from_node, to_node, base in t_edges
        if base == "original"
    ]

    # Protect against empty or invalid input
    if not edges or edges[0][0] is None or edges[0][1] is None:
        return [None] * len(to_nodes)

    G = nx.Graph()
    G.add_edges_from(edges)

    positions = None
    if layout == "spring":
        positions = nx.spring_layout(G, k=k, seed=SEED)
    elif layout == "circular":
        positions = nx.circular_layout(G)
    elif layout == "random":
        positions = nx.random_layout(G, seed=SEED)
    elif layout == "shell":
        positions = nx.shell_layout(G)
    elif layout == "kamada_kawai":
        positions = nx.kamada_kawai_layout(G)
    elif layout == "spectral":
        positions = nx.spectral_layout(G)
    elif layout == "spiral":
        positions = nx.spiral_layout(G)
    else:
        return [None] * len(from_nodes)

    coords: list[float | None] = []

    for from_node, to_node, base in t_edges:
        if from_node not in positions or to_node not in positions:
            coords.append(0.0)
            continue

        if base == "mirrored":
            from_node, to_node = to_node, from_node

        if dimension == "weight":
            coords.append(G.degree(from_node))
        else:
            pos = positions[from_node]
            coords.append(pos[dim_ix])

    return coords


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
