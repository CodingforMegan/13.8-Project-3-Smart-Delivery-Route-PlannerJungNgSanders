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
```
https://github.com/lolMichaelJung1/13.8-Project-3-Smart-Delivery-Route-PlannerJungNgSanders/blob/main/sample_input.png?raw=true
```
✅ Traffic Adjustement Criteria
```
Traffic_level{
        "heavy": 1.5,
        "high": 1.25,
        "moderate": 1.0,
        "light": 0.8,
        "low": 0.75
    }.get((level or "moderate").lower(), 1.0)

time_to_traffic = {
        "morning": "heavy",
        "late_morning": "high",
        "afternoon": "moderate",
        "evening": "light",
        "night": "low"
    }
```

✅ Sample Output

time_of_Day = "morning" (traffic_level = 1.5)
```
Welcome to Smart Delivery Route Planner!

Enter the time of day: Morning

Enter depot location: A
Enter delivery stops (comma separated): B,C,D

Checking delivery feasibility:
  A → B: Route exists.
  A → C: Route exists.
  A → D: Route exists.

Finding the shortest Route...

  A → B: A -> B | 15.00 ML

  A → C: A -> B -> C | 24.00 ML

  A → D: A -> D | 22.50 ML

Delivery plan:
  1. A → B (15.00 ML)
  2. B → C (9.00 ML)
  3. C → D (12.00 ML)
Total cost-effective distance: 36.00 ML
```
time_of_day = "night" (traffic_level = 0.75)
```
Welcome to Smart Delivery Route Planner!

Enter the time of day: Night

Enter depot location: A
Enter delivery stops (comma separated): B,C,D

Checking delivery feasibility:
  A → B: Route exists.
  A → C: Route exists.
  A → D: Route exists.

Finding the shortest Route...

  A → B: A -> B | 7.50 ML

  A → C: A -> B -> C | 12.00 ML

  A → D: A -> D | 11.25 ML

Delivery plan:
  1. A → B (7.50 ML)
  2. B → C (4.50 ML)
  3. C → D (6.00 ML)
Total cost-effective distance: 18.00 ML
```
## 📄 Function Designs 
Refer to DESIGN.md
- ✅ Purpose: what the function accomplishes
- ✅ Parameter/Return Values: Data going in and out
- ✅ Pseudocode: Step-by-step logic in English
