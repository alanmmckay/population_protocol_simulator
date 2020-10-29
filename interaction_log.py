from agent import Agent

class InteractionLog:
    def __init__(self,edge_list):
        self.transactions = dict()
        self.interactions = dict()
        self.indexes = list()
        
        self.partition = list() #list of interactions from the transactions dict
        self.partition_indexes = list() #list of indeces from the indexes list
        self.partition_interactions = dict() #list of interactions from the interactions dict
        self.partitioned_null_indexes = list()
        
        self.null_interactions = dict()
        self.null_transactions = list()
        self.null_indexes = list()
        
        self.pointer = -1
        self.partition_pointer = None 
        for edge in edge_list:
            self.interactions[str(edge)] = 0
            self.null_interactions[str(edge)] = 0
            
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
                    self.transactions[key]['edge'] = str(edge)
                    self.transactions[key]['states'] = state
                    self.interactions[str(edge)] += 1
                else:
                    raise ValueError("InteractionLog tuple requires string for edge")
            else:
                raise ValueError("InteractionLog requires tuple")
        else:
            raise ValueError("InteractionLog key value error")
    
    def append(self,pair, null = False):
        if null == False:
            self.__setitem__(self,(self.pointer + 1),pair)
        else:
            if type(pair) == tuple:
                if type(pair[0]) == Agent and type(pair[1]) == Agent:
                    edge = (pair[0].getVertex(),pair[1].getVertex())
                    self.pointer += 1
                    self.null_interactions[str(edge)] += 1
                    self.null_indexes.append(self.pointer)
                    self.null_transactions.append(str(edge))
                else:
                    raise ValueError("InteractionLog tuple requires string for edge")
            else:
                raise ValueError("InteractionLog requires tuple")
        return None
    
    def __getitem__(self,key):
        if key in self.transactions:
            return self.transactions[key]['states']
        elif key in self.partition_indexes:
            self.rollback(key)
            return self.transactions[key]['states']
    
    def restore(self,key = None):
        #perhaps validate the key??
        index = None
        if key == None:
            if len(self.partition_indexes) > 0:
                key = self.partition_indexes[0]
        while index != key:
            recent_edge_data = self.partition.pop()
            index = self.partition_indexes.pop()
            self.indexes.append(index)
            self.partition_interactions[recent_edge_data['edge']] -= 1
            if self.partition_interactions[recent_edge_data['edge']] == 0:
                self.partition_interactions.pop(recent_edge_data['edge'])
        return index
        
    def rollback(self,key):
        #if the key is indeed before - chronologically
            #assume dict[max]
            #.rollback[max] should do nothing
            #.rollback[max-1] will take it back to the config before max was added
        if (key in self.indexes) or (key in self.partition_indexes):
            if self.partition_pointer == None or self.partition_pointer > key:
                self.partition_pointer = key
            elif self.partition_pointer < key:
                self.partition_pointer = self.restore(key)
                
            while self.partition_pointer >= key:
                self.partition_pointer = self.indexes.pop()
                recent_edge_data = self.transactions[self.partition_pointer] #a dict
                self.partition.append(recent_edge_data)
                edge = self.transactions[recent]['edge']
                if edge in self.partition_interactions:
                    self.partition_interactions[edge] += 1
                else:
                    self.partition_interactions[edge] = 1
        else:
            raise ValueError("Invalid key in rollback")
                
        
    
        
    
