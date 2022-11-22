import pygame
class Animations:
    def __init__(self,rootAnimPath):
        self.rootAnimPath = rootAnimPath
        self.animationFrames = {}
        self.animationDatabase = {}
        
    def getAnimation(self,animName,frameDurations):
        animationFrameData = []
        n = 0
        for frame in frameDurations:
            animationFrameId = animName + '_' + str(n)
            img_loc = self.rootAnimPath + '/' + animationFrameId + '.png'
            # player_animations/idle/idle_0.png
            animation_image = pygame.image.load(img_loc).convert()
            animation_image.set_colorkey((255,255,255))
            self.animationFrames[animationFrameId] = animation_image.copy()
            for i in range(frame):
                animationFrameData.append(animationFrameId)
            n += 1
        return animationFrameData

    def change_action(action_var,frame,new_value):
        if action_var != new_value:
            action_var = new_value
            frame = 0
        return action_var,frame

Animations()