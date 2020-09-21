from graph_scanner import GraphScanner
from graph_token import GraphTokenType

class GraphParser:
    def __init__(self,scanner):
       self.scanner = scanner
       
    def parse(self):
        return self.parse_graph()
    
    def parse_graph(self):
        self.match(GraphTokenType.OPENPAREN)
        vertex_set = self.parse_vertex_set()
        self.match(GraphTokenType.COMMA)
        edge_set = self.parse_edge_set()
        self.match(GraphTokenType.CLOSEPAREN)
        return [vertex_set, edge_set]
    
    def parse_vertex_set(self):
        vertex_set = []
        self.match(GraphTokenType.OPENCURLY)
        next_token = self.scanner.peek()
        while not next_token.isCloseCurly():
            next_token = self.match_vertex()
            if next_token not in vertex_set:
                vertex_set.append(next_token)
                next_token = self.scanner.peek()
                if next_token.isComma():
                    self.match(GraphTokenType.COMMA)
                    next_token = self.scanner.peek()
            else:
                raise ValueError("error in parse_vertex_set")
        self.match(GraphTokenType.CLOSECURLY)
        return vertex_set
        
        
    #let an edge be described as a tuple
    #an unordered pair will be considered a pair of two tuples
    def parse_edge_set(self):
        edge_set = []
        self.match(GraphTokenType.OPENCURLY)
        next_token = self.scanner.peek()
        while not next_token.isCloseCurly():
            #perhaps clear the tuple element values
            
            opener = self.match_open_pair()
            a = match_vertex()
            self.match(GraphTokenType.COMMA)
            b = match_vertex()
            closer = self.match_close_pair()
            
            if (a,b) not in edge_set:
                edge_set.append((a, b))
                if opener.isOpenCurly():
                    if (b,a) not in edge_set:
                        edge_set.append((b, a))
                        if not closer.isCloseCurly():
                            raise ValueError("Curly Error in parse edge set")
                    else:
                        raise ValueError("Duplicate unordered pair in parse \
                              edge set")
                if opener.isOpenParen():
                    if not closer.isOpenParen():
                        raise ValueError("Paren Error in parse edge set")
            else:
                raise ValueError("Duplicate pair in parse edge set")
            
            next_token = self.scanner.peek()
            if next_token.isComma():
                self.match(GraphTokenType.COMMA)
                next_token = self.scanner.peek()
        self.match(GraphTokenType.CLOSECURLY)
        return edge_set
        
    def match(self, expected_token_type):
        next_token = self.scanner.nextToken()
        if next_token.getType() == expected_token_type:    
            return True
        else:
            raise ValueError("error in match")

    def match_vertex(self):
        next_token = self.scanner.nextToken()
        if next_token.isVertex():
            return next_token
        else:
            raise ValueError("error in match_vertex")
    
    def match_open_pair(self):
        next_token = self.scanner.nextToken()
        #can probably break out the .isDelimeter() methods here...
        if (next_token.getType() == GraphTokenType.OPENPAREN) or \
           (next_token.getType() == GraphTokenType.OPENCURLY):
            return next_token
        else:
            raise ValueError("error in match_open_pair")
        
    def match_close_pair(self):
        next_token = self.scanner.nextToken()
        #can probably break out the .isDelimeter() methods here...
        if (next_token.getType() == GraphTokenType.CLOSEPAREN) or \
           (next_token.getType() == GraphTokenType.CLOSECURLY):
            return True
        else:
            raise ValueError("error in match_close_pair")

        
