#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------

import heapq
import matplotlib.pyplot as plt
import networkx as nx

class Vertex:
    def __init__(self, label, lat=None, lon=None):
        self.label = label
        self.lat = lat
        self.lon = lon
        self.neighbors = {} # {neighbor_vertex: edge}

    def add_neighbor(self, neighbor, edge):
        self.neighbors[neighbor] = edge

    def __lt__(self, other):
        return self.label < other.label

    def __repr__(self):
        return f"Vertex({self.label}, lat={self.lat}, lon={self.lon})"


class Edge:
    def __init__(self, to, distance, travel_time, traffic=None, time_of_day=None):
        self.to = to
        self.distance = distance
        self.base_travel_time = travel_time  # static reference
        self.traffic = traffic
        self.time_of_day = time_of_day

        # avoid division by zero
        try:
            self.base_weight = self.distance / travel_time
        except ZeroDivisionError:
            self.base_weight = float("inf")

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
"""
adjacency_list: key: vertex label, value: lists representing the edges originating from that vertex, for example, ('A': 'B', 'C', 'E')
self.vertices: key: vertex label, value: corresponding Vertex object, for example, ('A': Vertex('A'))
self.edges: key: a tuple (start_label, end_label), value: corresponding edges object, for example, (('A', 'E'): 15)
"""
        self.adjacency_list = {}
        self.vertices = {}
        self.edges = {} 
    
    def add_vertex(self, label, lat=None, lon=None):
        if label in self.vertices:
            raise ValueError(f"Vertex with label {label} already exists.")
        else:
            new_vertex = Vertex(label, lat, lon)
            self.vertices[label] = new_vertex
            self.adjacency_list[label] = [] # Initialize adjacency list for the new vertex

    def get_vertex(self, label):
        return self.vertices.get(label)

    def add_directed_edge(self, start_label, end_label, distance, travel_time, traffic=None, time_of_day=None):
        if start_label not in self.vertices:
            # Instantiate Vertex class with start_label
            self.add_vertex(start_label)
        if end_label not in self.vertices:
            # Instantiate Vertex class with end_label
            self.add_vertex(end_label)

        # Ensure both vertices exist after potential creation
        if start_label in self.vertices and end_label in self.vertices:
            try:
                new_edge = Edge(self.vertices[end_label], distance=distance, travel_time=travel_time, traffic=traffic, time_of_day=time_of_day)
                self.adjacency_list[start_label].append(new_edge)
                self.edges[(start_label, end_label)] = new_edge
            except ZeroDivisionError:
                print(f"Warning: Could not add edge from {start_label} to {end_label} due to zero travel time.")
        else:
            print(f"Warning: Could not add directed edge from {start_label} to {end_label} because one or both vertices could not be found or added.")

    def add_undirected_edge(self, start_label, end_label, distance, travel_time, traffic=None, time_of_day=None):
        self.add_directed_edge(start_label, end_label, distance, travel_time, traffic, time_of_day)
        self.add_directed_edge(end_label, start_label, distance, travel_time, traffic, time_of_day)
    
    def get_edge(self, start_label, end_label):
        return self.edges.get((start_label, end_label))

    def update_edge(self, start_label, end_label, key, value):
        edge = self.get_edge(start_label, end_label)
        if edge: # Check if the edge exists
            if hasattr(edge, key): # Check if the edge object has the specified attribute
                setattr(edge, key, value)
            else:
                print(f"Warning: Edge from {start_label} to {end_label} does not have attribute '{key}'.")
        else:
            print(f"Warning: Edge from {start_label} to {end_label} not found.")

    # Helper method to get neighbors (edges originating from a vertex)
    def get_neighbors(self, vertex_label):
        return self.adjacency_list.get(vertex_label, [])

    # Helper method to get all vertex labels
    def get_nodes(self):
        return list(self.vertices.keys())


'''
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
'''
