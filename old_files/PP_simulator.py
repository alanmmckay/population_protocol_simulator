import random
import math

#Agent class properties:
#   FSA list 
#   neighbor list
#   #interaction list

#population protocol class properties
#   agent list
#   transition funcition
#   input map
#   output map
#   alphabet

#transition set schema ->
#  <transition_set> ::= (<transition>, <transitions>)
#  <transitions> ::= <transition> <transitions> | e
#  <transition> ::= (<states>,<states> -> <states>,states>)

class Agent(object):
    def __init__(self, initialState, identification = None):
        self.states = initialState
        self.neighbors = list()
        self.identification = identification
        self.interactionCount = 0
        
    def change_state(self, newState):
        if len(self.states) == len(newState):
            self.states = newState
        else:
            raise ValueError("Error in change_state method")
        
    def get_state(self):
        return self.states
    
    def add_neighbor(self, agent):
        self.neighbors.append(agent)
        
    def get_neighbors(self):
        return self.neighbors
    
    def get_identification(self):
        return self.identification
    
    def incrememnt_interaction_count(self):
        self.interactionCount += 1
        
    def get_interaction_count(self):
        return self.interactionCount
    
    
class PopulationProtocol(object):
    def __init__(self):
        self.population = list()
        self.transitionFunction = dict()
        self.inputMap = dict()
        self.outputMap = dict()
        self.alphabet = dict()
        self.transitionLog = dict()
        self.graphType = 0 #a graph that is restricted is also directed
        self.logSwitch = False
        self.programCounter = 0
        self.agentCount = 0
        
    def add_agent(self, initialState):
        self.population.append(Agent(initialState, self.agentCount))
        self.agentCount += 1
        
    def get_agents(self):
        return self.population
    
    #rule format: [[state1, state2, ..., statex],[newstate1, newstate2, ..., newstatex]]
    #cardinality between these lists need not be the samee
    def create_input_map(self, rules):
        for rule in rules:
            self.inputMap[str(rule[0])] = rule[1]
    
    def create_output_map(self, rules):
        for rule in rules:
            self.outputMap[str(rule[0])] = rule[1]
    
    #rules format: [[[statesOfA], [statesOfB]], [[newStatesOfA],[newStatesOfB]]]
    def create_transition_set(self, transitions):
        for transition in transitions:
            self.transitionFunction[str(transition[0])] = transition[1] #list elements which make new state
            
    def get_transition_set(self):
        return self.transitionFunction
            
    def increment_program_counter(self):
        self.programCounter += 1
        
    def get_program_counter(self):
        return self.programCounter
    
    def toggle_transition_log(self):
        self.logSwitch = not self.logSwitch
        return "Interactions Log has been toggled to "+str(self.transitionLog)
    
    def invoke_interaction(self, sender, receiver):
        self.programCounter = 0
        pair = list()
        pair.append(sender.get_state())
        pair.append(receiver.get_state())
        pairIndex = str(pair)
        nullBool = False
        if pairIndex in self.transitionFunction:
            if self.transitionFunction[pairIndex] == pair:
               nullBool = True
            else:
                sender.change_state(self.transitionFunction[pairIndex][0])
                receiver.change_state(self.transitionFunction[pairIndex][1])
        else:
            nullBool = True
        if self.logSwitch == True:
            self.programCounter += 1
            logEntry = dict()
            logEntry['sender'] = dict()
            logEntry['receiver'] = dict()
            logEntry['sender']['identification'] = sender.get_identification()
            logEntry['sender']['state'] = sender.get_state()
            logEntry['receiver']['identification'] = receiver.get_identification()
            logEntry['receiver']['state'] = receiver.get_state()
            logEntry['step'] = self.programCounter
            logEntry['null?'] = nullBool #maybe index null entries into a seperate list
            logEntry['population'] = self.population
            self.transitionLog[self.programCounter] = logEntry
            
    def draw_graph(self, step = None):
        nodeOutput = str()
        edgeOutput = str()
        if self.logSwitch == True:
            if step == None:
                transition = self.transitionLog[self.programCounter]
            else:
                transition = self.transitionLog[step]
            activeAgents = list()
            activeAgents.append(transition['sender']['identification'])
            activeAgents.append(transition['receiver']['identification'])
        primaryCount = 0
        factored = list()
        for agent in self.population:
            factored.append(agent)
            nodeOutput += str(primaryCount)+' [label="'+str(agent.get_state())+'",shape=circle,fontsize=24,width=0.5]\n'
            if self.graphType == 0:
                secondaryCount = 0
                for otherAgent in self.population:
                    if otherAgent not in factored:
                        edgeOutput += str(primaryCount) + " -> " + str(secondaryCount) + " "
                        edgeOutput += '[arrowhead=none'
                        if self.logSwitch == True:
                            if primaryCount in activeAgents and secondaryCount in activeAgents:
                                edgeOutput += ',color="#532380",penwidth=3'
                            else:
                                edgeOutput += ',color="#808080"'
                        else:
                            edgeOutput += ',color=#808080'
                        edgeOutput += ']\n'
                    secondaryCount += 1
            elif self.graphType == 1:
                #directed !!!NEED TO ADD A GRAPHTYPE SWITCHER FOR TESTING
                for otherAgent in agent.get_neighbors():
                    edgeOutput += str(primaryCount) + " -> " + str(otherAgent.get_identification())
                    if self.logSwitch == True:
                        if primaryCount in activeAgents and secondaryCount in activeAgents:
                            edgeOutput += ',color="#532380",penwidth=3'
                        else:
                            edgeOutput += ',color="#808080"'
                    else:
                        edgeOutput += ',color="#808080"'
                    edgeOutput += ']\n'
                pass
            elif self.graphType == 2:
                #restricted
                
                pass
            primaryCount += 1
        
        print("digraph D {")
        print(nodeOutput)
        print(edgeOutput)
        print("}")

