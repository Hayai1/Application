from scripts.enemy import Enemy
from random import randint
import pygame
class EnemyManager():
    def __init__(self,enemyAmount,target,worldid, dbhandler,roomData,rectsToCollideWith,graph):
        self.enemies= []
        self.enemyAmount = enemyAmount
        self.graph = graph
        self.target = target
        self.damageMult, self.hpMult = dbhandler.getEnemyData(worldid)
        self.collisionRects = rectsToCollideWith
        self.createEnemies(roomData)
    def randomPos(self,roomData):
        rndRoom = roomData[randint(0,len(roomData)-1)]
        rndPos = rndRoom.graphRects[0]
        return rndPos.x+8*16,rndPos.y+16
        
    def createEnemies(self,roomData):
        for enemy in range(0,self.enemyAmount):
            x,y = self.randomPos(roomData)
            self.enemies.append(Enemy(x,y,16, 16,self.graph,'assets/hpBar/enemy/enemyHpBar.png',target=self.target,collisionRects=self.collisionRects,damageMult=self.damageMult, hpMult=self.hpMult))
        
    def update(self, gameSurface, scroll):
        deadEnemies = []
        for enemy in self.enemies:
            enemy.update(gameSurface, scroll)
            if enemy.dead:
                deadEnemies.append(enemy)
        for enemy in deadEnemies:
            self.enemies.remove(enemy)
