from graph_scanner import GraphScanner
from token import TokenType
from errors import GeneralError

class GraphParser:
    def __init__(self,scanner):
       self.scanner = scanner
       
    def parse(self):
        return self.parse_graph()
    
    def parse_graph(self):
        self.match(TokenType.DELIMITER, '(')
        vertex_set = self.parse_vertex_set()
        self.match(TokenType.DELIMITER, ',')
        edge_set = self.parse_edge_set()
        self.match(TokenType.DELIMITER, ')')
        return (vertex_set, edge_set)
    
    def parse_vertex_set(self):
        vertex_set = []
        self.match(TokenType.DELIMITER, '{')
        next_token = self.scanner.peek()
        while not next_token.getValue() == '}':
            next_token = self.match_vertex()
            if next_token.getValue() not in vertex_set:
                vertex_set.append(next_token.getValue())
                next_token = self.scanner.peek()
                if next_token.getValue() == ',':
                    self.match(TokenType.DELIMITER, ',')
                    next_token = self.scanner.peek()
            else:
                error_msg = "Duplicate Vertex: '"
                error_msg += next_token.getValue()
                error_msg += "' found in vertex set."
                GeneralError(error_msg, self.scanner.getInputString())
                #raise ValueError("error in parse_vertex_set")
        self.match(TokenType.DELIMITER, '}')
        return vertex_set
        
        
    #let an edge be described as a tuple
    #an unordered pair will be considered a pair of two tuples
    def parse_edge_set(self):
        edge_set = []
        self.match(TokenType.DELIMITER, '{')
        next_token = self.scanner.peek()
        while not next_token.getValue() == '}':
            #perhaps clear the tuple element values
            
            opener = self.match_open_pair()
            a = self.match_vertex().getValue()
            self.match(TokenType.DELIMITER, ',')
            b = self.match_vertex().getValue()
            closer = self.match_close_pair()
            
            if opener.getValue() == '(':
                if not closer.getValue() == ')':
                    error_msg = "Error in edge set. Expecting a closing "
                    error_msg += "parenthesis ')', received: '"
                    error_msg += closer.getValue() + "'"
                    GeneralError(error_msg, self.scanner.getInputString())
                    #raise ValueError('Paren Error in parse edge set')
            if opener.getValue() == '{':
                if not closer.getValue() == '}':
                    error_msg = "Error in edge set. Expecting a closing "
                    error_msg += "curly bracket '}', received: '"
                    error_msg += closer.getValue() + "'"
                    GeneralError(error_msg, self.scanner.getInputString())
                    #raise ValueError('Curly Error in parse edge set')
                else:
                    if (b,a) not in edge_set:
                        edge_set.append((b,a))
                    #else error
                    
            if (a,b) not in edge_set:
                edge_set.append((a,b))
            #else error
            
            next_token = self.scanner.peek()
            if next_token.getValue() == ',':
                self.match(TokenType.DELIMITER, ',')
                next_token = self.scanner.peek()
        self.match(TokenType.DELIMITER, '}')
        return edge_set
        
    def match(self, expected_token_type, expected_token_value = None):
        next_token = self.scanner.nextToken()
        if next_token.getType() == expected_token_type:
            if expected_token_value:
                if next_token.getValue() == expected_token_value:
                    return True
                else:
                    error_msg = "Unexpected token: '"
                    error_msg += str(next_token)
                    error_msg += "' found."
                    GeneralError(error_msg, self.scanner.getInputString())
                    #raise ValueError("error in match")
            else:
                return True
        else:
            error_msg = "Unexpected token type found in parser match"
            GeneralError(error_msg, self.scanner.getInputString())
            #raise ValueError("error in match")


    def match_vertex(self):
        next_token = self.scanner.nextToken()
        if next_token.isString():
            return next_token
        else:
            error_msg = "Unexpected value for vertex: '"
            error_msg += next_token.getValue()
            error_msg += "'"
            GeneralError(error_msg, self.scanner.getInputString())
            #raise ValueError("error in match_vertex")
    
    def match_open_pair(self):
        next_token = self.scanner.nextToken()
        #can probably break out the .isDelimeter() methods here...
        if (next_token.getValue() == '(') or \
           (next_token.getValue() == '{'):
            return next_token
        else:
            raise ValueError("error in match_open_pair")
        
    def match_close_pair(self):
        next_token = self.scanner.nextToken()
        #can probably break out the .isDelimeter() methods here...
        if (next_token.getValue() == ')') or \
           (next_token.getValue() == '}'):
            return next_token
        else:
            raise ValueError("error in match_close_pair")

        
