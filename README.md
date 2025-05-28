# 13.8-Project-3-Smart-Delivery-Route-PlannerJungNgSanders

## Group Members
Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

## 🧠 Project Design & Structure
```
project_3/
├── main.py:
├           build_graph(filename)
├           is_route_possible(graph, start, end)
├           find_shortest_path(graph, start, end)
├           plan_delivery(graph, start, end)
├           visualize_graph(graph, plans)
├── graph_utils.py: Vertex class, Graph class, Edge class
├── traffic_simulation.py: adjust_for_traffic(graph, time_of_day),get_traffic_multiplier(level)
├── design_doc.pdf
├── sample_input.csv
├── README.md
└── DESIGN.md
```

## 📄 Overview
✅ Real-world purpose of the project

In this lab, our team will design and develop a graph-based Smart Delivery Route Planner System to help a logistics company provide reliable and adaptive delivery services to its customers while optimizing its efficiency.
The core goal of this system is to minimize delivery time and travel distance, thereby reducing fuel consumption, labor costs, and transportation delays—all of which contribute to a satisfying and cost-effective customer experience.
The system begins by constructing a representative road network, modeling the city as a graph where delivery locations are vertices and roads are directed, weighted edges—with weights representing distance or estimated travel time. Upon receiving a delivery request, the system first validates the route's feasibility based on the current state of the road network and, if available, real-time traffic conditions.
If the route is available, it applies graph algorithms such as Dijkstra’s algorithm to compute the shortest path between delivery points, and may use DFS or BFS to determine route connectivity. The system then generates an optimal delivery route that considers key factors such as distance, travel time, and delivery urgency.
Furthermore, our planning system also can dynamically adapt delivery routes in real time to prioritize urgent shipments while still efficiently handling regular deliveries.

✅ Input
sample_input.csv
```
A	B	5	10	moderate
B	C	3	6	light
C	D	4	8	heavy
D	E	2	4	high
A	D	10	15	low
```

✅ Sample Output
```
--- Smart Delivery Planner ---
Depot: A
Time of Day: morning

Edge Weights After Traffic Adjustment:
  A → B | Distance: 5.0 | Adjusted Time: 10.00 | Efficiency (dist/time): 0.50
  A → D | Distance: 10.0 | Adjusted Time: 11.25 | Efficiency (dist/time): 0.89
  B → C | Distance: 3.0 | Adjusted Time: 4.80 | Efficiency (dist/time): 0.62
  D → E | Distance: 2.0 | Adjusted Time: 5.00 | Efficiency (dist/time): 0.40
  C → D | Distance: 4.0 | Adjusted Time: 12.00 | Efficiency (dist/time): 0.33


Checking route feasibility:
  A → B: Possible
  A → C: Possible
  A → D: Possible
  A → E: Possible
  A → X: No Route


Finding shortest paths:
  A → B: A -> B
  A → C: A -> B -> C
  A → D: A -> D
  A → E: A -> D -> E
Error: One or both vertices (A, X) do not exist in the graph.
  A → X: No Path Found


Delivery Plan Summary:
No route possible from A to X.
  Delivery to B: A -> B
  Delivery to C: A -> B -> C
  Delivery to D: A -> D
  Delivery to E: A -> D -> E
  Delivery to X: No Route
```
- An instance of Graphs.
- Boolean value True/False for route check
- A sequence of vertex objects that compose the shortest route between the depot and delivery destination, alongside with travel distance or time
- Visualized delivery network with matplotlib 

✅ A worked-out manual example using 4–6 city nodes


## 📄 Function Designs (refer to DESIGN.md)
- ✅ Purpose: what the function accomplishes
- ✅ Parameter/Return Values: Data going in and out
- ✅ Pseudocode: Step-by-step logic in English
