"""
Unit tests for the main.py module.
"""
import pytest
from graph_utils import Graph
from main import build_graph, is_route_possible, find_shortest_path, plan_delivery

def test_build_graph(tmp_path):
    content = (
        "from_vertex,to_vertex,distance,travel_time,traffic\n"
        "X,Y,10,2,heavy\n"
        "Y,Z,5,1,light\n"
    )
    file = tmp_path / "test.csv"
    file.write_text(content)
    graph = build_graph(str(file))
    assert isinstance(graph, Graph)
    nodes = set(graph.get_nodes())
    assert nodes == {"X", "Y", "Z"}
    assert graph.get_edge("X", "Y") == pytest.approx(3.33, rel=1e-2)
    assert graph.get_edge("Y", "Z") == pytest.approx(6.25, rel=1e-2)

def test_is_route_possible():
    g = Graph()
    g.add_directed_edge("A", "B", 1, 1, "moderate")
    g.add_directed_edge("B", "C", 1, 1, "moderate")
    assert is_route_possible(g, "A", "C")
    assert not is_route_possible(g, "C", "A")
    assert not is_route_possible(g, "X", "Y")

def test_find_shortest_path_nonexistent_nodes():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    shortest_path = find_shortest_path(g, "X", "Y")
    assert shortest_path[0] is None
    assert shortest_path[1] == float("inf")
    #assert find_shortest_path(g, "X", "Y") is None

def test_find_shortest_path_unreachable():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    path, distance = find_shortest_path(g, "A", "B")
    assert path is None
    assert distance == float("inf")

def test_find_shortest_path_basic():
    g = Graph()
    g.add_directed_edge("A", "B", 4, 2, "moderate")
    g.add_directed_edge("B", "C", 6, 3, "moderate")
    path, distance = find_shortest_path(g, "A", "C")
    assert path == ["A", "B", "C"]
    assert distance == pytest.approx(10)

def test_plan_delivery_simple():
    g = Graph()
    g.add_directed_edge("A", "B", 4, 2, "moderate")
    g.add_directed_edge("B", "C", 6, 3, "moderate")
    plans, total_distance = plan_delivery(g, "A", ["B", "C"] )
    assert len(plans) == 2
    src, dest, path, dist = plans[0]
    assert src == "A"
    assert dest == "B"
    assert path == ["A", "B"]
    assert dist == pytest.approx(4)
    src, dest, path, dist = plans[1]
    assert src == "B"
    assert dest == "C"
    assert path == ["B", "C"]
    assert dist == pytest.approx(6)
    assert total_distance == pytest.approx(10)

def test_plan_delivery_with_unreachable():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    plans, total_distance = plan_delivery(g, "A", ["B"] )
    assert plans == [("A", "B", None, 0)]
    assert total_distance == 0
