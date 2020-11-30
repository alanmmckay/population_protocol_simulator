from agent import Agent

class InteractionLog:
    def __init__(self,edge_list):
        self.transactions = dict()
        self.interactions = dict()
        self.null_transactions = dict()
        self.indexes = list()
        self.null_indexes = list()
        
        self.partition = list() #list of interactions from the transactions dict
        self.null_partition = list()
        
        self.partition_indexes = list()
        self.null_partition_indexes = list()
        
        self.pointer = -1
        
        for edge in edge_list:
            self.interactions[str(edge)] = dict()
            self.interactions[str(edge)]['count'] = 0
            self.interactions[str(edge)]['null_count'] = 0
            
        infinity = float('inf')
        self.count_max = [-(infinity)]
        self.null_count_max = [-(infinity)]
        self.count_min = [infinity]
        self.null_count_min = [infinity]
            
            
    def __setitem__(self,key,pair):
        '''
        It may seem odd to have a combination of append and the ability to set a numeric key.
        The primary function is to use the append where the pointer moves by one each time.
        It may be necessary to allow this __setitem__ method though if we want to allow a
        user to place expected configurations.
        '''
        if (key > self.pointer) and (type(key) == int):
            if type(pair) == tuple:
                if type(pair[0]) == Agent and type(pair[1]) == Agent:
                    self.pointer = key
                    self.indexes.append(key)
                    self.transactions[key] = dict()  
                    edge = (pair[0].getVertex(),pair[1].getVertex())
                    state = (pair[0].getState(),pair[1].getState())
                    self.transactions[key]['pair'] = pair
                    self.transactions[key]['states'] = state
                    self.interactions[str(edge)]['count'] += 1
                    #print(self.interactions[str(edge)])
                    
                    ### --- max counter
                    if self.count_max[-1] <= self.interactions[str(edge)]['count']:
                        self.count_max.append(self.interactions[str(edge)]['count'])
                        
                    ### --- min counter
                    if self.count_min[-1] >= self.interactions[str(edge)]['count']:
                        self.count_min.append(self.interactions[str(edge)]['count'])
                        
                else:
                    raise ValueError("InteractionLog tuple requires string for edge")
            else:
                raise ValueError("InteractionLog requires tuple")
        else:
            raise ValueError("InteractionLog key value error")
    
    
    def append(self, pair, null = False):
        edge = (pair[0].getVertex(),pair[1].getVertex())
        if type(pair) == tuple:
            if type(pair[0]) == Agent and type(pair[1]) == Agent:
                if null == False:
                    self.__setitem__((self.pointer + 1), pair)
                else:
                    edge = (pair[0].getVertex(),pair[1].getVertex())
                    self.pointer += 1
                    self.null_indexes.append(self.pointer)
                    self.null_transactions[self.pointer] = pair
                    self.interactions[str(edge)]['null_count'] += 1
                    
                    ### --- max counter
                    if self.null_count_max[-1] <= self.interactions[str(edge)]['null_count']:
                        self.null_count_max.append(self.interactions[str(edge)]['null_count'])
                        
                    ### --- min counter
                    if self.null_count_min[-1] >= self.interactions[str(edge)]['null_count']:
                        self.null_count_min.append(self.interactions[str(edge)]['null_count'])
                    
            else:
                raise ValueError("InteractionLog tuple requires two Agent types")
        else:
            raise ValueError("InteractionLog requires tuple")
    
    def __getitem__(self,key):
        if key in self.transactions:
            return self.transactions[key]['states']
        elif key in self.partition_indexes:
            self.rollback(key)
            return self.transactions[key]['states']
    
    
    '''A function which takes a key as an argument and restores a population
        protocol's configuration from a rolled-back state. If no key is provided,
        a population protocol will be fully restored'''
    def restore(self,key = None):
        if (key in self.partition_indexes) or (key in self.null_partition_indexes) \
            or (key == None):
            
            if key == None:
                if len(self.partition_indexes) > 0:
                    index = self.partition_indexes[0]
                else:
                    index = -1
                if len(self.null_partition_indexes) > 0:
                    null_index = self.null_partition_indexes[0]
                else:
                    null_index = -1
                key = max(index,null_index)
            
            while self.pointer <= key:
                if len(self.partition_indexes) > 0:
                    index = self.partition_indexes.pop()
                else:
                    index = -1
                if len(self.null_partition_indexes) > 0:
                    null_index = self.null_partition_indexes.pop()
                else:
                    null_index = -1
                    
                if index > null_index:
                    #reappend index to indexes list
                    self.indexes.append(index)
                    #pop the transaction off the partition list
                    transaction = self.partition.pop()
                    pair = transaction[0]
                    edge = (pair[0].getVertex(),pair[1].getVertex())
                    later_states = transaction[1]
                    former_states = (pair[0].getState(),pair[1].getState())
                    #add the transaction back to the transaction dictionary
                    self.transactions[index] = dict()
                    self.transactions[index]['pair'] = pair
                    self.transactions[index]['states'] = former_states
                    #revert the state of the agents
                    pair[0].changeState(later_states[0])
                    pair[1].changeState(later_states[1])
                    #re-increment the interactions count
                    self.interactions[str(edge)]['count'] += 1
                    
                    ### --- max counter
                    if self.count_max[-1] <= self.interactions[str(edge)]['count']:
                        self.count_max.append(self.interactions[str(edge)]['count'])
                        
                    ### --- min counter
                    if self.count_min[-1] >= self.interactions[str(edge)]['count']:
                        self.count_min.append(self.interactions[str(edge)]['count'])
                        
                    if null_index != -1:
                        self.null_partition_indexes.append(null_index)
                    #move the pointer
                    self.pointer = index
                    
                elif null_index < index:
                    #reappend index to indexes list
                    self.null_indexes.append(null_index)
                    #pop the transaction off the partition list
                    pair = self.null_partition.pop()
                    self.null_transactions.append(pair)
                    edge = (pair[0].getVertex(),pair[1].getVertex())
                    #re-increment the interactions count
                    self.interactions[str(edge)]['null_count'] += 1
                    
                    ### --- max counter
                    if self.null_count_max[-1] <= self.interactions[str(edge)]['null_count']:
                        self.null_count_max.append(self.interactions[str(edge)]['null_count'])
                        
                    ### --- min counter
                    if self.null_count_min[-1] >= self.interactions[str(edge)]['null_count']:
                        self.null_count_min.append(self.interactions[str(edge)]['null_count'])
                        
                    if index != -1:
                        self.partition_indexes.append(index)
                    #move the pointer
                    self.pointer = null_index
                    
                else:
                    raise ValueError("Error in restore")
            
        
    '''A function which takes a key as an argument and returns a population
        protocol to the configuration which exists closest to the key'''
    def rollback(self,key):
        if (key in self.partition_indexes) or (key in self.null_partition_indexes):
            #call restore
            self.restore(key)

        if (key in self.indexes) or (key in self.null_indexes):
            print(key)
            while self.pointer > key:
                #Grab the most recent index off both index containers
                if len(self.indexes) > 0:
                    index = self.indexes.pop()
                else:
                    index = -1
                if len(self.null_indexes) > 0:
                    null_index = self.null_indexes.pop()
                else:
                    null_index = -1
                
                if index > null_index:
                    #Assign index to its respective partition container
                    self.partition_indexes.append(index)
                    #pop the transaction at index out of the dictionary
                    transaction = self.transactions.pop(index)
                    pair = transaction['pair']
                    later_states = (pair[0].getState(),pair[1].getState())
                    former_states = transaction['states']
                    #change the state of the two involved agents
                    pair[0].changeState(former_states[0])
                    pair[1].changeState(former_states[1])
                    #place this entry into its respective partitions dictionary
                    self.partition.append((pair,later_states))
                    #factor the interaction count
                    edge = (pair[0].getVertex(),pair[1].getVertex())
                    
                    ### --- max counter
                    if self.count_max[-1] == self.interactions[str(edge)]['count']:
                        self.count_max.pop()
                        
                    ### --- min counter
                    if self.count_min[-1] == self.interactions[str(edge)]['count']:
                        self.count_min.pop()
                    
                    self.interactions[str(edge)]['count'] -= 1
                    if null_index != -1:
                        self.null_indexes.append(null_index)
                    self.pointer = index
                elif null_index > index:
                    #Assign index to its respective partition container
                    self.null_partition_indexes.append(null_index)
                    pair = self.null_transactions.pop(null_index)
                    #no need to change the state of the two involved agents..
                    #thus place this entry into it's respective partitions dictionary
                    self.null_partition.append(pair)
                    #factor the interaction count
                    edge = (pair[0].getVertex(),pair[1].getVertex())
                    
                    ### --- max counter
                    if self.null_count_max[-1] == self.interactions[str(edge)]['null_count']:
                        self.null_count_max.pop()
                        
                    ### --- min counter
                    if self.null_count_min[-1] == self.interactions[str(edge)]['null_count']:
                        self.null_count_min.pop()
                        
                    self.interactions[str(edge)]['null_count'] -= 1
                    if index != -1:
                        self.indexes.append(index)
                    self.pointer = null_index
                else:
                    raise ValueError("Error in rollback")
        else:
            raise ValueError("Invalid key in rollback")
        
    def getCurrentMax(self, interaction_type):
        if interaction_type == 'regular':
            return self.count_max[-1]
        elif interaction_type == 'null':
            return self.null_count_max[-1]
        
    def getCurrentMin(self, interaction_type):
        if interaction_type == 'regular':
            return self.count_min[-1]
        elif interaction_type == 'null':
            return self.null_count_min[-1]
        
