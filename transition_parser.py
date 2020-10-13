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
        pre = self.parse_state_tuple()
        self.match(GeneralTokenType.DELIMITER, '-')
        self.match(GeneralTokenType.DELIMITER, '>')
        post = self.parse_state_tuple()
        self.match(GeneralTokenType.DELIMITER, ')')
        self.transitions[str((pre[0],pre[1]))] = (post[0],post[1])
        return True
    
    def parse_state_tuple(self):
        self.match(GeneralTokenType.DELIMITER, '(')
        a = self.match(GeneralTokenType.STRING).getValue()
        self.match(GeneralTokenType.DELIMITER, ',')
        b = self.match(GeneralTokenType.STRING).getValue()
        self.match(GeneralTokenType.DELIMITER, ')')
        return (a,b)
