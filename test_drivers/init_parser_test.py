from sys import argv, path
import os
path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + 
'/../'))
path.insert(0, os.getcwd()) 

from graph_scanner import GraphScanner
from graph_parser import GraphParser
from helper_functions import file_input
from init_scanner import InitScanner
from init_parser import InitParser

graph_data = file_input('graph')
print("Looking at graph: " + str(graph_data))
graph_scanner = GraphScanner(graph_data)
graph_parser = GraphParser(graph_scanner)

init_data = file_input('init')
print("Looking at init set: "+ str(init_data))
init_scanner = InitScanner(init_data)
init_parser = InitParser(init_scanner, graph_parser.parse()[0])

print(init_parser.parse())
