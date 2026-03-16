"""
Tests for topology_graph.py

DEVPLAN §2a test requirements:
- Disable Panama → US Gulf to Asia only has Cape and Suez
- Disable Hormuz → Qatar to Asia routes all severed
- Disable both → verify graph connectivity
"""

import pytest
from pathlib import Path

from src.constraint.topology_graph import (
    build_graph,
    get_routes,
    get_all_routes,
    get_feasible_routes,
    disable_bottleneck,
    get_routes_through_bottleneck,
    update_capacity,
    Route,
)

# Resolve config paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TERMINALS_PATH = PROJECT_ROOT / "config" / "terminals.yaml"
ROUTES_PATH = PROJECT_ROOT / "config" / "routes.yaml"


@pytest.fixture
def graph():
    """Build the full topology graph from config files."""
    return build_graph(TERMINALS_PATH, ROUTES_PATH)


# ── Graph Construction ──────────────────────────────────────────────


class TestBuildGraph:
    def test_nodes_loaded(self, graph):
        """All terminals from config should be present as nodes."""
        # Liquefaction terminals
        for tid in ("sabine_pass", "cameron", "corpus_christi", "ras_laffan",
                     "northwest_shelf", "ichthys", "bintulu"):
            assert tid in graph.nodes, f"Missing liquefaction terminal: {tid}"
        # Regasification terminals
        for tid in ("incheon", "negishi", "futtsu", "dapeng", "zhoushan"):
            assert tid in graph.nodes, f"Missing regasification terminal: {tid}"

    def test_node_count(self, graph):
        assert len(graph.nodes) == 12  # 7 liq + 5 regas

    def test_edge_count(self, graph):
        assert graph.number_of_edges() == 12  # 12 routes in routes.yaml

    def test_node_attributes(self, graph):
        node = graph.nodes["sabine_pass"]
        assert node["type"] == "liquefaction"
        assert node["capacity_mtpa"] == 30.0
        assert node["region"] == "US Gulf Coast"

    def test_edge_attributes(self, graph):
        """Verify edge attributes are correctly loaded."""
        routes = get_routes(graph, "sabine_pass", "incheon")
        assert len(routes) == 3  # Panama, Cape, Suez
        route_ids = {r.route_id for r in routes}
        assert route_ids == {"usgc_asia_panama", "usgc_asia_cape", "usgc_asia_suez"}

    def test_bottleneck_metadata(self, graph):
        """Bottleneck definitions should be in graph-level attributes."""
        assert "bottlenecks" in graph.graph
        assert "panama_canal" in graph.graph["bottlenecks"]
        assert "hormuz_strait" in graph.graph["bottlenecks"]

    def test_multi_edge_support(self, graph):
        """Multiple routes between same (origin, dest) should all exist."""
        routes = get_routes(graph, "sabine_pass", "incheon")
        vias = {r.via for r in routes}
        assert "panama_canal" in vias
        assert "cape_of_good_hope" in vias
        assert "suez_canal" in vias


# ── Route Queries ───────────────────────────────────────────────────


class TestGetRoutes:
    def test_usgc_to_korea(self, graph):
        routes = get_routes(graph, "sabine_pass", "incheon")
        assert len(routes) == 3

    def test_qatar_to_korea(self, graph):
        routes = get_routes(graph, "ras_laffan", "incheon")
        assert len(routes) == 1
        assert routes[0].via == "hormuz_strait"
        assert routes[0].transit_days == 15

    def test_australia_to_japan(self, graph):
        routes = get_routes(graph, "northwest_shelf", "futtsu")
        assert len(routes) == 1
        assert routes[0].via == "direct"
        assert routes[0].toll_usd == 0

    def test_nonexistent_route(self, graph):
        routes = get_routes(graph, "incheon", "sabine_pass")  # no reverse route
        assert len(routes) == 0

    def test_nonexistent_node(self, graph):
        routes = get_routes(graph, "nonexistent", "incheon")
        assert len(routes) == 0

    def test_get_all_routes(self, graph):
        routes = get_all_routes(graph)
        assert len(routes) == 12

    def test_route_dataclass_fields(self, graph):
        routes = get_routes(graph, "ras_laffan", "dapeng")
        assert len(routes) == 1
        r = routes[0]
        assert r.route_id == "qatar_china_direct"
        assert r.origin == "ras_laffan"
        assert r.destination == "dapeng"
        assert r.distance_nm == 5600
        assert r.bog_rate == 0.001
        assert r.capacity_constraint == "hormuz_strait"


# ── Bottleneck Disruption ───────────────────────────────────────────


