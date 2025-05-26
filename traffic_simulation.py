#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------

def get_traffic_multiplier(level):
    """Map traffic level to a multiplier used for travel time adjustment."""
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
