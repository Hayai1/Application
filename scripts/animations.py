import pygame
class Animations:
    def __init__(self,rootAnimPath):
        self.rootAnimPath = rootAnimPath#the root animation path e.g. 'assets/animations' in the directory there are folders which contain the animations in images
        self.animationFrames = {}#the animation frames
        self.animationDatabase = {}#the animation database
        self.frame = 0#the current frame
        self.state = 'idle'#the current state
    
        
    def getAnimation(self,animName,frameDurations):#get the animation
        animationFrameData = []#the animation frame data
        n = 0#the frame number
        for frame in frameDurations:#for each frame in the frame durations
            animationFrameId = animName + str(n)#the animation frame id
            imgLoc = f"{self.rootAnimPath}/{animName}/{animationFrameId}.png"#the image location
            animationImage = pygame.image.load(imgLoc).convert()#load the image
            animationImage.set_colorkey((0,0,0))#set the color key
            self.animationFrames[animationFrameId] = animationImage.copy()#add the animation frame to the animation frames
            for i in range(frame):#for each frame in the frame duration
                animationFrameData.append(animationFrameId)#add the animation frame id to the animation frame data
            n += 1#increment the frame number
        self.animationDatabase[animName] = animationFrameData#add the animation frame data to the animation database

    def getImg(self):#get the image to draw
        if len(self.animationDatabase[self.state])-1 == self.frame:#if the current frame is the last frame
            self.frame = 0#reset frame
        else:
            self.frame += 1#increment the frame
        img = self.animationFrames[self.animationDatabase[self.state][self.frame]]#get the image
        return img#return the image
    @property
    def getCurrentImg(self):
        return self.animationDatabase[self.state][self.frame]#return the current image
    def changeState(self,newState):#change the state
        if self.state != newState:#if the state is not the same as the new state
            self.state = newState#set the state to the new state
            self.frame = 0#reset the frame
        return self.state,self.frame#return the state and frame
