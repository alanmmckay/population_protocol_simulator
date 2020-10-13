#import the scanners and parsers
#import utility classes
#import helper functions

from graph_scanner import GraphScanner;
from graph_parser import GraphParser;

from init_scanner import InitScanner;
from init_parser import InitParser;

from transition_scanner import TransitionScanner;
from transition_parser import TransitionParser;

from population_protocol import PopulationProtocol

from helper_functions import file_input;

#graph_data = file_input("Input filename for graph data: ")
#init_data = file_input("Input filename for init set: ")
#transition_data = file_input("Input filename for transition set: ")

graph_data = "({a,b,c,d,e,f},{(a,b),(c,d)})"
init_data = "({{a,b,c,d,e}:[1]},{{f}:[2]})"
transition_data = "{((1,0)->(1,1)),((0,1)->(1,1)),((1,1)->(1,1)),((0,0)->(0,0))}"
graph_parse = GraphParser(GraphScanner(graph_data)).parse()
init_parse = InitParser(InitScanner(init_data),graph_parse[0]).parse()
transition_parse = TransitionParser(TransitionScanner(transition_data)).parse()

population = PopulationProtocol(graph_parse,transition_parse,init_parse)

for agent in population.getAgents():
    print(agent.getNeighbors())
   
print(population.getTransitionFunction())
