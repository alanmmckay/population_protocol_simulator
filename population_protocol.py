import random
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
           if agent.getState() != value:
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
            else:
                self.log.append((sender,receiver),True)
        else:
            return False
            
        return((sender.getVertex(),receiver.getVertex()))
        
        
