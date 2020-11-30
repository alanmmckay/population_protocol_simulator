from subprocess import check_call

from graph_scanner import GraphScanner
from graph_parser import GraphParser
from init_scanner import InitScanner
from init_parser import InitParser
from transition_scanner import TransitionScanner
from transition_parser import TransitionParser

from population_protocol import PopulationProtocol
from helper_functions import file_input

def process_file(file_name):
    f = open(file_name, 'r')
    data = f.read()
    f.close()
    data = data.replace(' ','').replace('\n','')
    return data

graph_data = process_file("test.graph")
init_data = process_file("test.init")
transition_data = process_file("test.transition")

graph_scanner = GraphScanner(graph_data)
graph_parser = GraphParser(graph_scanner)
graph_parsed = graph_parser.parse()

init_scanner = InitScanner(init_data)
init_parser = InitParser(init_scanner, graph_parsed[0])
init_parsed = init_parser.parse()

transition_scanner = TransitionScanner(transition_data)
transition_parser = TransitionParser(transition_scanner)
transition_parsed = transition_parser.parse()


population = PopulationProtocol(graph_parsed,transition_parsed,init_parsed)

convergence = input("Expected convergence for this protocol: ")
userInput = input("Command: ")
printcount = 0
while userInput != 'q':
    if userInput == "interact":
        userInput = int(input("quantity: "))
        if userInput == 0:
            while population.checkConvergence(convergence) == False:
                status = population.invokeInteraction()
                if status == "stateChanged":
                    break
            if population.checkConvergence(convergence) == True:
                print("Population has converged")
        else:
            count = 0
            while count < userInput:
                status = population.invokeInteraction()  
                if status:
                    count += 1
    if userInput == 'converge':
        userInput = int(input("Max interactions: "))
        count = 0
        while population.checkConvergence(convergence) == False:
            if(count > userInput):
                break
            population.invokeInteraction()
            count += 1
    if userInput == 'converge and nullprint':
        userInput = int(input('max interactions: '))
        count = 0
        while population.checkConvergence(convergence) == False:
            if(count > userInput):
                break
            count+=1
            population.invokeInteraction()
            dot = population.renderConfiguration("null")
            graphfile = open('output/graph'+str(printcount)+'.dot','w')
            graphfile.write(dot)
            graphfile.close()
            check_call(['dot','-Tpng','output/graph'+str(printcount)+'.dot','-o','output/graph-'+str(printcount)+'.png'])
            printcount += 1
            
    if userInput == 'nullprint':
        dot = population.renderConfiguration("null")
        print(dot)
        graphfile = open('output/graph'+str(printcount)+'.dot','w')
        graphfile.write(dot)
        graphfile.close()
        check_call(['dot','-Tpng','output/graph'+str(printcount)+'.dot','-o','output/graph-'+str(printcount)+'.png'])
        printcount += 1
    if userInput == "print":
        dot = population.renderConfiguration("regular")
        graphfile = open('output/graph'+str(printcount)+'.dot','w')
        graphfile.write(dot)
        graphfile.close()
        check_call(['dot','-Tpng','output/graph'+str(printcount)+'.dot','-o','output/graph-'+str(printcount)+'.png'])
        printcount += 1
        
    userInput = input("Command: ")

#dot -Tpng filename.dot -o outputfile.png
