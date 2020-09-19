from enum import Enum

class GraphTokenType(Enum):
    VERTEX = 1;
    DELIMITER = 2;
    EOF = 3;
    
class GraphToken:
    def __init__(self, token_type, token_value = None):
        self.token_type = token_type
        self.token_value = token_value
        
    def isVertex(self):
        return self.token_type == GraphTokenType.VERTEX
    
    def isDelimiter(self):
        return self.token_type == GraphTokenType.DELIMITER
    
    def isEOF(self):
        return self.token_type == GraphTokenType.EOF
    
    def __repr__(self):
        if self.isVertex():
            return 'Vertex ' + str(self.token_value)
        
        elif self.isDelimiter():
            return 'Delimiter ' + str(self.token_value)
        
        else:
            return 'end_of_stream'
