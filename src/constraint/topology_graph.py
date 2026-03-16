"""
Topology Graph — Physical LNG network as a directed graph.

Input: config/terminals.yaml, config/routes.yaml
Output: NetworkX MultiDiGraph with queryable route attributes

Core functions:
- build_graph: construct graph from YAML configs
- get_routes: all routes between origin and destination
- disable_bottleneck: simulate chokepoint closure by removing constrained edges
- get_feasible_routes: routes still available after disruption
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import networkx as nx
import yaml


@dataclass
class Route:
    """A single shipping route (edge) with full attributes."""
    route_id: str
    origin: str
    destination: str
    via: str
    distance_nm: float
    transit_days: float
    toll_usd: float
    bog_rate: float
    capacity_constraint: Optional[str]


def _load_yaml(path: str | Path) -> dict:
    """Load a YAML file and return parsed dict."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_graph(
    terminals_path: str | Path,
    routes_path: str | Path,
) -> nx.MultiDiGraph:
    """Build the LNG topology graph from config YAMLs.

    Uses MultiDiGraph to support multiple routes between the same terminal pair
    (e.g., US Gulf → Korea via Panama / Cape / Suez).

    Nodes are terminals (with type, capacity, region, coords).
    Edges are shipping routes keyed by route_id, with transit_days, toll, etc.
    """
    terminals_cfg = _load_yaml(terminals_path)
    routes_cfg = _load_yaml(routes_path)

    G = nx.MultiDiGraph()

    # Add terminal nodes
    for category in ("liquefaction", "regasification"):
        if category not in terminals_cfg:
            continue
        for tid, attrs in terminals_cfg[category].items():
            G.add_node(tid, **attrs)

    # Store bottleneck definitions as graph-level attributes
    if "bottlenecks" in routes_cfg:
        G.graph["bottlenecks"] = routes_cfg["bottlenecks"]

    # Add route edges (keyed by route_id for multi-edge support)
    for route_id, attrs in routes_cfg.get("routes", {}).items():
        origin = attrs["origin"]
        dest = attrs["destination"]
        G.add_edge(
            origin,
            dest,
            key=route_id,
            route_id=route_id,
            via=attrs.get("via", "direct"),
            distance_nm=attrs.get("distance_nm", 0),
            transit_days=attrs.get("transit_days", 0),
            toll_usd=attrs.get("toll_usd", 0),
            bog_rate=attrs.get("bog_rate", 0.001),
            capacity_constraint=attrs.get("capacity_constraint"),
        )

    return G


def get_routes(
    graph: nx.MultiDiGraph,
    origin: str,
    destination: str,
) -> List[Route]:
    """Return all route edges between origin and destination."""
    routes = []
    if not graph.has_node(origin) or not graph.has_node(destination):
        return routes
    if graph.has_edge(origin, destination):
        for key, data in graph[origin][destination].items():
            routes.append(_edge_to_route(origin, destination, data))
    return routes


def get_all_routes(graph: nx.MultiDiGraph) -> List[Route]:
    """Return every route in the graph."""
    return [
        _edge_to_route(u, v, data)
        for u, v, key, data in graph.edges(keys=True, data=True)
    ]


def disable_bottleneck(
    graph: nx.MultiDiGraph,
    bottleneck_id: str,
) -> nx.MultiDiGraph:
    """Return a new graph with all edges constrained by bottleneck_id removed.

    Does NOT mutate the input graph.
    """
    G = graph.copy()
    edges_to_remove = [
        (u, v, key)
        for u, v, key, data in G.edges(keys=True, data=True)
        if data.get("capacity_constraint") == bottleneck_id
    ]
    G.remove_edges_from(edges_to_remove)
    return G


def get_feasible_routes(
    graph: nx.MultiDiGraph,
    origin: str,
    destination: str,
) -> List[Route]:
    """Return routes still available between origin and destination.

    Identical to get_routes but named explicitly for post-disruption queries.
    """
    return get_routes(graph, origin, destination)


def get_routes_through_bottleneck(
    graph: nx.MultiDiGraph,
    bottleneck_id: str,
) -> List[Route]:
    """Return all routes that transit through a given bottleneck."""
    return [
        _edge_to_route(u, v, data)
        for u, v, key, data in graph.edges(keys=True, data=True)
        if data.get("capacity_constraint") == bottleneck_id
    ]


def update_capacity(
    graph: nx.MultiDiGraph,
    bottleneck_id: str,
    capacity_timeline: Dict[str, float],
    month: str,
) -> nx.MultiDiGraph:
    """Update edge capacity constraints for a bottleneck at a given month.

    If capacity is 0, removes all edges through that bottleneck (full closure).
    Otherwise, stores the current capacity as an edge attribute.

    Returns a new graph; does NOT mutate input.
    """
    G = graph.copy()
    capacity = capacity_timeline.get(month)
    if capacity is None:
        return G

    if capacity == 0:
        return disable_bottleneck(G, bottleneck_id)

    # Update capacity on relevant edges
    for u, v, key, data in G.edges(keys=True, data=True):
        if data.get("capacity_constraint") == bottleneck_id:
            G[u][v][key]["current_capacity"] = capacity

    return G


def _edge_to_route(origin: str, destination: str, data: dict) -> Route:
    """Convert edge attribute dict to Route dataclass."""
    return Route(
        route_id=data.get("route_id", "unknown"),
        origin=origin,
        destination=destination,
        via=data.get("via", "direct"),
        distance_nm=data.get("distance_nm", 0),
        transit_days=data.get("transit_days", 0),
        toll_usd=data.get("toll_usd", 0),
        bog_rate=data.get("bog_rate", 0.001),
        capacity_constraint=data.get("capacity_constraint"),
    )
