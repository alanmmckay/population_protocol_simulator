import random
import math
from agent import Agent
from interaction_log import InteractionLog

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
        
        if len(self.edges) == 0:
            for v1 in self.vertices:
                for v2 in self.vertices:
                    if v1 != v2:
                        self.edges.append((v1,v2))
        
        self.log = InteractionLog(self.edges)
        #edge_iterator = list(self.edges)
        
        for vertex in self.vertices:
            new_agent = Agent(vertex, self.initial_values[vertex][0])
            for edge in self.edges:
                if edge[0] == vertex:
                    new_agent.addNeighbor(edge[1])
                    #edge_iterator.remove(edge)
            self.agents.append(new_agent)
           
           
    def getAgents(self):
        return self.agents
    
    
    def getAgentStates(self):
        agentDict = dict()
        for agent in self.agents:
            agentDict[agent.getVertex()] = agent.getState()
        return agentDict
   
   
    def checkConvergence(self,value):
        for agent in self.agents:
            if str(agent.getState()) != str(value):
                return False
        return True
   
   
    def invokeInteraction(self,sender = None,receiver = None):
        init = sender
        if sender == None or receiver == None:
            candidates = list(self.agents)
            candidates_length = int(self.agents_length)
        
        if sender == None:
            while sender == None:
                if candidates_length <= 0:
                    raise ValueError("No edges exist; invokeInteraction")
                new = random.randint(0,candidates_length - 1)
                new = candidates.pop(new)
                candidates_length -= 1
                if new.getNeighborCount() > 0:
                    sender = new
        else:
            sender = self.agents[sender]
            if sender.getNeighborCount() <= 0:
                raise ValueError("No edges exist; invokeInteraction sender")
        
        if receiver == None:
            if init != None:
                candidates.pop(sender)
            while receiver == None:
                if candidates_length <= 0:
                    raise ValueError("No edges exist; invokeINteraction receiver")
                new = random.randint(0,candidates_length - 1)
                new = candidates.pop(new)
                candidates_length -= 1
                if new.getVertex() in sender.getNeighbors():
                    receiver = new
        else:
            receiver = self.agents[receiver]
            if receiver.getNeighborCount() <= 0:
                raise ValueError("No edges exist; invokeInteraction receiver")
        
        if receiver == sender:
            raise ValueError("Duplicate arguments")
        
        current_state = (sender.getState(),receiver.getState())
        if str(current_state) in self.transition_function:
            if str(self.transition_function[str(current_state)]) != str(current_state):
                #log interaction
                self.log.append((sender,receiver))
                sender.changeState(self.transition_function[str(current_state)][0])
                receiver.changeState(self.transition_function[str(current_state)][1])
                return "stateChanged"
            else:
                self.log.append((sender,receiver),True)
                return "null"
        else:
            return False
        #return((sender.getVertex(),receiver.getVertex()))
        
    def renderConfiguration(self, interaction_type = None):
        '''interaction_type represents which type of interaction to show on the graph.
            the default will output two graphs, one where each edge measures regular
            interactions and another where each edge measures null interactions.
            
            The string arguments of regular and null will only output a single graph
            of the respective type and the string argument of merged will output a single
            where each edge measures both null and regular interactions
        '''
        
        node_str = str()
        edge_str = str()
        max_weight = self.log.getCurrentMax('regular')
        min_weight = self.log.getCurrentMin('regular')
        max_null_weight = self.log.getCurrentMax('null')
        min_null_weight = self.log.getCurrentMin('null')
        
        if interaction_type == 'regular':
            maxi = max_weight
            mini = min_weight
            accessor = "count"
        elif interaction_type == 'null':
            maxi = max_null_weight
            mini = min_null_weight 
            accessor = "null_count"
            
        if mini == float('inf'):
            mini = 0
        
        if maxi == -(float('inf')):
            maxi = 1
            mini = 0
            
        if mini == float('inf') and maxi == -(float('inf')):
            maxi= 1
            mini = 0
            
        if mini == maxi:
            maxi = 1
            mini = 0
         
        penstep = 4/(maxi-mini)
        
        redstep = math.floor(127/(maxi))
        greenstep = math.floor(64/(maxi))
        bluestep = math.floor(128/(maxi))
        
        for agent in self.agents:
            vertex = agent.getVertex()
            label = agent.getState()
            node_str += str(vertex)
            node_str += ' [label ="'+str(label)+'",'
            node_str += 'shape=circle,fixedsize=true,fontsize=24,width=0.5]\n'
            
            for neighbor in agent.getNeighbors():
                edge = str((vertex,neighbor))
                value = self.log.interactions[edge][accessor]
                edge_str += vertex + ' -> ' + neighbor
                
                ### --- color logic for edges: grey->red
                red = (128 + (value)*redstep)
                green = (128 - (value)*greenstep)
                blue = (128 - (value)*bluestep)
                color = hex((256**2)*red + 256*green + blue)
                color=color.split('x')
                color=color[1]
                ### ---
                
                edge_str += ' [color="#'+str(color)+'",penwidth='+str(1+penstep*value)+']\n'
            
        return "digraph D { \n " + node_str + "\n" + edge_str + "}"
        
        
#rgb(255, 0, 0)
#rgb(230, 230, 230) grey
