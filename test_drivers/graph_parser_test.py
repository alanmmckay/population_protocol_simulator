from sys import argv, path
import os
path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + 
'/../'))
path.insert(0, os.getcwd())

from graph_scanner import GraphScanner
from graph_token import GraphToken, GraphTokenType
from graph_parser import GraphParser
from helper_functions import file_input

graph_data = file_input('graph')
print("Looking at graph: " + str(graph_data))
scanner = GraphScanner(graph_data)
parser = GraphParser(scanner)
print(parser.parse_graph())
