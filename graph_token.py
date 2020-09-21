from enum import Enum

class GraphTokenType(Enum):
    VERTEX = 1;
    OPENPAREN = 2;
    CLOSEPAREN = 3;
    OPENCURLY = 4;
    CLOSECURLY = 5;
    COMMA = 6;
    EOF = 7;
    
class GraphToken:
    def __init__(self, token_type, token_value = None):
        self.token_type = token_type
        self.token_value = token_value
        
    def isVertex(self):
        return self.token_type == GraphTokenType.VERTEX
    
    def isDelimiter(self):
        return self.token_type == GraphTokenType.DELIMITER
    
    def isOpenParen(self):
        return self.token_type == GraphTokenType.OPENPAREN
    
    def isCloseParen(self):
        return self.token_type == GraphTokenType.CLOSEPAREN
    
    def isOpenCurly(self):
        return self.token_type == GraphTokenType.OPENCURLY
    
    def isCloseCurly(self):
        return self.token_type == GraphTokenType.CLOSECURLY
    
    def isComma(self):
        return self.token_type == GraphTokenType.COMMA
    
    def isEOF(self):
        return self.token_type == GraphTokenType.EOF
    
    def getValue(self):
        return self.token_value
    
    def getType(self):
        return self.token_type
    
    def __repr__(self):
        if self.isVertex():
            return 'Vertex ' + str(self.token_value)
        
        elif self.isEOF():
            return 'end_of_stream'

        else:
            return 'Delimiter ' + str(self.token_value)
