from graph_scanner.py import GraphScanner
from graph_token import GraphToken, GraphTokenType
from helper_functions import file_input

graph_data = file_input('graph')
print("Looking at graph: " + str(graph_data))
graph = GraphScanner(graph_data)

while True:
    token = graph.getNextToken()
    print(token)
    if token.isEOF():
        break
