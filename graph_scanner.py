from scanner import Scanner
from graph_token import GraphToken, GraphTokenType

#case scheme:
#-objects which can be referenced externally use camel case
#-objects which are referenced internally use underscores
        
class GraphScanner(Scanner):
    def __init__(self, input_str):
        Scanner.__init__(self, input_str)
        #--- Generate Valid characters ---#
        self.delimiters = ["{","}","(",")",","]
        self.valid_string_chars = self.build_valid_char_list()
        #--- --- --- --- --- --- --- ---#
        
    def build_valid_char_list(self):
        valid_list = list()
        for i in range(65,91):
            valid_list.append(chr(i))
            valid_list.append(chr(i+32))
        for i in range(0,10):
            valid_list.append(chr(i))
        return valid_list
    
    def get_string(self):
        #while the next token is an alpha numeric character
        string = str()
        offset = self.pos
        while True:
            if self.input_str[offset] in self.valid_string_chars:
                string += self.input_str[offset]
                offset += 1
            else:
                return string
   
    def produceDelimiterToken(self):
        if self.input_str[self.pos] == '(':
            return GraphToken(GraphTokenType.OPENPAREN, \
                self.input_str[self.pos])
        elif self.input_str[self.pos] == ')':
            return GraphToken(GraphTokenType.CLOSEPAREN, \
                self.input_str[self.pos])
        elif self.input_str[self.pos] == ',':
            return GraphToken(GraphTokenType.COMMA, \
                self.input_str[self.pos])
        elif self.input_str[self.pos] == '{':
            return GraphToken(GraphTokenType.OPENCURLY, \
                self.input_str[self.pos])
        elif self.input_str[self.pos] == '}':
            return GraphToken(GraphTokenType.CLOSECURLY, \
                self.input_str[self.pos])
        #else:
            #error
   
    def produceToken(self):
        if self.pos >= self.maxPos:
            return GraphToken(GraphTokenType.EOF)
        elif self.input_str[self.pos] in self.delimiters:
            return self.produceDelimiterToken()
        else:
            vertex = self.get_string()
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
