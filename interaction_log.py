from agent import Agent

class InteractionLog:
    def __init__(self,edge_list):
        self.transactions = dict()
        self.interactions = dict()
        self.indexes = list()
        
        self.partition = list()
        self.partition_indexes = list()
        self.partition_pointer = None
        self.partition_interactions = dict()
        
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
    
    def __revert(self,key):
        #this should only be called internally
        recent = self.partitions.pop()
        index = self.partition_indexes.pop()
        self.indexes.append(index)
        self.partition_interactions[recent] -= 1
        while recent <= key:
            recent = self.partitions.pop()
            index = self.partition_indexes.pop()
            self.indexes.append(index)
            self.partition_interactions[recent] -= 1
        return index
        
    
    def rollback(self,key):
        if self.partition_pointer = None or self.partition_pointer > key:
            self.partition_pointer = key
        else:
            self.partition_pointer = self.__revert(key)
        recent = indexes.pop()
        while recent >= key:
            self.partition_indexes.append(recent)
            self.partition.append(self.transactions[recent])
            edge = self.transactions[recent]['edge']
            if edge in self.partition_interactions:
                self.partition_interactions[edge] += 1
            else:
                self.partition_interactions[edge] = 1
            recent = indexes.pop()
        pass
        
    
