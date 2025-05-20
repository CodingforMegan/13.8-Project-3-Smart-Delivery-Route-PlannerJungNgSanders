#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
from graph_utils import Vertex
from graph_utils import Edge
from graph_utils import Graph
import heapq


def main():
    filename = "sample_input.csv"
    graph = build_graph(filename)
    
    depot = "A"
    deliveries = ["B", "C", "D", "E", "X"]  # 'X' is an unreachable point for testing

    print(f"Planning deliveries from depot: {depot}\n")

# more implementations to call functions


def build_graph(filename):
    graph = GraphWithVertices()
    with open(filename) as f:
        next(f)
        for line in f:
            from_vertex, toward_vertex, distance, travel_time, traffic = line.strip().split(',')
            graph.add_directed_edge(u, v, float(distance), float(travel_time), traffic=traffic)
    return graph


def is_route_possible(graph, start, end):
    pass
  
def find_shortest_path(graph, start, end):
    pass

def plan_delivery(graph, depot, deliveries):
    pass

# Not sure if this method should be implemented here or in traffic_simulation.py
def adjust_for_traffic(graph, time_of_day):
    pass


if __name__ == "__main()__":
    main()