maximum = 0
keeper = dict()

and_protocol = PopulationProtocol()
and_protocol.create_transition_set([ [ [[0],[1]],[[0],[0]] ], [ [[1],[0]], [[0],[0]] ] ])

and_protocol.add_agent([0])
#print(and_protocol.get_agents()[0].get_identification())
and_protocol.add_agent([1])
#print(and_protocol.get_agents()[1].get_identification())
and_protocol.add_agent([1])


and_protocol.toggle_transition_log()
and_protocol.invoke_interaction(and_protocol.get_agents()[0], and_protocol.get_agents()[1])
and_protocol.invoke_interaction(and_protocol.get_agents()[0], and_protocol.get_agents()[2])
#print(and_protocol.get_agents()[1].get_state())
#print(and_protocol.logSwitch)

and_protocol.draw_graph()

'''
for run in range(0,1000): #generate; keep converged population with the most interactions
    and_protocol = PopulationProtocol()
    and_protocol.create_transition_set([ [ [[0],[1]],[[0],[0]] ], [ [[1],[0]], [[0],[0]] ] ])
                                            #^states of a
                                                #^states of b
    for i in range(1, 15):
        and_protocol.add_agent([1], i)
    and_protocol.add_agent([0], (len(and_protocol.get_agents())+1))
    #print(and_protocol.get_agents()[4].get_identification())
    runBool = True
    count = 0
    randAgentA = int()
    randAgentB = int()
    agents = and_protocol.get_agents()
    qty = len(agents)
    transition_set = and_protocol.get_transition_set()
    interactions = dict()
    nullInteractions = dict()
    #might want to track initial state of population

    while runBool == True:
        count += 1
        while True: #generate random interaction
            randAgentA = random.randint(0,qty - 1)
            randAgentB = random.randint(0,qty - 1)
            if randAgentA != randAgentB:
                break
        randAgentA = agents[randAgentA]
        randAgentB = agents[randAgentB]
        pair = list() #generate current pair:
        pair.append(randAgentA.get_state())
        pair.append(randAgentB.get_state())
        pairStr = str(pair)
        #print(str(randAgentA.get_identification()) + ", " + str(randAgentB.get_identification()))
        
        randAgentA.incrememnt_interaction_count()
        randAgentB.incrememnt_interaction_count()
        if pairStr in transition_set:
            newPair = transition_set[pairStr]
            randAgentA.change_state(newPair[0])
            randAgentB.change_state(newPair[1])
            interactions[count] = dict()
            interactions[count]['sender'] = dict()
            interactions[count]['sender']['identification'] = randAgentA.get_identification()
            interactions[count]['sender']['state'] = randAgentA.get_state()
            interactions[count]['receiver'] = dict()
            interactions[count]['receiver']['identification'] = randAgentB.get_identification()
            interactions[count]['receiver']['state'] = randAgentB.get_state()
        else:
            nullInteractions[count] = dict()
            nullInteractions[count]['sender'] = dict()
            nullInteractions[count]['sender']['identification'] = randAgentA.get_identification()
            nullInteractions[count]['sender']['state'] = randAgentA.get_state()
            nullInteractions[count]['receiver'] = dict()
            nullInteractions[count]['receiver']['identification'] = randAgentB.get_identification()
            nullInteractions[count]['receiver']['state'] = randAgentB.get_state()
        for agent in agents: #check for convergence
            #while there still exists a one, run random interactions:
            if agent.get_state()[0] == 1:#if not converged initiate random interaction
                break
            if count > maximum:
                keeper['count'] = count
                keeper['null'] = nullInteractions
                keeper['nom'] = interactions
                keeper['agents'] = and_protocol.get_agents() 
                maximum = count
            #print(count)
            
            runBool = False
    

#print(and_protocol.get_transition_set())
#print(len(agents))

#print("Program Counter: "+str(keeper['count'])) 
#print(keeper['nom'])
#print(len(keeper['nom']))
print(len(keeper['null']))

agent_map = {}
for i in range(1,16):
    agent_map[i] = dict()
    for k in range(1,16):
        if k != i:
            agent_map[i][k] = 0


for interaction in keeper['null']:
    sender = keeper['null'][interaction]['sender']['identification']
    receiver = keeper['null'][interaction]['receiver']['identification']
    agent_map[sender][receiver] += 1

null_agent_map = agent_map
#agent_map = {}
#for i in range(1,11):
    #agent_map[i] = dict()
    #for k in range(1,11):
        #if k != i:
            #agent_map[i][k] = 0

    
#for interaction in keeper['nom']:
    #sender = keeper['nom'][interaction]['sender']['identification']
    #receiver = keeper['nom'][interaction]['receiver']['identification']
    #agent_map[sender][receiver] += 1
    
def rgb2hex(r,g,b):
    return hex((256**2)*r + 256*g + b)

nom_agent_map = agent_map
nodes = str()
edges = list()
edgeweights = list()
track = list()
maxi = 0
for i in agent_map:
    intcount = int()
    for agent in keeper['agents']:
        if agent.get_identification() == i:
            intcount = agent.get_interaction_count()
    #nodes += str(i) + ' [label="Interactions: '+str(intcount)+'",shape=circle,width='+str(0.5+(0.25*intcount))+ ',fontsize=24]\n'
    nodes += str(i) + ' [label="Total\\nInteractions: '+str(intcount)+'",shape=circle,fontsize=24,width=0.5]\n'
    track.append(i)
    for k in agent_map[i]:
        weight = 0
        weight += agent_map[i][k]
        weight += agent_map[k][i]
        if weight > maxi:
            maxi = weight
        if k not in track:
            edges.append(str(i) + " -> " + str(k)) # + str(weight) + " [arrowhead=none]\n"
            edgeweights.append(weight)
            
edgestr = str()
reds = [128]
greens = [128]
blues = [128]
redstep = math.floor(127/maxi)
greenstep = math.floor(64/maxi)
bluestep = math.floor(128/maxi)
penwidth = [1]
penwidthstep = 15/maxi
for i in range(0,maxi):
    reds.append(128 + (i+1)*redstep)
    greens.append(128 - (i+1)*greenstep)
    blues.append(128 - (i+1)*bluestep)
    penwidth.append(1+i*penwidthstep)
counter = 0

for i in edges:
    #color = rgb2hex(255,greens[edgeweights[counter]-1],50)
    color = rgb2hex(reds[edgeweights[counter]],greens[edgeweights[counter]],blues[edgeweights[counter]])
    color = color.split('x')
    color = color[1]
    edgestr +=  str(i) + ' [color="#'+color+'",arrowhead=none,penwidth='+str(penwidth[edgeweights[counter]])+']\n'
    #edgestr +=  str(i) + ' [color="#'+color+'",arrowhead=none,label=" '+str(edgeweights[counter])+'",penwidth='+str(penwidth[edgeweights[counter]])+']\n'
    #edgestr +=  str(i) + ' [color="#'+color+'",arrowhead=none,label="null\\nInteractions: '+str(edgeweights[counter])+'"]\n'
    counter+=1
    
print("digraph D {")
print(nodes)
print(edgestr)
print("}")
'''
