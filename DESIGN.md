# Project 3: Smart Delivery Route Planner - Design
- Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)
- Date: 5/12/25
- Course: Spr25_CS_034 CRN 39575

## Main Module Pseudocode & Design
### `build_graph()`
- Purpose: The `build_graph()` function reads a file name and constructs a Graph instance, with the appropriate Vertex and Edge instances.
- Parameters: `filename` (string)
- Returns: Graph instance
- Pseudocode:
  - ```text
    FUNCTION build_graph(filename)
        CREATE empty Graph class instance
        OPEN file FROM filename
        FOR EACH line IN file
            SET from_vertex, to_vertex, distance, travel_time, traffic FROM line.split()
            CALL add_directed_edge(from_vertex, to_vertex, distance, travel_time, traffic)
        RETURN Graph
    ```
### `is_route_possible()`
- Purpose: The `is_route_possible()` function takes a given Graph instance, along with start and end vertices. The function then analyzes the graph to determine if a route between the two vertices is possible. If the route is possible, the function will return True, otherwise it will return False.
- Parameters: `graph` (Graph instance), `start` (Vertex instance), `end` (Vertex instance)
- Returns: Boolean
- Pseudocode:
  - ```text
    FUNCTION is_route_possible(graph, start, end)
        CREATE an empty set, visited
        CREATE stack WITH the start vertex as the first item
        WHILE stack IS NOT EMPTY
            POP item FROM stack
            IF item EQUALS end vertex
                RETURN True
            IF item NOT IN visited
                ADD item TO visited
                ADD item neighbors TO stack
        RETURN False
    ```
### `find_shortest_path()`
- Purpose: The `find_shortest_path()` function, as the name suggests, finds the shortest possible path between two given Vertex instances
- Parameters: `graph` (Graph instance), `start` (Vertex instance) , `end` (Vertex instance)
- Returns: A list of the vertices that compose the shortest route between the start and end path
- Pseudocode:
  - ```text
    FUNCTION find_shortest_path(graph, start, end)
        IF start OR end NOT IN graph
            RETURN None
        CREATE empty dictionary distance
        CREATE empty dictionary prev
        FOR vertex IN graph.get_nodes()
            SET distance[vertex] TO infinity
            SET previous[vertex] TO None
        SET dist[start] TO 0
        CREATE queue WITH (0, start)

        WHILE queue IS NOT EMPTY
            POP (curr_dist, u) WITH SMALLEST curr_dist FROM queue
            IF u EQUALS end
                BREAK
            FOR edge IN graph.neighbors(u)
                SET v TO edge.to
                SET weight TO edge.adjusted_travel_time()
                IF distance[u] + weight < distance[v]
                    SET distance[v] TO distance[u] + weight
                    SET previous[v] TO u
                    ADD (distance[v], v) TO queue

        IF distance[end] IS infinity
            RETURN None

        CREATE empty list path
        SET node TO end
        WHILE node IS NOT None
            INSERT node AT FRONT OF path
            SET node TO previous[node]
        RETURN path
    ```
### `plan_delivery()`
- Purpose: The `plan_delivery` function takes in a graph, a depot (starting Vertex instance) and a list of delivery destinations (Vertex instances). For each of the delivery vertices, it repeatedly calls `find_shortest_path()` to plan out a list of delivery paths.
- Parameters: `graph` (Graph instance), `depot` (Vertex instance), `deliveries` (list of Vertex instances)
- Returns: List of paths between `depot` and each Vertex in `deliveries`
- Pseudocode:
  - ```text
    FUNCTION plan_delivery(graph, depot, deliveries)
        CREATE list plans
        FOR EACH delivery IN deliveries
            CALL find_shortest_path(graph, depot, delivery)
            ADD found path TO plans
        RETURN plans
    ```

