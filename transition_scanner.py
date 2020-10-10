from graph_scanner import GraphScanner
from general_token import GeneralToken, GeneralTokenType
from errors import GeneralError
from delimiters import Delimiters

class TransitionScanner(GraphScanner):
    def __init__(self, input_str):
        GraphScanner.__init__(self, input_str)
        self.delimiters = Delimiters()
        self.delimiters.append(["{", "}", "(", ")", "[", "]", ",", "-",">"])
