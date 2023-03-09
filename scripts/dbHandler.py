import os#this is for checking if the database hasnt existed yet and tables need to be created
from scripts.orm import Database,Table, Column, PrimaryKey#this is for the database
DB_PATH = 'data/database/dataBase.db'#this is the path to the database
class DBHandler:#Database handler class
    def __init__(self):#constructor function for the database handler class takes no arguments
        #check if the database hasnt existed yet and tables need to be created

        createTables = False#this is for checking if the database hasnt existed yet and tables need to be created
        if not os.path.exists(DB_PATH):#if the database doesnt exist
            createTables = True#set createTables to true
        self.db = Database(DB_PATH)#create a new database object
        if createTables:#if the database hasnt existed yet and tables need to be created
            for i in [self.CHARACTER,self.CHARACTERPOSITIONS,self.WORLD,self.DIFFICULTY]:self.db.create(i)
        #create records
        if self.db.manualSQLCommand('SELECT * FROM DIFFICULTY') == []:#if the difficulty table is empty
            easy = self.DIFFICULTY(difficultyLevel = 1, name = 'Easy',enemyHPMultiplier=0.5, enemyAttackMultiplier=0.5)#create a new easy difficulty record
            self.db.saveRecord(easy)#save the record
            mid = self.DIFFICULTY(difficultyLevel = 2, name = 'Medium',enemyHPMultiplier=1, enemyAttackMultiplier=1)#create a new medium difficulty record
            self.db.saveRecord(mid)#save the record
            hard = self.DIFFICULTY(difficultyLevel = 3, name = 'Hard',enemyHPMultiplier=2, enemyAttackMultiplier=2)#create a new hard difficulty record
            self.db.saveRecord(hard)#save the record
        
    def getAllWorldData(self):#this function gets all the world data from the database in the WORLD table
        data=self.db.manualSQLCommand('SELECT worldid,worldName,seed FROM WORLD')#get all the world data from the database in the WORLD table
        return data#return the data
    def getAllCharacterData(self):#this function gets all the character data from the database in the CHARACTER table
        data=self.db.manualSQLCommand('SELECT characterid,name FROM CHARACTER')#get all the character data from the database in the CHARACTER table
        return data#return the data
    def createCharacterRecord(self, name):#this function creates a new character record in the database takes 1 argument: name which is a string of the characters name
        newCharacter = self.CHARACTER(name = name,HP = 100)#create a new character record
        self.db.saveRecord(newCharacter)#save the record
        return str(self.db.manualSQLCommand('SELECT MAX(characterid) FROM CHARACTER')[0][0])#return the characterid of the new character record
    def createWorldRecord(self, worldName, difficultyLevel, seed):#this function creates a new WORLD record in the database takes 3 arguments: worldName which is a string of the worlds name, difficultyLevel which is an int of the difficulty level and seed which is a string of the seed
        newWorld = self.WORLD(worldName = worldName,seed = seed,difficultyLevel = difficultyLevel)#create a new world record
        self.db.saveRecord(newWorld)#save the record
        return str(self.db.manualSQLCommand('SELECT MAX(worldid) FROM WORLD')[0][0])#return the worldid of the new world record
    def createCharacterPositionsRecord(self, playerId, worldId, playerPosition):#this function creates a new character positions record takes 3 arguments: playerId which is an int of the players characterid, worldId which is an int of the worldid and playerPosition which is a tuple of the players current position
        newCharacterPosition = self.CHARACTERPOSITIONS(characterid = playerId, worldid = worldId, xPos = playerPosition[0], yPos = playerPosition[1])#create a new character position record
        self.db.saveRecord(newCharacterPosition)#save the record
    def getPlayerPositionData(self,playerID, worldID,defaultPos):
        playerPositionData = self.db.manualSQLCommand(f'SELECT xPos,yPos FROM CHARACTERPOSITIONS WHERE characterid = {playerID} and worldid = {worldID}')#get the players position from the database
        if playerPositionData == []:
            self.createCharacterPositionsRecord(playerID, worldID, defaultPos[0],defaultPos[1])
            return defaultPos[0],defaultPos[1]
        return playerPositionData[0][0],playerPositionData[0][1]
    def getPlayerData(self, playerID):#this function gets the player data from the database takes 3 arguments: playerID which is an int of the players characterid, worldID which is an int of the worldid and defaultPos which is a tuple of the default position of the player
        playerName,hp = self.db.manualSQLCommand(f'SELECT name,HP FROM CHARACTER WHERE characterid = {playerID}')[0]#get the player name and hp from the database
        return playerName, hp
    def getWorldData(self, worldID):#this function gets the world data from the database takes 1 argument: worldID which is an int for an id of a world in WORLD
        worldName = str(self.db.manualSQLCommand(f'SELECT worldName FROM WORLD WHERE worldid = {worldID}')[0][0])#get the world name from the database
        seed = self.db.manualSQLCommand(f'SELECT seed FROM WORLD WHERE worldid = {worldID}')#get the seed from the database
        return worldName, seed[0][0]#return the world name and the seed
    def updatePlayerPosInSpecificWorld(self, playerId, worldId, playerPosition):#this function updates the players position in a specific world takes 3 arguments: playerId which is an int of the players characterid, worldId which is an int of the worldid and playerPosition which is a tuple of the players current position 
        self.db.manualSQLCommand(f"UPDATE CHARACTERPOSITIONS SET xPos ={playerPosition[0]}, yPos = {playerPosition[1]} WHERE characterid = {playerId} and worldid = {worldId}")#update the players position in the database
    def updatePlayerHp(self, playerId, hp):#this function updates the players hp takes 2 arguments: playerId which is an int of the players characterid and hp which is an int of the players hp
        self.db.manualSQLCommand(f"UPDATE CHARACTER SET HP = {hp} WHERE characterid = {playerId}")#update the players hp in the database
    def getEnemyData(self, worldID):#this function returns the enemy attack multiplier and hp multiplier depending on the worlds difficulty takes 1 argument: worldID which is an int for an id of a world in WORLD
        difficultyLevel = self.db.manualSQLCommand(f'SELECT difficultyLevel FROM WORLD WHERE worldid = {worldID}')[0][0]#get the difficulty level from the database
        damageMult,hpMult = self.db.manualSQLCommand(f'SELECT enemyAttackMultiplier,enemyHPMultiplier FROM DIFFICULTY WHERE difficultyLevel = {difficultyLevel}')[0]#get the enemy attack multiplier and hp multiplier from the database   
        return damageMult, hpMult#return the enemy attack multiplier and hp multiplier
        
    #----------------------------------------------Tables-------------------------------------------------------------->
    class CHARACTER(Table):#create the CHARACTER table and inherit from Table class
        characterid = PrimaryKey(True)#create the characterid column
        name = Column(str)#create the name column
        HP = Column(int)#create the HP column

    class CHARACTERPOSITIONS(Table):#create the CHARACTERPOSITIONS and inherit from Table class
        characterid = Column(int)# create the characterid column
        worldid = Column(int)#create the worldid column
        xPos = Column(float)#create the xPos column
        yPos = Column(float)#create the yPos column

    class WORLD(Table):#create the WORLD table and inherit from Table class
        worldid = PrimaryKey(int)#create the worldid column
        worldName = Column(str)#create the worldName column
        seed = Column(str)#create the seed column
        difficultyLevel = Column(int)#create the difficultyLevel column
        
    class DIFFICULTY(Table):#create the DIFFICULTY table and inherit from Table class
        difficultyLevel = Column(int)#create the difficultyLevel column
        enemyHPMultiplier = Column(float)#create the enemyHPMultiplier column
        enemyAttackMultiplier = Column(float)#create the enemyAttackMultiplier column
        name = Column(str)#create the name column
    #------------------------------------------------------------------------------------------------------------------>        
    
