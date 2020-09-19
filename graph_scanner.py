from graph_token import GraphToken, GraphTokenType
from helper_functions import file_input

graph_data = file_input('graph')

print(graph_data)

#case scheme:
#-objects which can be referenced externally use camel case
#-objects which are referenced internally use underscores

delimiters = ["{","}","(",")",","]

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
            self.lookahead = self.getNextToken()
        return self.look_ahead
    
   def nextToken(self):
       if self.look_ahead:
           next_token = self.look_ahead
           self.look_ahead = None
           return next_token
       else:
           return self.getNextToken()
       
    def getNextToken(self):
        #possibly add a method which skips irrelevant whitespace and comments
        if self.pos >= maxPos:
            return GraphToken(GraphTokenType.EOF)
        
        elif self.graph_str[self.pos] in delimiters:
            return GraphToken(GraphTokenType.DELIMITER,self.graph_str[self.pos])
        
        elif 
        #check to see valid vertex label.
        #check to see if it is a duplicate.
        
        else:
            #throw an error
    
