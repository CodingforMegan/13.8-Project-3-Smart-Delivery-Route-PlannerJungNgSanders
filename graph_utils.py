#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------

import heapq

class Vertex:
    def __init__(self, label, latitude=None, longitude=None, attributes=None):
        self.label = label
        self.lat = latitude
        self.lon = longitude
        self.attributes = attributes or {}

    def __repr__(self):
        return f"Vertex(label={self.label}, lat={self.lat}, lon={self.lon})"


class Edge:
    def __init__(self, to, distance, travel_time, traffic=None, time_of_day=None):
        self.to = to
        self.distance = distance
        self.base_travel_time = travel_time  # static reference
        self.traffic = traffic
        self.time_of_day = time_of_day

        # avoid division by zero
        self.base_weight = self.distance / travel_time if travel_time > 0 else float("inf")

    def adjusted_travel_time(self):
        """Return adjusted travel time based on traffic level."""
        traffic_level = (self.traffic or "moderate").lower()

        multiplier = {
            "heavy": 1.5,
            "moderate": 1.0,
            "light": 0.8,
            "high": 1.25,
            "low": 0.75
        }.get(traffic_level, 1.0)

        return self.base_travel_time * multiplier


    def __repr__(self):
        return f"---> {self.to} (distance={self.distance}, base_time={self.base_travel_time}, traffic={self.traffic})"

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.vertices = {}

    def add_vertex(self, vertex):
        self.vertices[vertex.label] = vertex
        self.adjacency_list[vertex.label] = []

    def get_vertex(self, label):
        return self.vertices.get(label)

    def add_directed_edge(self, from_vertex, to_vertex, distance, travel_time, traffic=None, time_of_day=None):
        if from_vertex not in self.vertices:
            self.add_vertex(Vertex(from_vertex))
        if to_vertex not in self.vertices:
            self.add_vertex(Vertex(to_vertex))
        edge = Edge(to_vertex, distance=distance, travel_time=travel_time, traffic=traffic, time_of_day=time_of_day)
        self.adjacency_list[from_vertex].append(edge)

    def add_undirected_edge(self, from_vertex, to_vertex, distance, travel_time, traffic=None, time_of_day=None):
        self.add_directed_edge(from_vertex, to_vertex, distance, travel_time, traffic, time_of_day)
        self.add_directed_edge(to_vertex, from_vertex, distance, travel_time, traffic, time_of_day)

    def get_edge(self, from_vertex, to_vertex):
        for edge in self.adjacency_list.get(from_vertex, []):
            if edge.to == to_vertex:
                return edge
        return None

    def update_edge(self, from_vertex, to_vertex, key, value):
        edge = self.get_edge(from_vertex, to_vertex)
        if edge and hasattr(edge, key):
            setattr(edge, key, value)


if __name__ == "__main__":
    graph = Graph()
    graph.add_vertex(Vertex("A", 40.7128, -74.0060))
    graph.add_vertex(Vertex("B", 34.0522, -118.2437))
    graph.add_directed_edge("A", "B", 100, 60, traffic="heavy")
    graph.add_directed_edge("B", "C", 200, 120, traffic="light")
    print(graph.adjacency_list)
    print()
    print(graph.get_edge("A", "B"))
    print()
    print(graph.update_edge("A", "B", "distance", 50))
    print()
    print(graph.neighbors("A"))
    print()
    print(graph.get_nodes())
    print()
    print(graph.get_vertex("A"))
    print()
    print(graph.get_vertex("C"))
    print()
    print(graph.get_vertex("D"))
    print()
    print(graph.vertices)
