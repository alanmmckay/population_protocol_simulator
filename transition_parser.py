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
        pre = self.parse_state_list()
        self.match(GeneralTokenType.DELIMITER, '-')
        self.match(GeneralTokenType.DELIMITER, '>')
        post = self.parse_state_list()
        self.match(GeneralTokenType.DELIMITER, ')')
        if len(pre) == len(post):
            count = 0
            for state in pre:
                if state not in self.transitions:
                    self.transitions[state] = post[count]
                    count += 1
                else:
                    pass #error
        else:
            pass #error
        
    def parse_state_list(self):
        states = list()
        self.match(GeneralTokenType.DELIMITER, '[')
        states.append(self.match(GeneralTokenType.STRING).getValue())
        next_token = self.scanner.peek()
        while next_token.getValue() == ',':
            print(next_token)
            states.append(self.match(GeneralTokenType.STRING).getValue())
            next_token = self.scanner.peek()
        self.match(GeneralTokenType.DELIMITER, ']')
        return states
        
        
