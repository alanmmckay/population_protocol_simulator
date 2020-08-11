from helper_functions import file_input

graph_data = file_input('graph')

print(graph_data)

scanner_position = 0

if graph_data[0] == '(':
    if graph_data[1] == '{':
        if graph_data[2] != ',':
            scanner_position = 2
        else:
            raise ValueError("syntax error: ,")
    else:
        raise ValueError("syntax error: {")
else:
    raise ValueError("syntax error: (")


active_vertices = list()

new_vertex = str()
while graph_data[scanner_position] != '}':
    new_vertex += graph_data[scanner_position]
    scanner_position += 1
