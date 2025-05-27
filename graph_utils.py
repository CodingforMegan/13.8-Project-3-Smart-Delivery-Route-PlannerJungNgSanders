#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
from traffic_simulation import get_traffic_multiplier
from typing import List, Tuple, Optional
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
        self.base_travel_time = travel_time # static reference
        self.traffic = traffic
        self.time_of_day = time_of_day

    def adjusted_travel_time(self):
        multiplier = get_traffic_multiplier(self.traffic)
        return self.base_travel_time * multiplier

    def current_weight(self):
        """Return a dynamic weight: distance / adjusted travel time"""
        adjusted_time = self.adjusted_travel_time()
        if adjusted_time == 0:
            return float("inf")
        return self.distance / adjusted_time  # higher = more efficient

    def __repr__(self):
        return f"---> {self.to.label} (distance={self.distance}, base_time={self.base_travel_time}, traffic={self.traffic})"


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
        new_vertex = Vertex(label, lat, lon)
        self.vertices[label] = new_vertex
        self.adjacency_list[label] = [] # Initialize adjacency list for the new vertex


    def get_vertex(self, label):
        return self.vertices.get(label)


    def add_directed_edge(self, start_label, end_label, distance, travel_time, traffic=None, time_of_day=None):
        if start_label not in self.vertices:
            # Instantiate Vertex class with start_label
            print(f"Vertex {start_label} does not exist. Adding it now.")
            self.add_vertex(start_label)
        if end_label not in self.vertices:
            # Instantiate Vertex class with end_label
            print(f"Vertex {end_label} does not exist. Adding it now.")
            self.add_vertex(end_label)

        # Ensure both vertices exist after potential creation
        try:
            new_edge = Edge(self.vertices[end_label], distance, travel_time, traffic, time_of_day)
            print(f"Adding edge from {start_label} to {end_label} with weight {new_edge.current_weight():.2f}")
            self.adjacency_list[start_label].append(new_edge)
            self.edges[(start_label, end_label)] = round(new_edge.current_weight(), 2)
        except ZeroDivisionError:
            print(f"Warning: Could not add edge from {start_label} to {end_label}. Division by zero.")


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


if __name__ == "__main__":
    graph_data = [
        {'from_vertex': 'A', 'to_vertex': 'B', 'distance': 5, 'travel_time': 10, 'traffic': 'moderate'},
        {'from_vertex': 'A', 'to_vertex': 'D', 'distance': 10, 'travel_time': 15, 'traffic': 'low'},
        {'from_vertex': 'B', 'to_vertex': 'C', 'distance': 3, 'travel_time': 6, 'traffic': 'light'},
        {'from_vertex': 'C', 'to_vertex': 'D', 'distance': 4, 'travel_time': 8, 'traffic': 'heavy'},
        {'from_vertex': 'D', 'to_vertex': 'E', 'distance': 2, 'travel_time': 4, 'traffic': 'high'}
    ]
