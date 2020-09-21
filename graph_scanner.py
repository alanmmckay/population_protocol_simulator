from graph_token import GraphToken, GraphTokenType
from helper_functions import file_input

graph_data = file_input('graph')

print(graph_data)

#case scheme:
#-objects which can be referenced externally use camel case
#-objects which are referenced internally use underscores

delimiters = ["{","}","(",")",","]
valid_vertex = list()
for i in range(97,123):
    valid_vertex.append(chr(i))
for i in range(0,10):
    valid_vertex.append(i)

class GraphScanner:
    def __init__(self, graph_str):
        self.graph_str = graph_str
        #-possibly convert this string to another data structure that is faster
        # to parse.
        self.pos = 0
        self.maxPos = len(graph_str)
        self.look_ahead = None
        self.line = 1
        
    def peek(self):
        if not self.look_ahead:
            self.look_ahead = self.nextToken()
        return self.look_ahead
    
    def nextToken(self):
        if self.look_ahead:
            next_token = self.look_ahead
            self.look_ahead = None
            return next_token
        else:
            return self.getNextToken()
       
    def getVertex(self):
        #while the next token is an alpha numeric character
        vertex_string = str()
        offset = self.pos
        while True:
            if self.graph_str[offset] in valid_vertex:
                vertex_string += self.graph_str[offset]
                offset += 1
            else:
                return vertex_string
    
    def produceToken(self):
        if self.pos >= self.maxPos:
            return GraphToken(GraphTokenType.EOF)
        elif self.graph_str[self.pos] in delimiters:
            #Adhocery: {
            if self.graph_str[self.pos] == '(':
                return GraphToken(GraphTokenType.OPENPAREN, \
                   self.graph_str[self.pos])
            elif self.graph_str[self.pos] == ')':
                return GraphToken(GraphTokenType.CLOSEPAREN, \
                   self.graph_str[self.pos])
            elif self.graph_str[self.pos] == ',':
                return GraphToken(GraphTokenType.COMMA, \
                   self.graph_str[self.pos])
            elif self.graph_str[self.pos] == '{':
                return GraphToken(GraphTokenType.OPENCURLY, \
                   self.graph_str[self.pos])
            elif self.graph_str[self.pos] == '}':
                return GraphToken(GraphTokenType.CLOSECURLY, \
                   self.graph_str[self.pos])
            #} can probably wrap this up into a dictionary.
        else:
            vertex = self.getVertex()
            if vertex != '':
                return GraphToken(GraphTokenType.VERTEX, \
                       vertex)
            else:
                raise ValueError("Invalid vertex label")
            
    def getNextToken(self):
        #possibly add a method which skips irrelevant whitespace and comments
        token = self.produceToken()
        if token.isVertex():
            self.pos += len(token.getValue())
        else:
            self.pos += 1
        return token
            
graph = GraphScanner(graph_data)

while True:
    token = graph.getNextToken()
    print(token)
    if token.isEOF():
        break

