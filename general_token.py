from enum import Enum

class GeneralTokenType(Enum):
    CHAR =  1;
    STRING = 2;
    DELIMITER = 3;
    EOF = 4;

class GeneralToken:
    def __init__(self, token_type, token_value = None):
        self.token_type = token_type
        self.token_value = token_value
        
    def getValue(self):
        return self.token_value
    
    def getType(self):
        return self.token_type
        
    def isChar(self):
        return self.token_type == GeneralTokenType.CHAR
        
    def isString(self):
        return self.token_type == GeneralTokenType.STRING
    
    def isDelimiter(self):
        return self.token_type == GeneralTokenType.DELIMITER
    
    def isEOF(self):
        return self.token_type == GeneralTokenType.EOF
    
    def __repr__(self):
        if self.isChar():
            return 'Char ' + str(self.token_value)
        elif self.isString():
            return 'String ' + str(self.token_value)
        elif self.isDelimiter():
            return 'Delimiter ' + str(self.token_value)
        elif self.isEOF():
            return 'end_of_stream'
        #else error
