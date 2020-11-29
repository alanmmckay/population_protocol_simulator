class Agent(object):
    def __init__(self, vertex, initial_state, identification = None):
        self.graph_vertex = vertex
        self.states = initial_state;
        self.neighbors = list()
        #used to prevent having to call len() on the neighbors list:
        self.neighbor_count = 0
        self.identification = identification
        
    def changeState(self, new_state):
        self.states = new_state
    
    def getState(self):
        return self.states
    
    def addNeighbor(self,agent):
        self.neighbor_count += 1
        self.neighbors.append(agent)
    
    def getNeighbors(self):
        return self.neighbors
    
    def validateNeighbor(self, agent):
        if agent in self.neighbors:
            return True
        else:
            return False
    
    '''
        not sure what to name this method. Essentially is a validator or will retreive
        an agent at a defined numeric index.
        The simulator will use this method to retreive a random neighbor of an agent.
    '''
    def getNeighbor(self,agent):
        if type(agent) == int:
            #validate range, return at index
            if agent < len(self.neighbors):
                return self.neighbors[agent]
            else:
                #perhaps throw an error
                return False
        elif type(agent) == Agent:
            return self.validateNeighbor(agent)
        
    def getNeighborCount(self):
        return self.neighbor_count
    
    def getIdentification(self):
        return self.identification

    def getVertex(self):
        return self.graph_vertex

    
