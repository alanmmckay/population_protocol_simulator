
def file_input(input_type):
    print("--- Input q to exit ---")
    input_string = 'Input file name of '+str(input_type)+': '
    while True:
        file_name = input(input_string)
        try:
            f = open(file_name, 'r')
            data = f.read()
            f.close()
            data = data.replace(' ','').replace('\n','')
            return data
        except:
            if file_name == 'q':
                return None
            else:
                input_string = 'File does not exist. Please input file name of '+str(input_type)+': '
                continue
 
