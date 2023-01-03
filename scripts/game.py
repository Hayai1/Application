
import pygame
import time

from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((700,500),"Nea Project",60)
        self.camera = Camera()
        self.world = World(self.window.surface,self.camera,8)
        self.player = Player(self.world.graphRects[0].x+8*16,self.world.graphRects[0].y+16, 16, 16,self.window.surface,self.camera,[0,0])

        enemyX = self.world.graphRects[0].x+8*16
        enemyY = self.world.graphRects[0].y+16
        self.enemy1 = Enemy(enemyX,enemyY, 16, 16,self.world.graph,'assets/playerAnimations/idle/idle0.png',[0,0])
        self.enemy2 = Enemy(enemyX-32,enemyY, 16, 16,self.world.graph,'assets/playerAnimations/idle/idle0.png',[0,0])
        self.player.setRectsToCollideWith(self.world.collisionRects)
        self.camera.set_target(self.player)
        self.player.input.enemy = self.enemy1
    def update(self):
        self.camera.update()
        self.world.update()
        self.enemy1.update(self.player,self.window.surface,self.camera.scroll,self.world.collisionRects)
        #self.enemy2.update(self.player,self.window.surface,self.camera.scroll,self.world.collisionRects)
        self.player.update()
        pygame.draw.rect(self.window.surface,(255,255,255),((self.enemy1.x + self.enemy1.width/2)-self.camera.scroll[0],(self.enemy1.y + self.enemy1.height)-self.camera.scroll[1],1,1))
        self.window.update()
        
    def runGame(self):
        while True:
            self.update()
    

