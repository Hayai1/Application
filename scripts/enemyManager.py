from scripts.enemy import Enemy
from random import randint

class EnemyManager():
    def __init__(self,enemyAmount,target,worldid, dbhandler,roomData,rectsToCollideWith,graph):#create the enemyManager
        self.enemies= []#the list of enemies
        self.enemyAmount = enemyAmount#the amount of enemies
        self.graph = graph#the graph
        self.target = target#the target to focus on
        self.damageMult, self.hpMult = dbhandler.getEnemyData(worldid)#get the damage and hp multiplier from the database
        self.collisionRects = rectsToCollideWith#the collision rects
        self.createEnemies(roomData)#create the enemies
    def randomPos(self,roomData):#get a random position within one a random room
        rndRoom = roomData[randint(0,len(roomData)-1)]#get a random room
        rndPos = rndRoom.graphRects[0]#get a random position in the room
        return rndPos.x+8*16,rndPos.y+16#return the position
        
    def createEnemies(self,roomData):#create the enemies
        for enemy in range(0,self.enemyAmount):#loop through the amount of enemies
            x,y = self.randomPos(roomData)#get a random position
            self.enemies.append(Enemy(x,y,16, 16,self.graph,'assets/hpBar/enemy/enemyHpBar.png',target=self.target,collisionRects=self.collisionRects,damageMult=self.damageMult, hpMult=self.hpMult))#create a new enemy
        
    def update(self, gameSurface, scroll):
        deadEnemies = []#the list of dead enemies
        for enemy in self.enemies:#loop through the enemies
            enemy.update(gameSurface, scroll)#update the enemy
            if enemy.dead:#if the enemy is dead
                deadEnemies.append(enemy)#add the enemy to the list of dead enemies
        '''
        removing during iteration would not work so:
        '''
        for enemy in deadEnemies:#loop through the dead enemies
            self.enemies.remove(enemy)#remove the enemy from the list of enemies
        