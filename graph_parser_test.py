from graph_scanner import GraphScanner
from graph_token import GraphToken, GraphTokenType
from graph_parser import GraphParser
from helper_functions import file_input

graph_data = file_input('graph')
print("Looking at graph: " + str(graph_data))
scanner = GraphScanner(graph_data)
parser = GraphParser(scanner)
print(parser.parse_graph())
