from parser import Parser
from general_token import GeneralTokenType
from errors import GeneralError

class InitParser(Parser):
    def __init__(self,scanner):
        Parser.__init__(self,scanner)
        self.vertex_set = list()
        self.vertex_dict = dict()
        #need to have a dictionary which tracks the state of each unique vertex
        
    def parse(self):
        return self.parse_initializer()

    def parse_initializer(self):
        self.match(GeneralTokenType.DELIMITER, '(')
        parse_state_associations()#
        self.match(GeneralTokenType.DELIMITER, ')')
        
    def parse_state_associations(self):
        parse_state_association()#
        next_token = self.scanner.peek()
        if next_token.getValue() == ',':
            while next_token.getValue() == ',':
                self.match(GeneralTokenType.DELIMITER, ',')
                parse_state_association()#
                next_token = self.scanner.peek()
        return None#
    
    def parse_state_association(self):
        self.match(GeneralTokenType.DELIMITER, '{')
        self.parse_vertex_set()#
        self.match(GeneralTokenType.DELIMITER, ':')
        self.parse_state_list()#
        self.match(GeneralTokenType.DELIMITER, '}')
        
    def parse_vertex_set(self):
        self.match(GeneralTokenType.DELIMITER, '{')
        self.match(GeneralTokenType.STRING)#
        next_token = self.scanner.peek()
        if next_token.getValue() == ',':
            while next_token.getValue() == ',':
                self.match(GeneralTokenType.DELIMITER, ',')
                self.match(GeneralTokenType.STRING)#
                next_token = self.scanner.peek()
        self.match(GeneralTokenType.DELIMITER, '}')
        
    def parse_state_list(self):
        self.match(GeneralTokenType.DELIMITER, '[')
        self.match(GeneralTokenType.STRING)#
        next_token = self.scanner.peek()
        if next_token.getValue() == ',':
            while next_token.getValue() == ',':
                self.match(GeneralTokenType.DELIMITER, ',')
                self.match(GeneralTokenType.STRING)#
                next_token = self.scanner.peek()
        self.match(GeneralTokenType.DELIMITER, ']')
