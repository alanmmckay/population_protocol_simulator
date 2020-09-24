from sys import argv, path
import os
path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + 
'/../'))
path.insert(0, os.getcwd())

from graph_scanner import GraphScanner
from helper_functions import file_input

graph_data = file_input('graph')
print("Looking at graph: " + str(graph_data))
graph = GraphScanner(graph_data)

while True:
    token = graph.getNextToken()
    print(token)
    if token.isEOF():
        break
