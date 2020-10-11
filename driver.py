#import the scanners and parsers
#import utility classes
#import helper functions

from graph_scanner import GraphScanner;
from graph_parser import GraphParser;

from init_scanner import InitScanner;
from init_parser import InitParser;

from transition_scanner import TransitionScanner;
from transition_parser import TransitionParser;

from helper_functions import file_input;

graph_data = file_input("Input filename for graph data: ")
init_data = file_input("Input filename for init set: ")
transition_data = file_input("Input filename for transition set: ")
graph_parse = GraphParser(GraphScanner(graph_data)).parse()
init_parse = InitParser(InitScanner(init_data),graph_parse[0]).parse()
transition_parse = TransitionParser(TransitionScanner(transition_data)).parse()

