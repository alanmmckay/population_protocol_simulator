from agent import Agent

class InteractionLog:
    def __init__(self,edge_list):
        self.transactions = dict()
        self.interactions = dict()
        self.indexes = list()
        
        self.partition = list() #list of edges from the transactions dict
        self.partition_indexes = list() #list of indeces from the indexes list
        self.partition_pointer = None 
        self.partition_interactions = dict() #list of interactions from the interactions dict
        
        self.pointer = -1
        for edge in edge_list:
            self.interactions[str(edge)] = 0
            
    def __setitem__(self,key,pair):
        '''needed input:
            -a graph edge presented as a string tuple
            -the states of both agents prior to the interaction
            #perhaps input could be a tuple composed of the two agent objects
        '''
        if type(pair) == tuple:
            if type(pair[0]) == Agent and type(pair[1]) == Agent:
                if key > self.pointer and type(key) == int:
                    self.pointer = key
                    self.indexes.append(key)
                    self.transactions[key] = dict()  
                    edge = (pair[0].getVertex(),pair[1].getVertex())
                    state = (pair[0].getState(),pair[1].getState())
                    self.transactions[key]['edge'] = str(edge)
                    self.transactions[key]['states'] = state
                    self.interactions[str(edge)] += 1
                else:
                    raise ValueError("InteractionLog key value error")
            else:
                raise ValueError("InteractionLog tuple requires string for edge")
        else:
            raise ValueError("InteractionLog requires tuple")
    
    def append(self,pair):
        self.__setitem__(self,(self.pointer + 1),pair)
        return None
    
    def __getitem__(self,key):
        return self.transactions[key]['states']
    
    def __revert(self,key = None):
        #this should only be called internally
        #should be allowed to empty the partition_indexes list
        index = None
        if key == None:
            key = self.partition_indexes[0]
        while index != key:
            recent_edge = self.partitions.pop()
            index = self.partition_indexes.pop()
            self.indexes.append(index)
            self.partition_interactions[recent_edge] -= 1
        return index
        
    
    def rollback(self,key):
        #if the key is indeed before - chronologically
            #assume dict[max]
            #.rollback[max] should do nothing
            #.rollback[max-1] will take it back to the config before max was added
        if (key in self.indexes) or (key in self.partition_indexes):
            if self.partition_pointer = None or self.partition_pointer > key:
                self.partition_pointer = key
            elif self.partition_pointer < key:
                self.partition_pointer = self.__revert(key)
                
            while self.partition_pointer >= key:
                self.partition_pointer = indexes.pop()
                recent_edge = self.transactions[self.partition_pointer] #a dict
                self.partition.append(recent_edge)
                edge = self.transactions[recent]['edge']
                if edge in self.partition_interactions:
                    self.partition_interactions[edge] += 1
                else:
                    self.partition_interactions[edge] = 1
        else:
            raise ValueError("Invalid key in rollback")
                
        
    
