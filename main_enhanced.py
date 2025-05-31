#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
from graph_utils import Graph
from traffic_simulation import adjust_for_traffic
from typing import List, Tuple, Optional
import csv
import heapq
import matplotlib.pyplot as plt
import networkx as nx


# ==========================
# ==========================
def build_graph(filename):
    """
    Builds a Graph instance using the data from the file that is passed in, which contains data in the format in each line:
    start label, end label, travel distance, travel time, and traffic level.

    Parameters
    ----------
    filename : str which is the name of the file
    
    Returns
    -------
    Graph instance
    """     
    graph = Graph()
    with open(filename) as f:
        next(f)
        for line in f:
            u, v, d, t, tr = line.strip().split(',')
            graph.add_directed_edge(u, v, float(d), float(t), traffic=tr)
    return graph


# ==========================
# ==========================
def is_route_possible(graph, start_label, end_label):
    """
    Verifies if there exists a route from a starting location/vertex to an end location/vertex.

    Parameters
    ----------
    graph : Graph instance
    start_label: str which is the starting or "from" vertex
    end_label: str which is the ending or "to" vertex
    
    Returns
    -------
    bool
    """      
    visited = set()
    stack = [start_label]
    while stack:
        current_label = stack.pop()
        if current_label == end_label:
            return True
        if current_label not in visited:
            visited.add(current_label)
            stack.extend(edge.to.label for edge in graph.get_neighbors(current_label))
    return False

# ==========================
# ==========================
def find_shortest_path(graph, start_label, end_label):
    """
    Finds the shortest path between two given vertices provided that the two vertices exist in the graph, by implementing
    Dijkstra's shortest path algorithm.

    Parameters
    ----------
    graph : Graph instance containing vertices and edges
    start_label: str which is the starting or "from" vertex
    end_label: str which is the ending or "to" vertex
    
    Returns
    -------
    Tuple containing the shortest path, which is a list of strings and the distance, which is a float.
    -path list: a list of the labels of the vertices that represent the shortest path from the starting and ending vertices. Returns None if a path doesn't exist containing the start and end vertices.
    dist: a float that represents the distance of the shortest path. Returns float 'inf' if the path doesn't exist.
    """      
    if start_label not in graph.get_nodes() or end_label not in graph.get_nodes():
        return None, float("inf")

    dists = {v: float("inf") for v in graph.get_nodes()} # get_nodes() -> list(vertices.keys())
    prev = {v: None for v in graph.get_nodes()}
    dists[start_label] = 0
    visited = set()
    queue = [(0, start_label)]

    while queue:
        curr_dist, curr_v = heapq.heappop(queue)
        if curr_v == end_label:
            break

        if curr_v not in visited:
            visited.add(curr_v)
            # Edge(self, to, distiance, travel_time=None, traffic=None, time_of_day=None)
            for edge in graph.get_neighbors(curr_v): # adjacency_list.get(curr_v, [])-> Edge object:
                to_v = edge.to.label
                alt_dist = curr_dist + edge.distance
                curr_travel_time = edge.adjusted_travel_time()
                if alt_dist < dists[to_v]:
                    dists[to_v] = alt_dist
                    prev[to_v] = curr_v
                    heapq.heappush(queue, (alt_dist, to_v))

    if dists[end_label] == float("inf"):
            return None, float("inf")

    path = []
    current = end_label
    while current:
          path.append(current)
          current = prev[current]
    return list(reversed(path)), dists[end_label]

