from sys import argv, path
import os
path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + 
'/../'))
path.insert(0, os.getcwd())

from transition_scanner import TransitionScanner
from helper_functions import file_input

transition_data = file_input('transition')
print("Looking at transition set: " + str(transition_data))
transition = TransitionScanner(transition_data)

while True:
    token = transition.getNextToken()
    print(token)
    if token.isEOF():
        break
