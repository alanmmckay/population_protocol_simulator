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
