from general_token import GeneralToken, GeneralTokenType

#--- --- ---#
#A scanner super class that simply iterates through an
#input string and assumes each character is an individual
#token.
#--- --- ---#

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
        
    def getInputString(self):
        return self.input_str
        
    if __name__ == "__main__":
        def getNextToken(self):
            # --- getNextToken invokes produceToken() while
                #keeping handling the character position of
                #the input string
            token = self.produceToken()
            if token.isChar():
                self.pos += 1
            return token
        
        def produceToken(self):
            # --- produceToken is used to create tokenType
                #objects based on the input string.
            if self.pos >= self.maxPos:
                return GeneralToken(GeneralTokenType.EOF)
            else:
                return GeneralToken(GeneralTokenType.CHAR, \
                    self.input_str[self.pos])
            
            
if __name__ == "__main__":
    from helper_functions import file_input
    input_data = file_input("input: ")
    scanner = Scanner(input_data)

    while True:
        token = scanner.getNextToken()
        print(token)
        if token.isEOF():
            break



