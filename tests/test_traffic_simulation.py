"""
Unit tests for the traffic_simulation.py module
"""

import pytest

from graph_utils import Graph
from traffic_simulation import adjust_for_traffic, get_traffic_multiplier

@pytest.fixture
def test_graph():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_directed_edge("A", "B", 5, 10, "moderate")
    graph.add_directed_edge("B", "C", 3, 6, "light")
    graph.add_directed_edge("C", "A", 4, 8, "heavy")
    return graph

@pytest.mark.parametrize(
    "level, multiplier",
    (("HEAVY", 1.5),
     ("high", 1.25),
     ("MODERATE",1.0),
     ("light", 0.8),
     ("LOW", 0.75))
)
def test_expected_traffic_multiplier(level, multiplier):
    assert get_traffic_multiplier(level) == multiplier

def test_unexpected_traffic_multiplier():
    assert get_traffic_multiplier("ok") == 1.0

def test_incorrect_traffic_multiplier_type():
    with pytest.raises(ValueError):
        get_traffic_multiplier(1.0)

@pytest.mark.parametrize("time_of_day,expected_level", [
    ("morning", "heavy"),
    ("late_morning", "high"),
    ("afternoon", "moderate"),
    ("evening", "light"),
    ("night", "low"),
    ("unknown", "moderate"),
])
def test_adjust_for_traffic_sets_correct_level(test_graph, time_of_day, expected_level):
    adjust_for_traffic(test_graph, time_of_day)
    traffic_levels = []
    for label in test_graph.get_nodes():
        for edge in test_graph.get_neighbors(label):
            traffic_levels.append(edge.traffic)
    assert all(level == expected_level for level in traffic_levels), (
        f"All edges should be set to {expected_level} for {time_of_day}"
    )