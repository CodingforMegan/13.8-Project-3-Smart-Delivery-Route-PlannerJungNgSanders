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
├── graph_utils.py: Vertex class, Graph class, Edge class
├── traffic_simulation.py: adjust_for_traffic(graph, time_of_day)
├── design_doc.pdf
├── sample_input.csv
└── README.md
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

✅ Expected output
- An instance of Graphs.
- Boolean value True/False for route check
- A sequence of vertex objects that compose the shortest route between the depot and delivery destination, alongside with travel distance or time
- Visualized delivery network with matplotlib 

✅ A worked-out manual example using 4–6 city nodes


## 📄 Function Designs (refer to DESIGN.md)
- ✅ Purpose: what the function accomplishes
- ✅ Parameter/Return Values: Data going in and out
- ✅ Pseudocode: Step-by-step logic in English
