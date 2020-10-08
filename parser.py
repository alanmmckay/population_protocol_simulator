from general_token import GeneralTokenType
from errors import GeneralError

class Parser:
    def __init__(self, scanner):
        #expects a scanner with the Delimiters object type
        self.scanner = scanner
        self.delimiter_set = scanner.getDelimiters()
        
    def parse(self):
        pass
        
    def match(self, expected_token_type, expected_token_value = None):
        next_token = self.scanner.nextToken()
        if next_token.getType() == expected_token_type:
            if expected_token_value:
                if next_token.getValue() == expected_token_value:
                    return next_token
                else:
                    error_msg = "Unexpected token: '"
                    error_msg += str(next_token)
                    error_msg +="' found."
                    GeneralError(error_msg, self.scanner.getInputString())
            else:
                return next_token
        else:
            error_msg = "Unexpected token type found in parser match"
            GeneralError(error_msg, self.scanner.getInputString())
            
    def match_encapsulator(self):
        next_token = self.scanner.nextToken()
        if next_token.getValue() in self.delimiter_set.getOpeners() or \
            next_token.getValue() in self.delimiter_set.getClosers():
                return next_token
        else:
            error_msg = "Error within edge set. Expecting an ecapsulating delimiter. "
            error_msg += "Received '"
            error_msg += next_token.getValue()
            error_msg += "' instead."
            GeneralError(error_msg, self.scanner.getInputString())
            
