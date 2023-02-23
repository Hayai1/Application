import os
from scripts.orm import Database,Table, Column, PrimaryKey
DB_PATH = 'data/database/dataBase.db'
class DBHandler:
    def __init__(self):
        #check if the database hasnt existed yet and tables need to be created
        #if os.path.exists(DB_PATH):
        #    os.remove(DB_PATH)

        createTables = False
        if not os.path.exists(DB_PATH):
            createTables = True
        self.db = Database(DB_PATH)
        if createTables:
            for i in [self.CHARACTER,self.CHARACTERPOSITIONS,self.WORLD,self.DIFFICULTY,self.APPLICATIONSETTINGS]:
                self.db.create(i)
        #create records
        if self.db.manualSQLCommand('SELECT * FROM DIFFICULTY') == []:
            easy = self.DIFFICULTY(difficultyLevel = 1, name = 'Easy',enemyHPMultiplier=0.5, enemyAttackMultiplier=0.5)
            self.db.saveRecord(easy)
            mid = self.DIFFICULTY(difficultyLevel = 2, name = 'Medium',enemyHPMultiplier=1, enemyAttackMultiplier=1)
            self.db.saveRecord(mid)
            hard = self.DIFFICULTY(difficultyLevel = 3, name = 'Hard',enemyHPMultiplier=2, enemyAttackMultiplier=2)
            self.db.saveRecord(hard)
        
    def getAllWorldData(self):
        data=self.db.manualSQLCommand('SELECT worldid,worldName,seed FROM WORLD')
        return data
    def getAllCharacterData(self):
        data=self.db.manualSQLCommand('SELECT characterid,name FROM CHARACTER')
        return data
    def createCharacterRecord(self, name):
        newCharacter = self.CHARACTER(name = name,HP = 100)
        self.db.saveRecord(newCharacter)
        return str(self.db.manualSQLCommand('SELECT MAX(characterid) FROM CHARACTER')[0][0])

    def createWorldRecord(self, worldName, difficultyLevel, seed):
        newWorld = self.WORLD(worldName = worldName,seed = seed,difficultyLevel = difficultyLevel)
        self.db.saveRecord(newWorld)
        return str(self.db.manualSQLCommand('SELECT MAX(worldid) FROM WORLD')[0][0])

    def getPlayerData(self, playerID, worldID,defaultPos):
        playerName,hp = self.db.manualSQLCommand(f'SELECT name,HP FROM CHARACTER WHERE characterid = {playerID}')[0]
        playerPositionData = self.db.manualSQLCommand(f'SELECT xPos,yPos FROM CHARACTERPOSITIONS WHERE characterid = {playerID} and worldid = {worldID}')
        if playerPositionData == []:
            newCharacterPosition = self.CHARACTERPOSITIONS(characterid = playerID, worldid = worldID, xPos = defaultPos[0], yPos = defaultPos[1])
            self.db.saveRecord(newCharacterPosition)
            return playerName, hp,defaultPos[0],defaultPos[1]
        return playerName, hp,playerPositionData[0][0],playerPositionData[0][1]
    def getWorldData(self, worldID):
        worldName = str(self.db.manualSQLCommand(f'SELECT worldName FROM WORLD WHERE worldid = {worldID}')[0][0])
        seed = self.db.manualSQLCommand(f'SELECT seed FROM WORLD WHERE worldid = {worldID}')
        return worldName, seed[0][0]
    def updatePlayerPosInSpecificWorld(self, playerId, worldId, playerPosition):
        self.db.manualSQLCommand(f"UPDATE CHARACTERPOSITIONS SET xPos ={playerPosition[0]}, yPos = {playerPosition[1]} WHERE characterid = {playerId} and worldid = {worldId}")
        
    def updatePlayerHp(self, playerId, hp):
        self.db.manualSQLCommand(f"UPDATE CHARACTER SET HP = {hp} WHERE characterid = {playerId}")
    def newCharacterPositionsRecord(self, playerId, worldId, playerPosition):
        newCharacterPosition = self.CHARACTERPOSITIONS(characterid = playerId, worldid = worldId, xPos = playerPosition[0], yPos = playerPosition[1])
        self.db.saveRecord(newCharacterPosition)
    
    def getEnemyData(self, worldID):
        difficultyLevel = self.db.manualSQLCommand(f'SELECT difficultyLevel FROM WORLD WHERE worldid = {worldID}')[0][0]
        damageMult,hpMult = self.db.manualSQLCommand(f'SELECT enemyAttackMultiplier,enemyHPMultiplier FROM DIFFICULTY WHERE difficultyLevel = {difficultyLevel}')[0]        
        return damageMult, hpMult    
        
        
    class CHARACTER(Table):
        characterid = PrimaryKey(True)
        name = Column(str)
        HP = Column(int)

    class CHARACTERPOSITIONS(Table):
        characterid = Column(int)
        worldid = Column(int)
        xPos = Column(float)
        yPos = Column(float)

    class WORLD(Table):
        worldid = PrimaryKey(int)
        worldName = Column(str)
        seed = Column(str)
        difficultyLevel = Column(int)
    class DIFFICULTY(Table):
        difficultyLevel = Column(int)
        enemyHPMultiplier = Column(float)
        enemyAttackMultiplier = Column(float)
        name = Column(str)
    class APPLICATIONSETTINGS(Table):
        fullscreen = Column(bool)
        resolution = Column(str)
        Volume = Column(float)
            
    
