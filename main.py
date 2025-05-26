#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
from graph_utils import Graph
from traffic_simulation import adjust_for_traffic
from typing import Optional, List
import csv
import heapq


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


def main():
    # Prepare sample input
    graph_data = [
        {'from_vertex': 'A', 'to_vertex': 'B', 'distance': 5, 'travel_time': 10, 'traffic': 'moderate'},
        {'from_vertex': 'A', 'to_vertex': 'D', 'distance': 10, 'travel_time': 15, 'traffic': 'low'},
        {'from_vertex': 'B', 'to_vertex': 'C', 'distance': 3, 'travel_time': 6, 'traffic': 'light'},
        {'from_vertex': 'C', 'to_vertex': 'D', 'distance': 4, 'travel_time': 8, 'traffic': 'heavy'},
        {'from_vertex': 'D', 'to_vertex': 'E', 'distance': 2, 'travel_time': 4, 'traffic': 'high'}
    ]

    input_file = 'sample_input.csv'
    with open(input_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['from_vertex', 'to_vertex', 'distance', 'travel_time', 'traffic'])
        writer.writeheader()
        writer.writerows(graph_data)
   
    filename = "sample_input.csv"
    # Build graph and apply traffic
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
    print("\\nChecking route feasibility:")
    for dest in deliveries:
        possible = is_route_possible(graph, depot, dest)
        print(f"  {depot} → {dest}: {'Possible' if possible else 'No Route'}")


    # 2. Test find_shortest_path()
    print("\\nFinding shortest paths:")
    for dest in deliveries:
        path = find_shortest_path(graph, depot, dest)
        if path:
            print(f"  {depot} → {dest}: {' -> '.join(path)}")
        else:
            print(f"  {depot} → {dest}: No Path Found")


    # 3. Use plan_delivery() to generate batch delivery plan
    print("\\nDelivery Plan Summary:")
    plans = plan_delivery(graph, depot, deliveries)
    for dest, path in plans:
        if path:
            print(f"  Delivery to {dest}: {' -> '.join(path)}")
        else:
            print(f"  Delivery to {dest}: No Route")


if __name__ == "__main__":
    main()

