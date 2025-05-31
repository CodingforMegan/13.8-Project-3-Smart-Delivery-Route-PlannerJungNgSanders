#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
from __future__ import annotations
from traffic_simulation import get_traffic_multiplier


class Vertex:
    """
    Implements a vertex in a graph.

    Attributes
    ----------
    label : Any
    lat : float
    lon : float
    neighbors : dictionary that maps a vertex to an edge

    Methods
    -------
    add_neighbor(neighbor, edge)
        Connects a neighbor vertex to a vertex object.
    __lt__()
        Returns a bool comparing the label of a vertex and another vertex.
    __repr__()
        Returns a string representation of a vertex's label, latitude, and longitude.        
    """
    def __init__(self, label, lat=None, lon=None):
        self.label = label
        self.lat = lat
        self.lon = lon
        self.neighbors = {} # {neighbor_vertex: edge}

    def add_neighbor(self, neighbor: Vertex, edge: Edge) -> None:
        """
        Connects a neighbor vertex to a vertex object.

        Parameters
        ----------
        neighbor : Vertex instance
        edge : Edge instance

        Returns
        -------
        None
        """
        self.neighbors[neighbor] = edge

    def __lt__(self, other: Vertex) -> bool:
        """
        Returns a bool that results from a lexicographic comparison of the label of two vertices.

        Parameters
        ----------
        other : Vertex instance
        
        Returns
        -------
        bool
        """
        return self.label < other.label

    def __repr__(self) -> str:
        """
        Returns a string representation of a vertex instance's label, lat, and lon.
        
        Returns
        -------
        str
        """
        return f"Vertex({self.label}, lat={self.lat}, lon={self.lon})"

class Edge:
    """
    Implements an edge in a graph.

    Attributes
    ----------
    to : Vertex
    distance : int
    base_travel_time : int
    traffic : str
    time_of_day : float
    
    Methods
    -------
    adjusted_travel_time()
        Returns a float by calling the get_traffic_multiplier method from the traffic_simulation class
    current_weight()
        Returns a float that is calculated by distance / adjusted_time
    __repr__()
        Returns a string representation of an edge's label, distance, base_travel_time, traffic, and time_of_day     
    """    
    def __init__(self, to, distance, travel_time, traffic=None, time_of_day=None):
        self.to = to
        self.distance = distance
        self.base_travel_time = travel_time # static reference
        self.traffic = traffic
        self.time_of_day = time_of_day

    def adjusted_travel_time(self) -> float:
        """
        Returns a float representing the travel time by calling the get_traffic_multiplier from the traffic_simulation class, which uses a map.
        
        Returns
        -------
        float
        """
        multiplier = get_traffic_multiplier(self.traffic)
        return self.base_travel_time * multiplier

    def current_weight(self) -> float:
        """
        Returns the dynamic weight of an edge by using the formula distance / adjusted travel time.
        
        Returns
        -------
        float
        """
        adjusted_time = self.adjusted_travel_time()
        if adjusted_time == 0:
            return float("inf")
        return self.distance / adjusted_time  # higher = more efficient

    def __repr__(self) -> str:
        """
        Returns a string representation of an edge's to vertex, distance, base time, and traffic level.
        
        Returns
        -------
        str
        """
        return f"---> {self.to.label} (distance={self.distance}, base_time={self.base_travel_time}, traffic={self.traffic})"


