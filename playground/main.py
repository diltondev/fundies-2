class Thing:
    a: int
    b: int
    def __init__(self) -> None:
        pass
    
    def setA(self, a: int) -> None:
        self.a = a
        
    def setB(self, b: int) -> None:
        self.b = b
        
    def printa(self) -> None:
        print(self.a)
        
    def withA(self, a: int) -> Thing:
        self.setA(a)
        return self
    
    def withB(self, b: int) -> Thing:
        self.setB(b)
        return self
    

def funny(x: int) -> int:
    return x

my_thing = Thing().withA(3).withB(funny(4))
my_thing.printa()
print(my_thing.b)
