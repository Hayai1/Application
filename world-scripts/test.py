def recursion(ifNum,Checker,loc,coordinates):
    if ifNum == Checker:
        return print(f"{ifNum} == {Checker}, {loc}, {coordinates}")
    else:
        ifNum = int(ifNum) + 1
        if loc[0] == 64:
            loc[0] = 0
            loc[1] += 32
        else:
            loc[0] += 32
        return recursion(str(ifNum),Checker,loc,coordinates)





global data
data = "0000\n1111\n2222\n3333\n4444\n5555\n6666\n7777\n8888"
def getRoom():
        room = []
        xCounter = -1
        yCounter = 0
        surfaceX = 0
        for tile in data:
            xCounter += 1
            if tile == '\n':
                if surfaceX < xCounter:
                    surfaceX = xCounter
                yCounter +=1
                xCounter =-1
            else:
                recursion('0',tile,[0,0,16,16],(xCounter*16,yCounter*16))
                
            '''
            if tile == '0':
                print(room,(0,0,16,16),(xCounter*16,yCounter*16))
            elif tile == '1':
                print(room,(32,0,16,16),(xCounter*16,yCounter*16))
            elif tile == '2':
                print(room,(64,0,16,16),(xCounter*16,yCounter*16))
            elif tile == '3':
                print(room,(0,32,16,16),(xCounter*16,yCounter*16))
            elif tile == '4':
                print(room,(32,32,16,16),(xCounter*16,yCounter*16))
            elif tile == '5':
                print(room,(64,32,16,16),(xCounter*16,yCounter*16))
            elif tile == '6':
                print(room,(0,64,16,16),(xCounter*16,yCounter*16))
            elif tile == '7':
                print(room,(32,64,16,16),(xCounter*16,yCounter*16))
            elif tile == '8':
                print(room,(64,64,16,16),(xCounter*16,yCounter*16))
            elif tile == '\n':
                if surfaceX < xCounter:
                    surfaceX = xCounter
                    
                yCounter +=1
                xCounter =-1
        '''







getRoom()





def getRoom():
        room = []
        xCounter = -1
        yCounter = 0
        surfaceX = 0
        for tile in data:
            xCounter += 1
            if tile == '0':
                print(room,(0,0,16,16),(xCounter*16,yCounter*16))
            elif tile == '1':
                print(room,(32,0,16,16),(xCounter*16,yCounter*16))
            elif tile == '2':
                print(room,(64,0,16,16),(xCounter*16,yCounter*16))
            elif tile == '3':
                print(room,(32,0,16,16),(xCounter*16,yCounter*16))
            elif tile == '4':
                print(room,(32,0,16,16),(xCounter*16,yCounter*16))
            elif tile == '5':
                print(room,(64,32,16,16),(xCounter*16,yCounter*16))
            elif tile == '6':
                print(room,(0,64,16,16),(xCounter*16,yCounter*16))
            elif tile == '7':
                print(room,(32,64,16,16),(xCounter*16,yCounter*16))
            elif tile == '8':
                print(room,(64,64,16,16),(xCounter*16,yCounter*16))
            elif tile == '9':
                print(room,(128,32,16,16),(xCounter*16,yCounter*16))     
            elif tile == '\n':
                if surfaceX < xCounter:
                    surfaceX = xCounter
                yCounter +=1
                xCounter =-1

#getRoom()