## Traffic Simulation Module Pseudocode & Design
### `adjust_for_traffic()`
- Purpose: The `adjust_for_traffic()` function allows for adjusting the travel times of particular graph edges based on a given time of day.
- Parameters: `graph` (Graph instance), `time_of_day` (string)
- Returns: `None`
- Pseudocode:
  - ```text
    FUNCTION adjust_for_traffic(graph, time_of_day)
        SET traffic_level FROM time_of_day
        FOR EACH node IN graph
            FOR EACH edge IN node
                SET edge.traffic TO traffic_level
    ```


## Class Pseudocode & Design
### `graph_utils.Vertex`
- The `graph_utils.Vertex` class is used to manage attributes and methods for graph vertices.
##### Attributes
- `label`: The string label associated with the particular vertex
- `lat`: The float value for the latitude of the particular vertex
- `lon`: The float value for the longitude of the particular vertex
- `attributes`: A dictionary of any additional attribute values for a vertex
##### Methods
- `__init__`
  - Purpose: The `__init__` method initializes the Vertex class with a `label`, `latitude` (default None), `longitude` (default None), and `attributes` (default None)
  - Parameters: `label`, `latitude` (default None), `longitude` (default None), and `attributes` (default None) 
  - Returns: `None`
  - Pseudocode: 
    - ```text
      CLASS Vertex
          FUNCTION __init__(label, latitude=None, longitude=None, attributes=None)
              SET self.label, self.latitude, self.longitude TO label, latitude, longitude
              IF attributes
                  SET self.attributes TO attributes
              ELSE
                  SET self.attributes TO {}
      ```
- `__repr__`
  - Purpose: The `__repr__` method is used to give a string representation of the Vertex instance, printing the specific instance attributes
  - Parameters: No parameters
  - Returns: `None` (The string representation is printed)
  - Pseudocode:
    - ```text
      FUNCTION __repr__()
          PRINT "Vertex(label={self.label}, lat={self.lat}, lon={self.lon})"
      ```

### `graph_utils.Edge`
- The `graph_utils.Edge` class is used to manage attributes and methods for graph edges.
##### Attributes
- `to`
- `distance`
- `travel_time`
- `traffic`
- `time`
##### Methods
- `__init__()`
  - Purpose: The `__init__` method initializes the Edge class with a `to`, `distance`, `travel_time`, `traffic` (default None), and `time_of_day` (default None)
  - Parameters: `to`, `distance`, `travel_time`, `traffic` (default None), `time_of_day` (default None)
  - Returns: `None`
  - Pseudocode: 
    - ```text
      CLASS Edge
          FUNCTION __init__(to, distance, travel_time, traffic=None, time_of_day=None)
              SET self.to, self.distance, self.travel_time, self.traffic, self.time
                  TO to, distance, travel_time, traffic, time
      ```
- `__repr__()`
  - Purpose: The `__repr__` method is used to give a string representation of the Edge instance, printing the specific instance attributes
  - Parameters: No parameters
  - Returns: `None` (The string representation is printed)
  - Pseudocode:
    - ```text
      FUNCTION __repr__()
          PRINT "---> {self.to} (distance={self.distance}, time={self.travel_time}, traffic={self.traffic})"
      ```
- `adjusted_travel_time()`
  - Purpose: The `adjusted_travel_time()` method is used to calculate an expected travel time based on the given traffic level.
  - Parameters: None
  - Returns: A float value representing the calculated adjusted travel time
  - Pseudocode:
    - ```text
      FUNCTION adjusted_travel_time()
          IF self.traffic EQUALS "heavy":
              RETURN self.travel_time * 1.5
          ELSE IF self.traffic EQUALS "light":
              RETURN self.travel_time * 0.8
          RETURN self.travel_time
      ```

### `graph_utils.Graph`
- The `graph_utils.Graph` class is used to manage attributes and methods for graphs, including edges, vertices, and an adjacency list
##### Attributes
- `adjacency_list`: default value = `{}`
- `vertices`: default value = `{}`
##### Methods
- `__init__()`
  - Purpose: The `__init__` method initializes a Graph class instance with two empty dictionaries, `adjacency_list` and `vertices`
  - Parameters: None
  - Returns: `None`
  - Pseudocode:
    - ```text
      CLASS Graph
          FUNCTION __init__()
              SET self.adjacency_list, self.vertices TO {}, {}
      ```
