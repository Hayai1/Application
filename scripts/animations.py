import pygame
class Animations:
    def __init__(self,rootAnimPath):
        self.rootAnimPath = rootAnimPath
        self.animationFrames = {}
        self.animationDatabase = {}
        self.frame = 0
        self.state = 'idle'
    
        
    def getAnimation(self,animName,frameDurations):
        animationFrameData = []
        n = 0
        for frame in frameDurations:
            animationFrameId = animName + str(n)
            imgLoc = f"{self.rootAnimPath}/{animName}/{animationFrameId}.png"
            animationImage = pygame.image.load(imgLoc).convert()
            animationImage.set_colorkey((0,0,0))
            self.animationFrames[animationFrameId] = animationImage.copy()
            for i in range(frame):
                animationFrameData.append(animationFrameId)
            n += 1
        self.animationDatabase[animName] = animationFrameData

    def getImg(self):
        if len(self.animationDatabase[self.state])-1 == self.frame:
            self.frame = 0
        else:
            self.frame += 1
        img = self.animationFrames[self.animationDatabase[self.state][self.frame]]
        return img
    def getCurrentImg(self):
        return self.animationDatabase[self.state][self.frame]
    def changeState(self,newState):
        if self.state != newState:
            self.state = newState
            self.frame = 0
        return self.state,self.frame