# ==========================
# ==========================
def find_least_cost_path(graph, start_label, end_label):
    """
    Finds the path with the lowest cost between two given vertices provided that the two vertices exist in the graph, by implementing
    Dijkstra's shortest path algorithm.

    Parameters
    ----------
    graph : Graph instance containing vertices and edges
    start_label: str which is the starting or "from" vertex
    end_label: str which is the ending or "to" vertex
    
    Returns
    -------
    Tuple containing the path with the lowest cost (list of strings), costs (list of floats), and total time of travel (list of floats).
    -path list: a list of the labels of the vertices that represent the shortest path from the starting and ending vertices. Returns None if a path doesn't exist containing the start and end vertices.
    cost: A list of floats that represents the lowest cost of travel from the starting vertex all other verticed. Returns float 'inf' if the path doesn't exist.
    -travel_times: A list of floats that represents the travel time for the lowest cost path from the starting vertex to all other vertices. Returns float 'inf' if the path doesn't exist.
    """      
    if start_label not in graph.get_nodes() or end_label not in graph.get_nodes():
        return None, float("inf"), float("inf") # Return None, inf cost, inf time

    costs = {v: float("inf") for v in graph.get_nodes()} # get_nodes() -> list(vertices.keys())
    travel_times = {v: float("inf") for v in graph.get_nodes()}
    prev = {v: None for v in graph.get_nodes()}
    costs[start_label] = 0
    travel_times[start_label] = 0
    visited = set()
    # Priority queue stores (cumulative_cost, cumulative_time, vertex_label)
    queue = [(0, 0, start_label)]

    while queue:
        curr_cost, curr_time, curr_v = heapq.heappop(queue)
        if curr_v == end_label:
            break

        if curr_v not in visited:
            visited.add(curr_v)
            # Edge(self, to, distance, travel_time=None, traffic=None, time_of_day=None)
            for edge in graph.get_neighbors(curr_v): # adjacency_list.get(curr_v, [])-> Edge object:
                to_v = edge.to.label
                alt_cost = curr_cost + edge.current_weight()
                alt_time = curr_time + edge.adjusted_travel_time() # Calculate cumulative time
                
                # If the new path has a lower cost, update and push to queue
                if alt_cost < costs[to_v]:
                    costs[to_v] = alt_cost
                    travel_times[to_v] = alt_time # Update travel time
                    prev[to_v] = curr_v
                    heapq.heappush(queue, (alt_cost, alt_time, to_v))
                # If the costs are equal, you might want a tie-breaking rule
                # For example, prioritize lower time if costs are the same:
                elif alt_cost == costs[to_v] and alt_time < travel_times[to_v]:
                    travel_times[to_v] = alt_time # Update travel time
                    prev[to_v] = curr_v
                    heapq.heappush(queue, (alt_cost, alt_time, to_v))


    if costs[end_label] == float("inf"):
            return None, float("inf"), float("inf") # Return None, inf cost, inf time

    path = []
    current = end_label
    while current:
          path.append(current)
          current = prev[current]
    return list(reversed(path)), costs[end_label], travel_times[end_label] # Return path, total cost, total time

# ===============================
# ===============================
def plan_delivery(graph, depot_label, delivery_labels):
    """
    Finds the shortest path that contains all vertices/locations from a starting vertex/depot and a list of delivery locations that are to be visited.

    Parameters
    ----------
    graph : Graph instance
    depot_label: str which is the starting or "from" vertex
    delivery_labels: list of str which contains the labels of all the vertices that are to be visited
    
    Returns
    -------
    A tuple of plans and total_distance.
    -plans, a list of tuples in the form (from_label, to_label, path, distance)
    -total_distance, a float which represents the total distance traveled for all delivery locations rounded to
    two decimal places
    """     
    plans = []
    total_distance = 0
    curr_label = depot_label
    for dest_label in delivery_labels:
        if not is_route_possible(graph, curr_label, dest_label):
            plans.append((curr_label, dest_label, None, 0))
        else:
            path, distance = find_shortest_path(graph, curr_label, dest_label)
            plans.append((curr_label, dest_label, path, distance))
            total_distance += distance
        curr_label = dest_label
    return plans, round(total_distance, 2)

