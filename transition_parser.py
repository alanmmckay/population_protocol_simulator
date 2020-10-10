from parser import Parser
from general_token import GeneralTokenType
from errors import GeneralError

class TransitionParser(Parser):
    def __init__(self,scanner):
        Parser.__init__(self,scanner)
        self.transitions = dict()
        
    def parse(self):
        return self.parse_transition_set()
    
    def parse_transition_set(self):
        self.match(GeneralTokenType.DELIMITER, '{')
        self.parse_transition()#
        next_token = self.scanner.peek()
        while next_token.getValue() == ',':
            self.match(GeneralTokenType.DELIMITER, ',')
            self.parse_transition()#
            next_token = self.scanner.peek()
        self.match(GeneralTokenType.DELIMITER, '}')
        return self.transitions
        
    def parse_transition(self):
        self.match(GeneralTokenType.DELIMITER, '(')
        next_token = self.scanner.peek()
        if next_token.getValue() == '[':
            self.parse_state_lists()
        else: 
            pre = self.match(GeneralTokenType.STRING).getValue()
            self.match(GeneralTokenType.DELIMITER, '-')
            self.match(GeneralTokenType.DELIMITER, '>')
            post = self.match(GeneralTokenType.STRING).getValue()
            self.transitions[pre] = post
        self.match(GeneralTokenType.DELIMITER, ')')
        
        
    def parse_state_lists(self):
        pre = self.parse_state_list()
        self.match(GeneralTokenType.DELIMITER, '-')
        self.match(GeneralTokenType.DELIMITER, '>')
        post = self.parse_state_list()
        self.transitions[str(pre)] = post
        
    def parse_state_list(self):
        states = list()
        self.match(GeneralTokenType.DELIMITER, '[')
        states.append(self.match(GeneralTokenType.STRING).getValue())
        next_token = self.scanner.peek()
        while next_token.getValue() == ',':
            self.match(GeneralTokenType.DELIMITER, ',')
            states.append(self.match(GeneralTokenType.STRING).getValue())
            next_token = self.scanner.peek()
        self.match(GeneralTokenType.DELIMITER, ']')
        return states
        
    
