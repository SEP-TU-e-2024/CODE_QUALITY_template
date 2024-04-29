import kaas

t = kaas.Test()
print(t.getA())

class bruh():
    t = kaas.Test()
    
    def __init__(self):
        self.a = t.getA()
    
    def getT(self):
        return self.a
        
class Bozo():
    def __init__(self):
        self.b = bruh()
    
    def getB(self):
        return self.b

print("Hello World!")
print("Hello World!")
print("Hello World!")
