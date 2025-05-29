#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
    """
    Includes functions to update the edges of the graph. Since the edges between vertices in our graph, we included two functions to 
    weigh the edges.

    Methods
    -------
    get_traffic_multiplier(level)
        Maps the traffic level to a multipler to weigh an edge in the graph.
    adjust_for_traffic(graph, time_of_day)
        Updates the weights of all edges in the graph based on the time of day.       
    """
def get_traffic_multiplier(level):
    """
    Map traffic level to a multiplier used for travel time adjustment.
    
    Parameters
    ----------
    level : str representing the severity of traffic/congestion
    
    Returns
    -------
    float that is mapped to the traffic level
    """    
    return {
        "heavy": 1.5,
        "high": 1.25,
        "moderate": 1.0,
        "light": 0.8,
        "low": 0.75
    }.get((level or "moderate").lower(), 1.0)


def adjust_for_traffic(graph, time_of_day):
    """
    Adjust traffic levels on all edges in the graph based on the time of day.
    This function updates the 'traffic' attribute on each edge.
    
    Parameters
    ----------
    graph : graph instance
    time_of_day : str
    
    Returns
    -------
    None
    """     
    time_to_traffic = {
        "morning": "heavy",
        "late_morning": "high",
        "afternoon": "moderate",
        "evening": "light",
        "night": "low"
    }

    new_level = time_to_traffic.get(time_of_day.lower(), "moderate")

    for u in graph.get_nodes():
        for edge in graph.get_neighbors(u):
            edge.traffic = new_level
