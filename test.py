class class1:
    def __init__(self,x):
        self.x = x

class class2(class1):
    def __init__(self):
        self.y = 20
        super().__init__(self.y+10)

c2 = class2()

print(c2.x, c2.y)