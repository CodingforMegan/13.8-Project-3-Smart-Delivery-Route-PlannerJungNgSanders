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
    Djikstra's shortest path algorithm.

    Parameters
    ----------
    graph : Graph instance
    start_label: str which is the starting or "from" vertex
    end_label: str which is the ending or "to" vertex
    
    Returns
    -------
    list containing the labels of the vertices that represent the shortest path from the starting and ending vertices.
    """       
      if start_label not in graph.get_nodes() or end_label not in graph.get_nodes():
          print(f"Error: One or both vertices ({start_label}, {end_label}) do not exist in the graph.")
          return None

      distances = {node: float("inf") for node in graph.get_nodes()}
      prev = {node: None for node in graph.get_nodes()}
      distances[start_label] = 0
      queue = [(0, start_label)]

      while queue:
          curr_dist, current_label = heapq.heappop(queue)
          if current_label == end_label:
              break
          for edge in graph.get_neighbors(current_label):
              neighbor_label = edge.to.label
              weight = edge.adjusted_travel_time()
              if distances[current_label] + weight < distances[neighbor_label]:
                  distances[neighbor_label] = distances[current_label] + weight
                  prev[neighbor_label] = current_label
                  heapq.heappush(queue, (distances[neighbor_label], neighbor_label))

      if distances[end_label] == float("inf"):
          print(f"No path found from {start_label} to {end_label}.")
          return None

      path = []
      current_label = end_label
      while current_label:
          path.append(current_label)
          current_label = prev[current_label]
      return list(reversed(path))


def plan_delivery(graph, depot_label, delivery_labels):
    """
    Finds the shortest path that contains all vertices/locations from a starting vertex/depot and a list of delivery locations that are to be visited.

    Parameters
    ----------
    graph : Graph instance
    depot_label: str which is the starting or "from" vertex
    delivery_labels: list which contains the labels of all the vertices that are to be visited
    
    Returns
    -------
    list of tuples containing the labels of the vertices that represent the shortest path that includes the starting vertex/depot and all the vertices/delivery locations that
    are to be visited.
    """       
    plans = []
    for dest_label in delivery_labels:
        # Check if a route is possible before finding the shortest path
        if is_route_possible(graph, depot_label, dest_label):
            path = find_shortest_path(graph, depot_label, dest_label)
            plans.append((dest_label, path))
        else:
            # Handle cases where the route is not possible
            print(f"No route possible from {depot_label} to {dest_label}.")
            plans.append((dest_label, None)) # Append None to indicate no path
    return plans


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
    print("\n\nChecking route feasibility:")
    for dest in deliveries:
        possible = is_route_possible(graph, depot, dest)
        print(f"  {depot} → {dest}: {'Possible' if possible else 'No Route'}")


    # 2. Test find_shortest_path()
    print("\n\nFinding shortest paths:")
    for dest in deliveries:
        path = find_shortest_path(graph, depot, dest)
        if path:
            print(f"  {depot} → {dest}: {' -> '.join(path)}")
        else:
            print(f"  {depot} → {dest}: No Path Found")


    # 3. Use plan_delivery() to generate batch delivery plan
    print("\n\nDelivery Plan Summary:")
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

