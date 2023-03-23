
class Camera:
    def __init__(self,target):#target is the object to focus on
        self.true_scroll = [0,0]#the true scroll
        self.scroll = [0,0]#the scroll
        self.target = target#the target to focus on
    def update(self):#update the camera
        self.true_scroll[0] += (self.target.rect.x-self.true_scroll[0]-152)/20#set the true scroll to the target's x position - 152 (the center of the screen) divided by 20 (the speed of the camera so it's more smooth when following the player 
        self.true_scroll[1] += (self.target.rect.y-self.true_scroll[1]-106)/20#set the true scroll to the target's y position - 106 (the center of the screen) divided by 20 (the speed of the camera so it's more smooth when following the player
        self.scroll = self.true_scroll.copy()#set the scroll to the true scroll
        self.scroll[0] = int(self.scroll[0])#set the scroll's x position to an integer
        self.scroll[1] = int(self.scroll[1])#set the scroll's y position to an integer
