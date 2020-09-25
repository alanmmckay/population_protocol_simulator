import sys
#sys.tracebacklimit=0

class Error():
    def __init__(self, input_string):
        self.input_string = input_string
        self.error_message = "\n--\n"
        self.error_type = str()
        self.file_name = "error.txt"
        self.error_string = str()
        self.output_string = str()
        self.output = str()
        
    def open_file(self):
        self.output = open(self.file_name, 'w')
        
    def write_file(self, error):
        self.output_string = "!--- "+self.error_type+" ERROR! ---!\n\n\n"
        self.output_string += "---> Input String: \n"
        self.output_string += self.input_string
        self.output_string += "\n\n\n---> Error Information: \n"
        self.output_string += error
        self.output.write(self.output_string)
        
    def close_file(self):
        self.output.close()
        
    def throw_error(self):
        self.error_message += "\n--\nError log written to "+self.file_name
        raise RuntimeError(self.error_message)
    
    def output_error(self):
        #self.open_file()
        #self.write_file(self.error_string)
        #self.close_file()
        self.throw_error()
        pass
#end class Error


class GeneralError(Error):
    def __init__(self, msg, input_str):
        Error.__init__(self, input_str)
        self.error_message += msg
        self.error_string = msg
        self.output_error()
#end class GeneralError

class ParseError(GeneralError):
    def __init(self, msg, input_str):
        GeneralError.__init__(msg, input_str)
