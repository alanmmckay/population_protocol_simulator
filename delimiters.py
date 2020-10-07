class Delimiters:
    def __init__(self):
        self.contextless = list()
        self.encapsulators = list()
        self.openers = list()
        self.closers = list()
        self.encapsulators.append(self.openers)
        self.encapsulators.append(self.closers)
        
    def __iter__(self):
        for d in self.contextless:
            yield d
        for l in self.encapsulators:
            for d in l:
                yield d
            
    def __contains__(self, item):
        for d in self:
            if item == d:
                return True
        return False
    
    def assign(self,item):
        #perhaps add logic to ensure every opener has an equivelent closer
        if item in ['<','{','[','(']:
            self.openers.append(item)
        elif item in ['>','}',']',')']:
            self.closers.append(item)
        else:
            self.contextless.append(item)
        return True

    def append(self,item):
        if type(item) == list:
            for d in item:
                self.assign(str(d))
        else:
            self.assign(str(item))
        return True

    def getEncapsulators(self):
        return self.encapsulators
    
    def getOpeners(self):
        return self.encapsulators[0]
    
    def getClosers(self):
        return self.encapsulators[1]
    
if __name__ == "__main__":
    delimiters = Delimiters()
    delimiters.append(['1','2','3','4','}','('])
    
