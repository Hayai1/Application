#10x10
'''
01000100
00100000
00010000
00001000
00000100
00000010
00000100
00001000
00010000
00100000
'''
rects = [[1,0],[3,2],[3,8],[5,0],[2,1],[4,3],[6,5],[5,4],[5,6],[4,7],[2,9]]

x = [i[0] for i in rects]
y = [i[1] for i in rects]

world = [[0 for i in range(max(x)+1)] for j in range(max(y)+1)]


for rect in rects:
    world[rect[1]][rect[0]] = 1

for i in world:
    print(i)