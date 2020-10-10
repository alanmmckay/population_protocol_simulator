from sys import argv, path
import os
path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + 
'/../'))
path.insert(0, os.getcwd())

from transition_scanner import TransitionScanner
from transition_parser import TransitionParser
from helper_functions import file_input

transition_data = file_input('transition')
print("Looking at transition set: " + str(transition_data))
scanner = TransitionScanner(transition_data)
parser = TransitionParser(scanner)
print(parser.parse())
