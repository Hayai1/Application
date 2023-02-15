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
        #create the database
        
        #create the tables
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

    def getPlayerData(self, playerID, worldID):
        playerName = str(self.db.manualSQLCommand(f'SELECT name FROM CHARACTER WHERE characterid = {playerID}')[0][0])
        playerPositionData = self.db.manualSQLCommand(f'SELECT xPos,yPos FROM CHARACTERPOSITIONS WHERE characterid = {playerID} and worldid = {worldID}')
        return playerName, playerPositionData
    def getWorldData(self, worldID):
        worldName = str(self.db.manualSQLCommand(f'SELECT worldName FROM WORLD WHERE worldid = {worldID}')[0][0])
        seed = self.db.manualSQLCommand(f'SELECT seed FROM WORLD WHERE worldid = {worldID}')
        return worldName, seed[0][0]
    
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
            
    
