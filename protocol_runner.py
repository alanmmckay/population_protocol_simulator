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
    f = open('input/'+str(file_name), 'r')
    data = f.read()
    f.close()
    data = data.replace(' ','').replace('\n','')
    return data

def process_components(name):
    graph_data = process_file(name+".graph")
    init_data = process_file(name+".init")
    transition_data = process_file(name+".transition")

    graph_scanner = GraphScanner(graph_data)
    graph_parser = GraphParser(graph_scanner)
    graph_parsed = graph_parser.parse()

    init_scanner = InitScanner(init_data)
    init_parser = InitParser(init_scanner, graph_parsed[0])
    init_parsed = init_parser.parse()

    transition_scanner = TransitionScanner(transition_data)
    transition_parser = TransitionParser(transition_scanner)
    transition_parsed = transition_parser.parse()
    
    return (graph_parsed,init_parsed,transition_parsed)


print(" --- Population Protocol Runner --- ")
print(" -- At any point, input 'quit' to quit -- ")

userInput = str()

q = 0
while userInput != 'quit':
    userInput = input("Input protocol name: ")
    if userInput != 'quit':
        name = userInput
        data_tuple = process_components(name)
        population = PopulationProtocol(data_tuple[0],data_tuple[1],data_tuple[2])
    else:
        break
    
    userInput = input("expected convergence for this protocol: ")
    if userInput != 'quit':
        convergence = userInput
    else:
        break
    
    printcount = 0
    step = 0
    converged = False
    print(" --- Population "+name+" selected. Convergence value: "+convergence)
    print("Input 'exit' at anytime to leave this population and select anew")
    
    while (userInput != 'quit') and (userInput != 'exit'):
        if userInput == "interact":
            userInput = input("Amount of interactions: (input 0 to interact until a state changes) ")
            
            if userInput == 'quit' or userInput == 'exit':
                break
            
            userInput = int(userInput)
            
            if userInput == 0:
                while population.checkConvergence(convergence) == False:
                    status = population.invokeInteraction()
                    
                    ### convergance check
                    step+=1
                    if population.checkConvergence(convergence) == True:
                        if converged == False:
                            converged = step
                            
                    if status == "stateChanged":
                        break
                    
            else:
                count = 0
                while count < userInput:
                    status = population.invokeInteraction()  
                    if status:
                        count += 1
                    
                    ### convergence check
                    step+=1
                    if population.checkConvergence(convergence) == True:
                        if converged == False:
                            converged = step
                            
        if userInput == 'converge':
            userInput = input("Maximum amount of interactions: ")
            
            if userInput == 'quit' or userInput == 'exit':
                break
            
            userInput = int(userInput)
            count = 0
            while population.checkConvergence(convergence) == False:
                if(count > userInput):
                    break
                population.invokeInteraction()
                count += 1
                
                ### convergence check
                step+=1
                if population.checkConvergence(convergence) == True:
                    if converged == False:
                        converged = step
                    
        if userInput == 'converge and nullprint':
            userInput = input('Maximum amount of interactions: ')
            
            if userInput == 'quit' or userInput == 'exit':
                break
            
            userInput = int(userInput)
            count = 0
            while population.checkConvergence(convergence) == False:
                if(count > userInput):
                    break
                count+=1
                status = population.invokeInteraction()
                if status == 'stateChanged':
                    dot = population.renderConfiguration("null")
                    graphfile = open('output/graph'+str(printcount)+'.dot','w')
                    graphfile.write(dot)
                    graphfile.close()
                    check_call(['dot','-Tpng','output/graph'+str(printcount)+'.dot','-o','output/graph-'+str(printcount)+'.png'])
                    printcount += 1
                
                ### convergence check
                step+=1
                if population.checkConvergence(convergence) == True:
                    if converged == False:
                        converged = step
                    
        if userInput == 'nullprint':
            dot = population.renderConfiguration("null")
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
        
            
        if userInput == "rollback":
            print(population.log.null_indexes)
            print(population.log.indexes)
            userInput = input("step to rollback: ")
            population.log.rollback(int(userInput))
            
        if userInput == "restore":
            population.log.restore()
        
        
        if converged != False and converged != -1:
            print("Population has converged on step "+str(converged))
            converged = -1
            
        userInput = input("Command: ")

    for i in range(0,printcount):
        check_call(['rm','output/graph'+str(i)+'.dot'])
        check_call(['rm','output/graph-'+str(i)+'.png'])
#dot -Tpng filename.dot -o outputfile.png
