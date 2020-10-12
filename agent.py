class Agent(object):
    def __init__(self, vertex, initial_state, identification = None):
        self.graph_vertex = vertex
        self.states = initial_state;
        self.neighbors = list()
        self.identification = identification
        self.interactionCount = 0
        
    def changeState(self, new_state):
        self.states = new_state
    
    def getState(self):
        return self.states
    
    def addNeighbor(self,agent):
        self.neighbors.append(agent)
    
    def getNeighbors(self):
        return self.neighbors
    
    def getIdentification(self):
        return self.identification
    
    def incrementInteractionCount(self):
        self.interaction_count += 1
        
    def getInteractionCount(self):
        return self.interaction_count

    def getVertex(self):
        return self.graph_vertex

    
