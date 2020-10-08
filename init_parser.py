from parser import Parser
from general_token import GeneralTokenType
from errors import GeneralError

class InitParser(Parser):
    def __init__(self,scanner,graph_vertices):
        Parser.__init__(self,scanner)
        self.existing_vertices = graph_vertices
        self.vertex_set = list()
        self.vertex_dict = dict()
        #need to have a dictionary which tracks the state of each unique vertex
        
    def parse(self):
        return self.parse_initializer()

    def parse_initializer(self):
        self.match(GeneralTokenType.DELIMITER, '(')
        self.parse_state_associations()#
        self.match(GeneralTokenType.DELIMITER, ')')
        return self.vertex_dict
        
    def parse_state_associations(self):
        self.parse_state_association()#
        next_token = self.scanner.peek()
        while next_token.getValue() == ',':
            self.match(GeneralTokenType.DELIMITER, ',')
            self.parse_state_association()#
            next_token = self.scanner.peek()
        return True
    
    def parse_state_association(self):
        self.match(GeneralTokenType.DELIMITER, '{')
        initialized_vertices = self.parse_vertex_set()
        self.match(GeneralTokenType.DELIMITER, ':')
        state_list = self.parse_state_list()
        self.match(GeneralTokenType.DELIMITER, '}')
        #loop and add to dict
        for vertex in initialized_vertices:
            self.vertex_dict[vertex] = state_list
        return True
        
    def parse_vertex_set(self):
        self.match(GeneralTokenType.DELIMITER, '{')
        initialized_vertices = list()
        initialized_vertices.append(self.parse_vertex())
        next_token = self.scanner.peek()
        while next_token.getValue() == ',':
            self.match(GeneralTokenType.DELIMITER, ',')
            initialized_vertices.append(self.parse_vertex())
            next_token = self.scanner.peek()
        self.match(GeneralTokenType.DELIMITER, '}')
        return initialized_vertices
        
    def parse_vertex(self):
        next_token = self.match(GeneralTokenType.STRING)
        if next_token.getValue() in self.existing_vertices:
            if next_token.getValue() not in self.vertex_set:
                self.vertex_set.append(next_token.getValue())
                return next_token.getValue()
            else:
                GeneralError("Error in parse_vertex")
        else:
            GeneralError("Error in parse_vertex")
        
    def parse_state_list(self):
        state_list = list()
        self.match(GeneralTokenType.DELIMITER, '[')
        next_token = self.match(GeneralTokenType.STRING)
        state_list.append(next_token.getValue())
        next_token = self.scanner.peek()
        while next_token.getValue() == ',':
            self.match(GeneralTokenType.DELIMITER, ',')
            next_token = self.match(GeneralTokenType.STRING)
            state_list.append(next_token.getValue())
            next_token = self.scanner.peek()
        self.match(GeneralTokenType.DELIMITER, ']')
        return state_list
