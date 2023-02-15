class class1():
    def __init__(self):
        self.var = 1
        self.objOfClass2 = class2(self.setVar)
    def setVar(self,value):
        self.var = value

class class2:
    def __init__(self,setVarFunc):
        self.setVarFunc = setVarFunc
    def callSetVarFunc(self,value):
        self.setVarFunc(value)
    

objOfClass1 = class1()
print(objOfClass1.var)
objOfClass1.objOfClass2.callSetVarFunc(2)
print(objOfClass1.var)