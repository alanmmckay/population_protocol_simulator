from helper_functions import file_input

graph_data = file_input('graph')

print(graph_data)

scanner_position = 0

if graph_data[0] == '(':
    if graph_data[1] == '{':
        if graph_data[2] != ',':
            scanner_position = 2
        else:
            raise ValueError("syntax error: leading comma")
    else:
        raise ValueError("syntax error: {")
else:
    raise ValueError("syntax error: (")


active_vertices = list()

new_vertex = str()
comma_bool = False

def insert_vertex(vertex):
    if vertex not in active_vertices:
        active_vertices.append(new_vertex)
    else:
        raise ValueError("duplicate vertex")

while graph_data[scanner_position] != '}':
    if graph_data[scanner_position] == ',':
        insert_vertex(new_vertex)
        new_vertex = str()
        comma_bool = True
    else:
        new_vertex += graph_data[scanner_position]
        comma_bool = False
    scanner_position += 1

if comma_bool == False:
    insert_vertex(new_vertex)
    scanner_position += 1
else:
    raise ValueError("syntax error: trailing comma")
print(active_vertices)
print(graph_data[scanner_position])


if graph_data[scanner_position] == ',':
    scanner_position += 1
    if graph_data[scanner_position] == '{':
        scanner_position += 1
        if graph_data[scanner_position] == ',':
            raise ValueError("syntax error: leading comma")
    else:
        raise ValueError("syntax error: {")
else:
    raise ValueError("syntax error: missing comma between sets")
