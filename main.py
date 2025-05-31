#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
from graph_utils import Graph
from traffic_simulation import adjust_for_traffic
import heapq
import matplotlib.pyplot as plt
import networkx as nx


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
        next(f)  # Skip header
        for line in f:
            from_vertex, to_vertex, distance, travel_time, traffic = line.strip().split(',')
            graph.add_directed_edge(from_vertex, to_vertex, float(distance), float(travel_time), traffic=traffic)
    return graph


# check route for Smart Delivery Planner
# ======================================
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
        if not current_label in visited:
            visited.add(current_label)
            stack.extend(edge.to.label for edge in graph.get_neighbors(current_label))

    return False


# planning most cost-efficiency path for Smart Delivery Planner
# ============================================================
def find_shortest_path(graph, start_label, end_label):
    """
    Finds the shortest path between two given vertices provided that the two vertices exist in the graph, by implementing
    Dijkstra's shortest path algorithm.

    Parameters
    ----------
    graph : Graph instance
    start_label: str which is the starting or "from" vertex
    end_label: str which is the ending or "to" vertex
    
    Returns
    -------
    Tuple containing the shortest path, which is a list of strings and the distance, which is a float.
    path list: a list of the labels of the vertices that represent the shortest path from the starting and ending vertices.
    dist: a float that represents the distance of the shortest path
    """       
    if start_label not in graph.get_nodes() or end_label not in graph.get_nodes():
        return None
    dist = {vertex: float("inf") for vertex in graph.get_nodes()}
    prev = {vertex: None for vertex in graph.get_nodes()}
    dist[start_label] = 0
    queue = [(0, start_label)]

    #print(f"Debug: Starting shortest path from {start} to {end}")
    #print(f"Debug: Inital dist: {dist}")
    #print(f"Debug: Initial queue: {queue}")

    while queue:
        curr_dist, curr_vertex = heapq.heappop(queue)
        #print(f"Debug: Processing vertex: {curr_vertex} with current distance: {curr_dist}")
        if curr_vertex == end_label:
            break
        for edge in graph.get_neighbors(curr_vertex):
            to_vertex = edge.to.label
            curr_weight = edge.adjusted_travel_time()
            #print(f"  Debug: Considering edge to {to_vertex} with weight: {curr_weight}")
            if dist[curr_vertex] + curr_weight < dist[to_vertex]:
                dist[to_vertex] = dist[curr_vertex] + curr_weight
                prev[to_vertex] = curr_vertex
                heapq.heappush(queue, (dist[to_vertex], to_vertex))
                #print(f"  Debug: Updated distance to {to_vertex}: {dist[to_vertex]}")

    #print(f"Debug: Final dist: {dist}")
    #print(f"Debug: Final prev: {prev}")
    if dist[end_label] == float("inf"):
        #print(f"  Debug: No path found from {start} to {end}")
        return None, float("inf") # Return None for path and "inf" for distance if no path
    else:
        path = []
        curr_vertex = end_label
        while curr_vertex:
            path.append(curr_vertex)
            curr_vertex = prev[curr_vertex]
        return list(reversed(path)), dist[end_label] # Return the path and the final distance


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
        # Check if a route is possible before finding the shortest path
        if not is_route_possible(graph, curr_label, dest_label):
            plans.append((curr_label, dest_label, None, 0))
        else:
            # Handle cases where the route is not possible
            path, distance = find_shortest_path(graph, curr_label, dest_label)
            plans.append((curr_label, dest_label, path, distance))
            total_distance += distance
        curr_label = dest_label
    return plans, round(total_distance, 2)


#  visualize Smart Delivery Route with importing 
#  networkx & matplotlib.pyplot modules
# =========================================================
# =========================================================
def visualize_routes(graph, plans):
    """
    Visualizes the Graph instance's edges and vertices and highlights the selected delivery routes of the Smart Delivery Route program.

    Parameters
    ----------
    graph : Graph instance
    plans: list of tuples containing the labels of the vertices that represent the shortest path that includes the starting vertex/depot and all the vertices/delivery locations that
    are to be visited. 
    
    Returns
    -------
    None. This function visualizes a plot from matplotlib to visualize the graph and highlights the selected delivery routes and includes labels for the edge weights, which represent travel times.
    """     
    G = nx.DiGraph()

    # Add all nodes
    for label in graph.get_nodes():
        G.add_node(label)

    # Add all edges with adjusted travel time as weight
    for u in graph.get_nodes():
        for edge in graph.get_neighbors(u):
            G.add_edge(u, edge.to.label, weight=edge.adjusted_travel_time())
   
    pos = nx.spring_layout(G, seed=42)  # consistent layout

    # Draw full graph in light gray
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='gray', node_size=800)

    # Highlight selected delivery routes
    route_edges = []
    for from_label, to_label, path, distance in plans:
        if path and len(path) > 1:
            route_edges += [(path[i], path[i+1]) for i in range(len(path)-1)]
  
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='red', width=2)

    # Change this part to use current_weight()
    labels = nx.get_edge_attributes(G, 'weight') # This still gets the adjusted_travel_time added earlier
    efficiency_labels = {}
    for u in graph.get_nodes():
        for edge in graph.get_neighbors(u):
            efficiency_labels[(u, edge.to.label)] = edge.current_weight()

    efficiency_labels = {k: f"{v:.2f}" for k, v in efficiency_labels.items()} # Use .2f for efficiency
    nx.draw_networkx_edge_labels(G, pos, edge_labels=efficiency_labels)

    plt.title("Smart Delivery Routes with Cost-Efficiency Weights") # Update title
    plt.tight_layout()
    plt.show()

# =======================================
# usage demo
# ========================================
def main():
    # Build graph and apply traffic   
    filename = "sample_input.csv"
    graph = build_graph(filename)

    print("\nWelcome to Smart Delivery Route Planner!")
    # Adjust graph edge weights for time-of-day traffic      
    time_of_day = input("\nEnter the time of day: ").lower()
    adjust_for_traffic(graph, time_of_day)
    # Get depot location and delivery stops from customers
    depot = input("\nEnter depot location: ").strip()
    deliveries = [x.strip() for x in input("Enter delivery stops (comma separated): ").strip().split(',')]
    
    # 1. Test is_route_possible()
    print("\nChecking delivery feasibility:")
    for dest in deliveries:
        if is_route_possible(graph, depot, dest):
            print(f"  {depot} → {dest}: Route exists.")
        else:
            print(f"  {depot} → {dest}: No route")

    # 2. Test find_shortest_path()
    print("\nFinding the shortest Route...")
    for dest in deliveries:
        print()
        if is_route_possible(graph, depot, dest):
            path, distance = find_shortest_path(graph, depot, dest) # Capture both path and distance
            if path:
                print(f"  {depot} → {dest}: {' -> '.join(path)} | {distance:.2f} ML") # Print the distance variable
            else:
                print(f"  {depot} → {dest}: No Path Found")

    # 3. Use plan_delivery() to generate batch delivery plan
    print("\nDelivery plan:")
    plans, total_distance = plan_delivery(graph, depot, deliveries)
    for i, (src, dest, path, dist) in enumerate(plans):
        if path:
            print(f"  {i+1}. {src} → {dest} ({dist:.2f} ML)")
        else:
            print(f"  {i+1}. {src} → {dest}: No Route")
    print(f"Total cost-effective distance: {total_distance:.2f} ML")
    
    # 4. call visualize_routes
    visualize_routes(graph, plans)


if __name__ == "__main__":
    main()

