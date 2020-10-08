from sys import argv, path
import os
path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + 
'/../'))
path.insert(0, os.getcwd())

from init_scanner import InitScanner
from helper_functions import file_input

init_data = file_input('graph')
print("Looking at graph: " + str(init_data))
initial = InitScanner(init_data)

while True:
    token = initial.getNextToken()
    print(token)
    if token.isEOF():
        break
