import random
from agent import Agent

class PopulationProtocol(object):
    def __init__(self,graph,transitions,init):
        #graph: [[vertices],[edges]
        #edge: tuple: (from vertex, to vertex)
        #transitions {state(s): state(s)}
        #init: {vertex: state(s)}
        
        self.vertices = graph[0]
        self.edges = graph[1]
        self.transition_function = transitions
        self.initial_values = init
        self.agents = list()
        self.agents_length = len(graph[0])
        
        edge_iterator = list(self.edges)
        for vertex in self.vertices:
            new_agent = Agent(vertex, self.initial_values[vertex])
            for edge in edge_iterator:
                if edge[0] == vertex:
                    new_agent.addNeighbor(edge[1])
                    edge_iterator.remove(edge)
            self.agents.append(new_agent)
                    
    def getAgents(self):
        return self.agents
   
    def getTransitionFunction(self):
       return self.transition_function
   
    def invokeInteractions(self,sender = None,receiver = None):
        if sender == None:
            sender = random.randint(0,self.agents_length - 1)
            sender = agents[sender]
        if receiver == None:
            receiver = random.randint(0,sender.getNeighborCount() - 1)
        receiver = sender.getNeighbor(receiver)#will return false if not a neighbor
        if receiver:
            #factor the transition function; look up state pair and assign new values 
            current_state = (sender.getState(),receiver.getState())
            if str(current_state) in self.transition_function:
                #log interaction
                newStates = self.transition_function[str(current_state)]
                sender.changeState(newStates[0])
                receiver.changeState(newStates[1])
            else:
                #log null interaction
                pass
                
            
        
