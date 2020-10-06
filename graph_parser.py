from general_token import GeneralTokenType
from errors import GeneralError

class GraphParser:
    def __init__(self,scanner):
       self.scanner = scanner
       self.vertex_set = list()
       
    def parse(self):
        return self.parse_graph()
    
    def parse_graph(self):
        self.match(GeneralTokenType.DELIMITER, '(')
        self.vertex_set = self.parse_vertex_set()
        self.match(GeneralTokenType.DELIMITER, ',')
        edge_set = self.parse_edge_set()
        self.match(GeneralTokenType.DELIMITER, ')')
        return (self.vertex_set, edge_set)
    
    def parse_vertex_set(self):
        vertex_set = []
        self.match(GeneralTokenType.DELIMITER, '{')
        next_token = self.scanner.peek()
        #prime the loop
        if next_token.getValue() != '}':
            next_token = self.match_vertex()
            vertex_set.append(next_token.getValue())
            next_token = self.scanner.peek()
            if next_token.getValue() == ',':
                #execute the loop
                while next_token.getValue() == ',':
                    self.match(GeneralTokenType.DELIMITER, ',')
                    next_token = self.match_vertex()
                    if next_token.getValue() not in vertex_set:
                        vertex_set.append(next_token.getValue())
                        next_token = self.scanner.peek()
                    else:
                        error_msg = "Duplicate Vertex: '"
                        error_msg += next_token.getValue()
                        error_msg += "' found in vertex set."
                        GeneralError(error_msg, self.scanner.getInputString())
                        #raise ValueError("error in parse_vertex_set")
            self.match(GeneralTokenType.DELIMITER, '}')
        return vertex_set
    
    def parse_edge(self):
        opener = self.match_open_pair()
        a = self.match_vertex().getValue()
        self.match(GeneralTokenType.DELIMITER, ',')
        b = self.match_vertex().getValue()
        closer = self.match_close_pair()
        
        if (a not in self.vertex_set) or (b not in self.vertex_set):
            error_msg = "Error in edge. Vertex contained in edge '"
            error_msg += str((a,b))
            error_msg += "' has not been declared within vertex set."
            GeneralError(error_msg, self.scanner.getInputString())
            #raise ValueError("edge vertex not in vertex set")
        
        if opener.getValue() == '(':
            if closer.getValue() == ')':
                return [(a,b)]
            else:
                error_msg = "Error in edge set. Expecting a closing "
                error_msg += "parenthesis ')', received: '"
                error_msg += closer.getValue() + "'"
                GeneralError(error_msg, self.scanner.getInputString())
                #raise ValueError('Paren Error in parse edge set')
        elif opener.getValue() == '{':
            if closer.getValue() == '}':
                return [(a,b),(b,a)]
            else:
                error_msg = "Error in edge set. Expecting a closing "
                error_msg += "curly bracket '}', received: '"
                error_msg += closer.getValue() + "'"
                GeneralError(error_msg, self.scanner.getInputString())
                #raise ValueError('Curly Error in parse edge set')
                
                
    #let an edge be described as a tuple
    #an unordered pair will be considered a pair of two tuples
    def parse_edge_set(self):
        edge_set = []
        self.match(GeneralTokenType.DELIMITER, '{')
        next_token = self.scanner.peek()
        if next_token.getValue() != '}':
            next_token = self.parse_edge()#perhaps rename next_token variable
            
            for pair in next_token:
                if pair not in edge_set:
                    edge_set.append(pair)
                else:
                    error_msg = "Duplicate edge: '"
                    error_msg += pair
                    error_msg += "' found in edge set."
                    GeneralError(error_msg, self.scanner.getInputString())
                    
            next_token = self.scanner.peek()
        if next_token.getValue() == ',':
            while next_token.getValue() == ',':
                #execute the loop
                self.match(GeneralTokenType.DELIMITER, ',')
                next_token = self.parse_edge()
                
                for pair in next_token:
                    if pair not in edge_set:
                        edge_set.append(pair)
                    else:
                        error_msg = "Duplicate edge: '"
                        error_msg += pair
                        error_msg += "' found in edge set."
                        GeneralError(error_msg, self.scanner.getInputString())

                next_token = self.scanner.peek()
        self.match(GeneralTokenType.DELIMITER, '}')
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
            error_msg = "Error in within edge set. Expecting an opening "
            error_msg += "delimiter. Received '"
            error_msg += next_token.getValue()
            error_msg += "' instead"
            GeneralError(error_msg, self.scanner.getInputString())
            #raise ValueError("error in match_open_pair")
        
    def match_close_pair(self):
        next_token = self.scanner.nextToken()
        #can probably break out the .isDelimeter() methods here...
        if (next_token.getValue() == ')') or \
           (next_token.getValue() == '}'):
            return next_token
        else:
            error_msg = "Error in within edge set. Expecting an closing "
            error_msg += "delimiter. Received '"
            error_msg += next_token.getValue()
            error_msg += "' instead"
            GeneralError(error_msg, self.scanner.getInputString())
            #raise ValueError("error in match_close_pair")

        
