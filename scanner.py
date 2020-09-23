from enum import Enum

#--- --- ---#
#A scanner super class that simply iterates through an
#input string and assumes each character is an individual
#token.
#--- --- ---#

if __name__ == "__main__":
    class ScannerTokenType(Enum):
        CHAR = 1;
        EOF = 1;

    class ScannerToken:
        def __init__(self, token_type, token_value = None):
            self.token_type = token_type
            self.token_value = token_value
                
        def isChar(self):
            return self.token_type == ScannerTokenType.CHAR

        def isEOF(self):
            return self.token_type == ScannerTokenType.EOF

        def getValue(self):
            return self.token_value

        def getType(self):
            return self.token_type

        def __repr__(self):
            if self.isChar():
                return 'Char: ' + str(self.token_value)
            elif self.isEOF():
                return 'end_of_stream'
            

class Scanner:
    def __init__(self, input_str):
        self.input_str = input_str
        self.pos = 0
        self.maxPos = len(input_str)
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
        
    if __name__ == "__main__":
        def getNextToken(self):
            # --- getNextToken invokes produceToken() while
                #keeping handling the character position of
                #the input string
            token = self.produceToken()
            if len(token.getValue()) == 1:
                self.pos += 1
            return token
        
        def produceToken(self):
            # --- produceToken is used to create tokenType
                #objects based on the input string.
            if self.pos >= self.maxPos:
                return ScannerToken(ScannerTokenType.EOF)
            else:
                return ScannerToken(ScannerTokenType.CHAR, \
                    self.input_str[self.pos])