class TestDisableBottleneck:
    def test_disable_panama(self, graph):
        """DEVPLAN: Disable Panama → US Gulf to Asia only has Cape and Suez."""
        g2 = disable_bottleneck(graph, "panama_canal")

        routes = get_feasible_routes(g2, "sabine_pass", "incheon")
        assert len(routes) == 2
        vias = {r.via for r in routes}
        assert vias == {"cape_of_good_hope", "suez_canal"}

    def test_disable_hormuz(self, graph):
        """DEVPLAN: Disable Hormuz → Qatar to Asia routes all severed."""
        g2 = disable_bottleneck(graph, "hormuz_strait")

        # Qatar to Korea
        assert len(get_feasible_routes(g2, "ras_laffan", "incheon")) == 0
        # Qatar to Japan
        assert len(get_feasible_routes(g2, "ras_laffan", "futtsu")) == 0
        # Qatar to China
        assert len(get_feasible_routes(g2, "ras_laffan", "dapeng")) == 0

    def test_disable_both(self, graph):
        """DEVPLAN: Disable both → verify graph connectivity."""
        g2 = disable_bottleneck(graph, "panama_canal")
        g3 = disable_bottleneck(g2, "hormuz_strait")

        # US Gulf to Asia: only Cape and Suez minus Suez? No — Suez is separate.
        # Panama gone, so 2 remain (Cape + Suez)
        usgc_routes = get_feasible_routes(g3, "sabine_pass", "incheon")
        # Suez has capacity_constraint="suez_canal", not "panama_canal" or "hormuz"
        assert len(usgc_routes) == 2

        # Qatar routes: all gone
        assert len(get_feasible_routes(g3, "ras_laffan", "incheon")) == 0

        # Australia and SE Asia routes: unaffected
        assert len(get_feasible_routes(g3, "northwest_shelf", "futtsu")) == 1
        assert len(get_feasible_routes(g3, "bintulu", "incheon")) == 1

    def test_original_graph_unchanged(self, graph):
        """disable_bottleneck should not mutate the original graph."""
        original_edge_count = graph.number_of_edges()
        _ = disable_bottleneck(graph, "hormuz_strait")
        assert graph.number_of_edges() == original_edge_count

    def test_disable_nonexistent_bottleneck(self, graph):
        """Disabling a non-existent bottleneck should return identical graph."""
        g2 = disable_bottleneck(graph, "nonexistent_chokepoint")
        assert g2.number_of_edges() == graph.number_of_edges()


# ── Bottleneck Queries ──────────────────────────────────────────────


class TestRoutesThoughBottleneck:
    def test_panama_routes(self, graph):
        routes = get_routes_through_bottleneck(graph, "panama_canal")
        assert len(routes) == 1
        assert routes[0].route_id == "usgc_asia_panama"

    def test_hormuz_routes(self, graph):
        routes = get_routes_through_bottleneck(graph, "hormuz_strait")
        assert len(routes) == 3  # qatar → korea, japan, china

    def test_suez_routes(self, graph):
        routes = get_routes_through_bottleneck(graph, "suez_canal")
        assert len(routes) == 1
        assert routes[0].route_id == "usgc_asia_suez"


# ── Capacity Updates ────────────────────────────────────────────────


class TestUpdateCapacity:
    def test_capacity_degradation(self, graph):
        """Panama drought scenario: capacity drops but routes remain."""
        timeline = {"2023-12": 22, "2024-03": 27}
        g2 = update_capacity(graph, "panama_canal", timeline, "2023-12")

        routes = get_routes(g2, "sabine_pass", "incheon")
        panama = [r for r in routes if r.via == "panama_canal"]
        assert len(panama) == 1  # route still exists

        # Check capacity attribute was set
        for u, v, key, data in g2.edges(keys=True, data=True):
            if data.get("capacity_constraint") == "panama_canal":
                assert data["current_capacity"] == 22

    def test_capacity_zero_removes_edges(self, graph):
        """Hormuz closure: capacity=0 should remove all Hormuz edges."""
        timeline = {"2026-02": 999, "2026-03": 0}
        g2 = update_capacity(graph, "hormuz_strait", timeline, "2026-03")

        assert len(get_routes_through_bottleneck(g2, "hormuz_strait")) == 0
        assert len(get_routes(g2, "ras_laffan", "incheon")) == 0

    def test_capacity_missing_month_no_change(self, graph):
        """If month not in timeline, graph should be unchanged."""
        timeline = {"2023-12": 22}
        g2 = update_capacity(graph, "panama_canal", timeline, "2024-06")
        assert g2.number_of_edges() == graph.number_of_edges()

    def test_original_unchanged(self, graph):
        """update_capacity should not mutate the original graph."""
        timeline = {"2026-03": 0}
        _ = update_capacity(graph, "hormuz_strait", timeline, "2026-03")
        assert len(get_routes_through_bottleneck(graph, "hormuz_strait")) == 3
