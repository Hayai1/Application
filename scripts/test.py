class class1:
    def __init__(self,x) -> None:
        self.x = x
    def getX(self):
        return self.x


obj1 = class1(5)
while True:
    
    print(obj1.getX())