- `add_vertex(vertex)`
  - Purpose: Using the given vertex's label as a key, the vertex is added to the Graph class instance `vertices` dictionary, and using the same key, an empty list is added to the `adjacency_list` dictionary 
  - Parameters: `vertex`
  - Returns: `None`
  - Pseudocode:
    - ```text
      FUNCTION add_vertex(vertex)
          SET KEY self.vertices TO vertex.label
          SET VALUE self.vertices[vertex.labl] TO vertex
      ```
- `get_vertex(label)`
  - Purpose: Given a label, this method retrieves the corresponding vertex from the Graph class instance `vertices` attribute
  - Parameters: `label` (string)
  - Returns: The found Vertex instance
  - Pseudocode:
    - ```text
      FUNCTION get_vertex(label)
          RETURN the vertex instance matching the provided label FROM self.vertices
      ```
- `add_directed_edge(from_vertex, to_vertex, distance, travel_time, traffic, time_of_day)`
  - Purpose: The `add_directed_edge()` method takes in two Vertex instances and adds a record in the Graph instance `adjacency_list` dictionary to note that the two edges are adjacent to each other. This method is used to denote a one-way relationship between two vertices.
  - Parameters: `from_vertex` (Vertex instance), `to_vertex` (Vertex instance), `distance` (float), `travel_time` (float), `traffic` (string), `time_of_day` (string)
  - Returns: `None`
  - Pseudocode:
    - ```text
      FUNCTION add_directed_edge(from_vertex, to_vertex, distance, travel_time, traffic, time_of_day)
          ADD from_vertex WITH attributes TO self.vertices IF NOT EXISTS
          ADD to_vertex WITH attributes TO self.vertices IF NOT EXISTS
          ADD edge relationship TO self.adjacency_list
      ```
- `add_undirected_edge(from_vertex, to_vertex, distance, travel_time, traffic, time_of_day)`
  - Purpose: The `add_undirected_edge()` method takes in two Vertex instances and adds two directed edge relationships between them.
  - Parameters: `from_vertex`, `to_vertex`, `distance`, `travel_time`, `traffic`, `time_of_day`
  - Returns: `None`
  - Pseudocode:
    - ```text
      FUNCTION add_undirected_edge(from_vertex, to_vertex, distance, travel_time, traffic, time_of_day)
          CALL add_directed_edge(from_vertex, to_vertex, distance, travel_time, traffic, time_of_day)
          CALL add_directed_edge(to_vertex, from_vertex, distance, travel_time, traffic, time_of_day)
      ```
- `get_edge(from_vertex, to_vertex)`
  - Purpose: The `get_edge()` method retrieves the Edge instance between the `from_vertex` and the `to_vertex`
  - Parameters: `from_vertex` (Vertex instance), `to_vertex` (Vertex instance)
  - Returns: The found Edge instance between the two vertices, otherwise `None`
  - Pseudocode:
    - ```text
      FUNCTION get_edge(from_vertex, to_vertex)
          IF a matching edge between from_index and to_index is found IN self.adjacency_list
              RETURN matching edge
          ELSE
              RETURN None
      ```
- `update_edge(from_vertex, to_vertex, key, value)`
  - Purpose: For a given Edge instance (between `from_vertex` and `to_vertex`), set the given `key` to the provided `value`
  - Parameters: `from_vertex`, `to_vertex`, `key`, `value`
  - Returns: `None`
  - Pseudocode:
    - ```text
      FUNCTION update_edge(from_vertex, to_vertex, key, value)
          SET edge TO RESULT OF CALL get_edge(from_vertex, to_vertex)
          SET edge.key EQUAL TO value
      ```