class Graph:
    """
    Implements a graph using Vertex and Edge instances.

    Attributes
    ----------
    adjacency_list : dictionary where the key is the vertex label and value is a list representing the neighbors of that vertex
    vertices : dictionary where the key is the vertex label and value is the corresponding vertex object
    edges : dictionary where the key is a tuple (stat_label, end_label) and value is the corresponding edge object
    
    Methods
    -------
    add_vertex(label, lat=None, lon=None)
        Adds a unique vertex with a label, lat, and lon.
    get_vertex(label)
        Returns a single vertex object based on the label.
    add_directed_edge(start_label, end_label, distance, travel_time, traffic=None, time_of_day=None)
        Adds a directed edge from the start_label to _end label with the weight calculated by distance, travel_time, traffic,
        and time_of_day.     
    add_undirected_edge(start_label, end_label, distance, travel_time, traffic=None, time_of_day=None)
        Adds an undirected edge by adding two directed edges, one from the start_label to the end_label and one from the 
        end_label to start_label.
    get_edge(start_label, end_label)
        Returns an edge with the corresponding starting and ending labels.  
    update_edge(start_label, end_label, key, value)
        Updates an attribute of an edge.   
    get_neighbors(vertex_label)
        Helper method that returns all the neighbors of a vertex.           
    get_nodes()
        Helper method that returns a list of all the vertex labels.           
    """
    def __init__(self):
        """
        adjacency_list: key: vertex label, value: lists representing the edges originating from that vertex, for example, ('A': 'B', 'C', 'E')
        self.vertices: key: vertex label, value: corresponding Vertex object, for example, ('A': Vertex('A'))
        self.edges: key: a tuple (start_label, end_label), value: corresponding edges object, for example, (('A', 'E'): 15)
        """
        self.adjacency_list = {}
        self.vertices = {}
        self.edges = {} 
    

    def add_vertex(self, label: str, lat: int=None, lon: int=None) -> None:
        """
        Adds a vertex to the Graph instance.

        Parameters
        ----------
        label : str
        lat : int
            the latitude of the vertex, which is a location in the graph
        lon : int
            the longitude of the vertex, which is a location in the graph
        
        Returns
        -------
        None

        Raises
        ------
        ValueError
            If a vertex with the given label already exists.
        """
        if label in self.vertices:
            raise ValueError(f"Vertex with label {label} already exists.")
        new_vertex = Vertex(label, lat, lon)
        self.vertices[label] = new_vertex
        self.adjacency_list[label] = [] # Initialize adjacency list for the new vertex

    # retrieve a single Vertex object
    def get_vertex(self, label: str) -> Vertex:
        """
        Returns a Vertex instance from a Graph instance.

        Parameters
        ----------
        label : str
        
        Returns
        -------
        Vertex instance 
        """          
        return self.vertices.get(label)


    def add_directed_edge(
            self,
            start_label: str,
            end_label: str,
            distance: float,
            travel_time: int,
            traffic: str=None,
            time_of_day: str=None
        ) -> None:
        """
        Adds a directed edge to the Graph instance. If the start or end label vertices do not exist in the graph, they are created. Ensures that both vertices
        exist and have an edge that is valid.

        Parameters
        ----------
        start_label : str of the start vertex
        end_label :  str of the end vertex
        distance : float representing the distance, which is the weight of the edge
        travel_time : int
        traffic : str
        time_of_day: str
        
        Returns
        -------
        None

        Raises
        ------
        ZeroDivisionError
        """
        if start_label not in self.vertices:
            # Instantiate Vertex class with start_label
            print(f"Vertex {start_label} does not exist. Adding it now.")
            self.add_vertex(start_label)
        if end_label not in self.vertices:
            # Instantiate Vertex class with end_label
            print(f"Vertex {end_label} does not exist. Adding it now.")
            self.add_vertex(end_label)

        # Ensure both vertices exist after potential creation
        try:
            new_edge = Edge(self.vertices[end_label], distance, travel_time, traffic, time_of_day)
            print(f"Adding edge from {start_label} to {end_label} with weight {new_edge.current_weight():.2f}")
            self.adjacency_list[start_label].append(new_edge)
            self.edges[(start_label, end_label)] = round(new_edge.current_weight(), 2)
        except ZeroDivisionError:
            print(f"Warning: Could not add edge from {start_label} to {end_label}. Division by zero.")


    def add_undirected_edge(
            self,
            start_label: str,
            end_label: str,
            distance: float,
            travel_time: int,
            traffic: str=None,
            time_of_day: str=None
        ) -> None:
        """
        Adds an undirected edge to the Graph instance by adding two undirected edges, one from the start label to the end label and one from the end label to the start label.

        Parameters
        ----------
        start_label : str of the start vertex
        end_label :  str of the end vertex
        distance : float representing the distance, which is the weight of the edge
        travel_time : int
        traffic : str
        time_of_day: str
        
        Returns
        -------
        None
        """
        self.add_directed_edge(start_label, end_label, distance, travel_time, traffic, time_of_day)
        self.add_directed_edge(end_label, start_label, distance, travel_time, traffic, time_of_day)


    def get_edge(self, start_label: str, end_label: str) -> float:
        """
        Returns an edge's weight that has the corresponding start and end labels.

        Parameters
        ----------
        start_label : str of the start vertex
        end_label :  str of the end vertex
         
        Returns
        -------
        float
        """
        return self.edges.get((start_label, end_label))


    def update_edge(self, start_label: str, end_label: str, key: str, value: float) -> None:
        """
        Assigns a new weight to an existing edge.

        Parameters
        ----------
        start_label : str of the start vertex
        end_label :  str of the end vertex
        key : The attribute of an edge
        value: The weight of the edge, which is a float
        
        Returns
        -------
        None
        """          
        edge = self.get_edge(start_label, end_label)
        if edge: # Check if the edge exists
            if hasattr(edge, key): # Check if the edge object has the specified attribute
                setattr(edge, key, value)
            else:
                print(f"Warning: Edge from {start_label} to {end_label} does not have attribute '{key}'.")
        else:
            print(f"Warning: Edge from {start_label} to {end_label} not found.")

    # Helper method to get neighbors (edges originating from a vertex)
    def get_neighbors(self, vertex_label: str) -> list:
        """
        Returns the neighbors, which are the vertices connected to a vertex, in the form of an adjacency list.

        Parameters
        ----------
        vertex_label : str, which is the label of a vertex
        
        Returns
        -------
        list which consists of the neighbor vertices
        """         
        return self.adjacency_list.get(vertex_label, [])

    # Helper method to get all vertex labels (used in route check and dijkstra algorithm)
    def get_nodes(self) -> list[str]:
        """
        Returns the labels of all the existing vertices in the graph.
        
        Returns
        -------
        list
        """
        return list(self.vertices.keys())


if __name__ == "__main__":
    graph = Graph()

    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_vertex("E")
    graph.add_vertex("F")
    graph.add_vertex("G")
    graph.add_vertex("H")
    graph.add_vertex("I")


    for vertex in graph.vertices.values():
        print(vertex)

    # Iterate over dictionary items to get key-value pairs
    for label, edges in graph.adjacency_list.items():
        print(f"Vertex {label}: {edges}")

    graph.add_directed_edge("A", "B", 5, 10, "moderate")
    graph.add_directed_edge("A", "D", 10, 15, "low")
    graph.add_directed_edge("B", "C", 3, 6, "light")
    graph.add_directed_edge("C", "D", 4, 8, "heavy")
    graph.add_directed_edge("D", "E", 2, 4, "high")

    for vertex in graph.vertices.values():
        print(vertex)

    # Iterate over dictionary items to get key-value pairs
    for label, edges in graph.adjacency_list.items():
        print(f"Vertex {label}: {edges}")

    for key, value in graph.edges.items():
        print(f"{key}: {value}")
