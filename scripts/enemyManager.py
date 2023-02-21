from scripts.enemy import Enemy
from random import randint
import pygame
class EnemyManager():
    def __init__(self,enemyAmount,roomData,player,surface,camera,rectsToCollideWith,graph):
        self.enemies= []
        self.enemyAmount = enemyAmount
        self.graph = graph
        self.player = player
        self.surface = surface
        self.camera = camera
        self.collisionRects = rectsToCollideWith
        self.createEnemies(roomData)
        
        
    def createEnemies(self,roomData):
        for i in range(0,self.enemyAmount):
            rndRoom = roomData[randint(0,len(roomData)-1)]
            rndPos = rndRoom.graphRects[0]
            self.enemies.append(Enemy(rndPos.x+8*16,rndPos.y+16,16, 16,self.graph,'assets/hpBar/enemy/enemyHpBar.png',[0,0],target=self.player,surf=self.surface,camera=self.camera,collisionRects=self.collisionRects))
        
    def update(self):
        deadEnemies = []
        for enemy in self.enemies:
            enemy.update()
            if enemy.dead:
                deadEnemies.append(enemy)
        for enemy in deadEnemies:
            self.enemies.remove(enemy)
