from parser import Parser
from general_token import GeneralTokenType
from errors import GeneralError

class GraphParser(Parser):
    def __init__(self,scanner):
        Parser.__init__(self, scanner)
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
            next_token = self.match(GeneralTokenType.STRING)
            vertex_set.append(next_token.getValue())
            next_token = self.scanner.peek()
            if next_token.getValue() == ',':
                #execute the loop
                while next_token.getValue() == ',':
                    self.match(GeneralTokenType.DELIMITER, ',')
                    next_token = self.match(GeneralTokenType.STRING)
                    if next_token.getValue() not in vertex_set:
                        vertex_set.append(next_token.getValue())
                        next_token = self.scanner.peek()
                    else:
                        error_msg = "Duplicate Vertex: '"
                        error_msg += next_token.getValue()
                        error_msg += "' found in vertex set."
                        GeneralError(error_msg, self.scanner.getInputString())
            self.match(GeneralTokenType.DELIMITER, '}')
        return vertex_set
    
    
    def parse_edge(self):
        #this usage of match_encapsulator could backfire if this type of data is
        #expecting a value from a subset of the encapsulator superset
        opener = self.match_encapsulator()
        a = self.match(GeneralTokenType.STRING).getValue()
        self.match(GeneralTokenType.DELIMITER, ',')
        b = self.match(GeneralTokenType.STRING).getValue()
        closer = self.match_encapsulator()
        
        if (a not in self.vertex_set) or (b not in self.vertex_set):
            error_msg = "Error in edge. Vertex contained in edge '"
            error_msg += str((a,b))
            error_msg += "' has not been declared within vertex set."
            GeneralError(error_msg, self.scanner.getInputString())
        
        if self.delimiter_set.validateEncapsulator(opener.getValue(), \
            closer.getValue()):
            pair = [(a,b)]
            if opener.getValue() == '{':
                pair.append((b,a))
            return pair
        else:
            error_msg = "Error in edge set. Expecting a matching pair of encapsulating"
            error_msg += " delimiters. Received: '"+str(opener.getValue())+"' and '"
            error_msg += str(closer.getValue())+"'."
            GeneralError(error_msg, self.scanner.getInputString())
            
            
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
    
