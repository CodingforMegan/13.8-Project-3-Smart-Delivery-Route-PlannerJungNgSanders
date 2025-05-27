#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
from graph_utils import Graph
from traffic_simulation import adjust_for_traffic
from typing import Optional, List, Tuple
import csv
import heapq
import matplotlib.pyplot as plt
import networkx as nx



def build_graph(filename):
    graph = Graph()
    with open(filename) as f:
        next(f)  # Skip header
        for line in f:
            from_vertex, to_vertex, distance, travel_time, traffic = line.strip().split(',')
            graph.add_directed_edge(from_vertex, to_vertex, float(distance), float(travel_time), traffic=traffic)
    return graph


def is_route_possible(graph, start: str, end: str) -> bool:
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node == end:
            return True
        if node not in visited:
            visited.add(node)
            stack.extend(edge.to.label for edge in graph.get_neighbors(node))
    return False


def find_shortest_path(graph, start: str, end: str) -> Optional[List[str]]:
    if start not in graph.get_nodes() or end not in graph.get_nodes():
        return None

    dist = {node: float("inf") for node in graph.get_nodes()}
    prev = {node: None for node in graph.get_nodes()}
    dist[start] = 0
    queue = [(0, start)]

    while queue:
        curr_dist, u = heapq.heappop(queue)
        if u == end:
            break
        for edge in graph.get_neighbors(u):
            v = edge.to.label
            weight = edge.adjusted_travel_time()
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(queue, (dist[v], v))

    if dist[end] == float("inf"):
        return None

    path = []
    node = end
    while node:
        path.append(node)
        node = prev[node]
    return list(reversed(path))


def plan_delivery(graph, depot: str, deliveries: List[str]) -> List[Tuple[str, Optional[List[str]]]]:
    plans = []
    for dest in deliveries:
        path = find_shortest_path(graph, depot, dest)
        plans.append((dest, path))
    return plans


#  visualize Smart Delivery Route with importing 
#  networkx & matplotlib.pyplot modules
# =========================================================
# =========================================================
def visualize_routes(graph, plans):
    G = nx.DiGraph()

    # Add all nodes
    for node in graph.get_nodes():
        G.add_node(node)

    # Add all edges with adjusted travel time as weight
    for u in graph.get_nodes():
        for edge in graph.get_neighbors(u):
            G.add_edge(u, edge.to.label, weight=edge.adjusted_travel_time())

    pos = nx.spring_layout(G, seed=42)

    # Draw full graph in light gray
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='gray', node_size=800)

    # Highlight selected delivery routes
    route_edges = []
    for _, path in plans:
        if path and len(path) > 1:
            route_edges += [(path[i], path[i+1]) for i in range(len(path)-1)]

    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='red', width=2)

    labels = nx.get_edge_attributes(G, 'weight')
    labels = {k: f"{v:.1f}" for k, v in labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Smart Delivery Routes with Traffic-Aware Weights")
    plt.tight_layout()
    plt.show()


# =======================================
# usage demo
# ========================================
def main():
    # Build graph and apply traffic   
    filename = "sample_input.csv"
    graph = build_graph(filename)

    
    # Adjust graph edge weights for time-of-day traffic    
    time_of_day = "morning"
    adjust_for_traffic(graph, time_of_day)


    depot = "A"
    deliveries = ["B", "C", "D", "E", "X"]  # X is unreachable

    print(f"--- Smart Delivery Planner ---")
    print(f"Depot: {depot}")
    print(f"Time of Day: {time_of_day}\n")   

    print("Edge Weights After Traffic Adjustment:")
    for u in graph.get_nodes():
        for edge in graph.get_neighbors(u):
            print(f"  {u} → {edge.to.label} | Distance: {edge.distance} | "
                  f"Adjusted Time: {edge.adjusted_travel_time():.2f} | "
                  f"Efficiency (dist/time): {edge.current_weight():.2f}")

    # 1. Test is_route_possible()
    print("\nChecking route feasibility:")
    for dest in deliveries:
        possible = is_route_possible(graph, depot, dest)
        print(f"  {depot} → {dest}: {'Possible' if possible else 'No Route'}")


    # 2. Test find_shortest_path()
    print("\nFinding shortest paths:")
    for dest in deliveries:
        path = find_shortest_path(graph, depot, dest)
        if path:
            print(f"  {depot} → {dest}: {' -> '.join(path)}")
        else:
            print(f"  {depot} → {dest}: No Path Found")


    # 3. Use plan_delivery() to generate batch delivery plan
    print("\nDelivery Plan Summary:")
    plans = plan_delivery(graph, depot, deliveries)
    for dest, path in plans:
        if path:
            print(f"  Delivery to {dest}: {' -> '.join(path)}")
        else:
            print(f"  Delivery to {dest}: No Route")

    # 4. call visualize_routes
    visualize_routes(graph, plans)


if __name__ == "__main__":
    main()

