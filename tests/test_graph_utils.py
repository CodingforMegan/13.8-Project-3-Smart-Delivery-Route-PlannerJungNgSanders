"""
Unit tests for the graph_utils.py module
"""

import pytest

from graph_utils import Edge, Graph, Vertex

@pytest.fixture
def test_graph():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_vertex("E")
    graph.add_directed_edge("A", "B", 5, 10, "moderate")
    graph.add_directed_edge("B", "C", 3, 6, "light")
    graph.add_directed_edge("C", "A", 4, 8, "heavy")
    graph.add_undirected_edge("A", "E", 10, 10, "moderate")
    return graph

@pytest.fixture
def test_vertex():
    vertex = Vertex(label="A", lat=10, lon=10)
    return vertex

def test_default_vertex_initialization():
    vertex = Vertex("A")
    assert vertex.label == "A"
    assert vertex.lat is None
    assert vertex.lon is None
    assert not vertex.neighbors

def test_nondefault_vertex_initialization(test_vertex):
    assert test_vertex.label == "A"
    assert test_vertex.lat == 10
    assert test_vertex.lon == 10
    assert not test_vertex.neighbors

def test_vertex_add_neighbor():
    vertex_a = Vertex("A")
    vertex_b = Vertex("B")
    edge = Edge(to=vertex_b, distance=10, travel_time=10)
    vertex_a.add_neighbor(vertex_b, edge)
    assert vertex_a.neighbors
    assert vertex_a.neighbors[vertex_b] == edge

def test_vertex_representation(test_vertex):
    assert str(test_vertex) == "Vertex(A, lat=10, lon=10)"

def test_vertex_comparison(test_vertex):
    vertex_b = Vertex("B")
    assert test_vertex < vertex_b

def test_edge_default_initialization(test_vertex):
    edge = Edge(test_vertex, 10, 10)
    assert edge.to == test_vertex
    assert edge.distance == 10
    assert edge.base_travel_time == 10
    assert edge.traffic is None
    assert edge.time_of_day is None

def test_edge_nondefault_initialization(test_vertex):
    edge = Edge(test_vertex, distance=10, travel_time=10, traffic="High", time_of_day="Morning")
    assert edge.to == test_vertex
    assert edge.distance == 10
    assert edge.base_travel_time == 10
    assert edge.traffic == "High"
    assert edge.time_of_day == "Morning"

def test_edge_adjusted_travel_time(test_vertex):
    edge = Edge(test_vertex, distance=10, travel_time=10, traffic="High", time_of_day="Morning")
    assert edge.adjusted_travel_time() == 12.5

def test_edge_current_weight(test_vertex):
    edge = Edge(test_vertex, distance=10, travel_time=10, traffic="High", time_of_day="Morning")
    assert edge.current_weight() == 0.8

def test_edge_representation(test_vertex):
    edge = Edge(test_vertex, distance=10, travel_time=10, traffic="High", time_of_day="Morning")
    assert str(edge) == f"---> A (distance=10, base_time=10, traffic=High)"

def test_graph_default_initialization():
    graph = Graph()
    assert not graph.adjacency_list
    assert not graph.vertices
    assert not graph.edges

def test_graph_nondefault_initialization(test_graph):
    assert len(test_graph.adjacency_list) == 5
    assert len(test_graph.adjacency_list["A"]) == 2
    assert len(test_graph.adjacency_list["D"]) == 0
    assert len(test_graph.adjacency_list["E"]) == 1

def test_graph_get_vertex(test_graph):
    found_vertex = test_graph.get_vertex("A")
    assert isinstance(found_vertex, Vertex)
    assert found_vertex.label == "A"
    assert found_vertex.lat is None
    assert found_vertex.lon is None

def test_graph_add_directed_edge(test_graph):
    test_graph.add_directed_edge("A", "D", 10, 5, traffic="moderate")
    # Ensure that the adjacency list for "A" has increased by one and that "D" is still zero
    assert len(test_graph.adjacency_list["A"]) == 3
    assert len(test_graph.adjacency_list["D"]) == 0

def test_graph_add_undirected_edge(test_graph):
    test_graph.add_undirected_edge("A", "D", 10, 5, traffic="moderate")
    # Ensure that the adjacency list for "A" has increased by one and that "D" has increased by one
    assert len(test_graph.adjacency_list["A"]) == 3
    assert len(test_graph.adjacency_list["D"]) == 1

def test_graph_get_edge(test_graph):
    found_edge_weight = test_graph.get_edge("A", "B")
    assert found_edge_weight == 0.5
    assert isinstance(found_edge_weight, float)

def test_graph_update_edge(test_graph):
    assert test_graph.get_edge("A", "B") == 0.5
    test_graph.update_edge("A", "B", key="base_travel_time", value=5)

def test_graph_get_neighbors(test_graph):
    assert len(test_graph.get_neighbors("A")) == 2

def test_graph_get_nodes(test_graph):
    assert test_graph.get_nodes() == ["A", "B", "C", "D", "E"]


