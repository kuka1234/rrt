def check_duplicate(random_point, closest_node): ##have removed
    # checks for duplicates; can happen later on
    for i in start_node.get_list_of_nodes():
        if i.name == scaleDown(closest_node.name, random_point):
            return "duplicated point" + "see if statement"

def check_new_parent_node(new_point, start_node):
    for i in start_node.get_list_of_nodes():
        temp_dist = findDistance(i.name, new_point.name)
        if temp_dist< search_factor and temp_dist + i.getDistance() < new_point.getDistance() and not checkForCollisons(i.name, new_point.name):
            new_point.changeParent(i)

def check_for_child_node(new_point, start_node):
    # checks if any nodes close to the new node can be connected to the new node to form a short path. New node -> node
    for i in start_node.get_list_of_nodes():
        temp_dist = findDistance(i.name, new_point.name)
        if temp_dist< search_factor and temp_dist + new_point.getDistance() < i.getDistance() and not checkForCollisons(
                i.name, new_point.name):
            i.changeParent(new_point)
