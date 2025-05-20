#Group Members: Michael Jung (ID:10680322), Timothy Sanders (ID: 01002147), Megan Ng (ID: 00756276)

#Date: 5/12/25

#Course: Spr25_CS_034 CRN 39575
#----------------------------------------------
def adjust_for_traffic(graph, time_of_day):
    traffic_levels = {
        "morning": "heavy",
        "afternoon": "moderate",
        "evening": "light",
        "night": "light"
    }
    new_level = traffic_levels.get(time_of_day, "moderate")

    for u in graph.get_nodes():
        for edge in graph.neighbors(u):
            edge.traffic = new_level