# ===============================
# ===============================
def plan_least_cost_delivery(graph, depot_label, delivery_labels):
    """
    Finds the path with the lowest cost that contains all vertices/locations from a starting vertex/depot and a list of delivery locations that are to be visited.

    Parameters
    ----------
    graph : Graph instance
    depot_label: str which is the starting or "from" vertex
    delivery_labels: list of str which contains the labels of all the vertices that are to be visited
    
    Returns
    -------
    A tuple of plans, total cost, total travel time, and overall average speed.
    -plans, a list of tuples in the form (from_label, to_label, path, distance)
    -total_cost, a float which represents the total cost of travel for the lowest cost path that visits all delivery locations rounded to
    two decimal places
    -total_travel_time, a float that represents the total travel time for the lowest cost path that visits all delivery locations rounded to
    two decimal places
    -overall_avg_speed, a float represents the overall average speed for the lowest cost path that visits all delivery locations rounded to
    two decimal places, which is calculated by total_cost/total_travel_time
    """     
    plans = []
    total_cost = 0
    total_travel_time = 0 # Initialize total travel time
    curr_label = depot_label

    for dest_label in delivery_labels:
        if not is_route_possible(graph, curr_label, dest_label):
            plans.append((curr_label, dest_label, None, 0, 0)) # Add 0 for time

        else:
            path, cost, travel_time = find_least_cost_path(graph, curr_label, dest_label)  # Get segment cost, travel_time
            plans.append((curr_label, dest_label, path, cost, travel_time))
            total_cost += cost
            total_travel_time += travel_time # Update total travel time

# Calculate overall average speed
    overall_distance = sum(plan[3] for plan in plans if plan[3] is not None) # Sum of costs (which are sums of distance/time)
    # This might not be the total physical distance. If you need total physical distance,
    # you would need to track distance separately in find_leastcost_path as well.
    # Let's assume for now you want the overall "ML/min" metric based on total cost and total time.

    overall_avg_speed = total_cost / total_travel_time if total_travel_time > 0 else float('inf')

    return plans, round(total_cost, 2), round(total_travel_time, 2), round(overall_avg_speed, 2) # Return total time and overall avg speed


# ===============================
# main()
# ===============================
def main():
    filename = "sample_input.csv"
    graph = build_graph(filename)
    print(graph.get_nodes())

    print("\nWelcome to Smart Delivery Planner!")
    time_of_day = input("\nEnter the time of day: ").lower()
    adjust_for_traffic(graph, time_of_day)
    depot = input("\nEnter depot location: ").strip()
    deliveries = input("Enter delivery stops (comma separated): ").strip().split(',')
    print("\nChecking delivery feasibility:")
    for dest in deliveries:
        if is_route_possible(graph, depot, dest):
            print(f"  {depot} → {dest}: Route exists.")
        else:
            print(f"  {depot} → {dest}: No route")

    print("\nFinding the shortest route...")
    for dest in deliveries:
        if is_route_possible(graph, depot, dest):
            path, distance = find_shortest_path(graph, depot, dest)
            if path:
                print(f"  {depot} → {dest}: {' -> '.join(path)} | {distance:.2f} ML")
            else:
                print(f"  {depot} → {dest}: No Path Found")

    print("\nFinding the least cost route...")
    for dest in deliveries:
        if is_route_possible(graph, depot, dest):
            path, cost, travel_time = find_least_cost_path(graph, depot, dest)
            if path:
                print(f"  {depot} → {dest}: {' -> '.join(path)} | {cost:.2f} ML/min | {travel_time:.2f} min")
            else:
                print(f"  {depot} → {dest}: No Path Found")


    print("\nStatic Delivery plan:")
    plans, total_distance = plan_delivery(graph, depot, deliveries)
    for i, (src, dest, path, dist) in enumerate(plans):
        if path:
            print(f"  {i+1}. {src} → {dest} ({dist:.2f} ML)")
        else:
            print(f"  {i+1}. {src} → {dest}: No Route")
    print(f"Total distance: {total_distance:.2f} ML")


    print("\nLeast Cost Delivery plan:")
    plans, total_cost, total_travel_time, overall_avg_speed = plan_least_cost_delivery(graph, depot, deliveries) # Get total time and overall speed
    for i, (src, dest, path, segment_cost, segment_time) in enumerate(plans): # Get segment time
        if path:
            print(f"  {i+1}. {src} → {dest} (Cost: {segment_cost:.2f} ML/min, Time: {segment_time:.2f} min)") # Print segment cost and time
        else:
            print(f"  {i+1}. {src} → {dest}: No Route")
    print(f"Total cost: {total_cost:.2f} ML/min")
    print(f"Total travel time: {total_travel_time:.2f} min")
    print(f"Overall average speed: {overall_avg_speed:.2f} ML/min")

if __name__ == "__main__":
    main()
