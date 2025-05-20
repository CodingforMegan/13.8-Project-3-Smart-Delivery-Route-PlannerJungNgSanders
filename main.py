#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
from graph_utils import Vertex
from graph_utils import Edge
from graph_utils import Graph
import heapq


def main():
    pass


def build_graph(filename):
    graph = GraphWithVertices()
    with open(filename) as f:
        next(f)
        for line in f:
            from_vertex, toward_vertex, distance, travel_time, traffic = line.strip().split(',')
            graph.add_directed_edge(u, v, float(distance), float(travel_time), traffic=traffic)
    return graph

def build_graph(filename):
    pass

def is_route_possible(graph, start, end):
    pass
  
def find_shortest_path(graph, start, end):
    pass

def plan_delivery(graph, depot, deliveries):
    pass

def adjust_for_traffic(graph, time_of_day):
    pass


if __name__ == "__main()__":
    main()
