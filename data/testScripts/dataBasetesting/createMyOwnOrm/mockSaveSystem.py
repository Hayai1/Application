import os,random

from myOrm import Database, Column, Table, PrimaryKey

DB_PATH = 'data/testScripts/dataBasetesting/createMyOwnOrm/dataBase.db'

if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

db = Database(DB_PATH)

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
    seed = Column(int)
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

db.create(CHARACTER)
db.create(CHARACTERPOSITIONS)
db.create(WORLD)
db.create(DIFFICULTY)
db.create(APPLICATIONSETTINGS)

player1 = CHARACTER(name = "kenshi", HP = 100)
player2 = CHARACTER(name = "zeldora", HP = 100)
player3 = CHARACTER(name = "strings", HP = 100)

world1 = WORLD(worldName="world1", seed = 38529523087, difficultyLevel = 1)
world2 = WORLD(worldName="world2", seed = 38529523087, difficultyLevel = 2)
world3 = WORLD(worldName="world3", seed = 38529523087, difficultyLevel = 3)

characterSaveData1 = CHARACTERPOSITIONS(characterid = 1,
                                        worldid = 1,
                                        xPos = 45.5,
                                        yPos=32.1)
characterSaveData2 = CHARACTERPOSITIONS(characterid = 2,
                                        worldid = 2,
                                        xPos = 45.5,
                                        yPos=32.1)
characterSaveData3 = CHARACTERPOSITIONS(characterid = 3,
                                        worldid = 3,
                                        xPos = 45.5,
                                        yPos=32.1)
characterSaveData4 = CHARACTERPOSITIONS(characterid = 1,
                                        worldid = 3,
                                        xPos = 45.5,
                                        yPos=32.1)




db.saveRecord(player1)
db.saveRecord(player2)
db.saveRecord(player3)
db.saveRecord(world1)
db.saveRecord(world2)
db.saveRecord(world3)
db.saveRecord(characterSaveData1)
db.saveRecord(characterSaveData2)
db.saveRecord(characterSaveData3)
db.saveRecord(characterSaveData4)



print("Characters to choose from: ")
print(db.manualSQLCommand('SELECT characterid, name FROM CHARACTER'))#get all the characters to choose from
getCharcter = input('select a character or type "new" to create a new character: ')
if getCharcter == 'new':
    newCharacterName = input('enter a name for the new character: ')
    newCharacterHP = 100
    newCharacter = CHARACTER(name = newCharacterName,HP = newCharacterHP)
    db.saveRecord(newCharacter)
    getCharcter = str(db.manualSQLCommand('SELECT MAX(characterid) FROM CHARACTER')[0][0])

    
print(db.manualSQLCommand('SELECT * FROM WORLD'))#get all the worlds
getWorld = input('select a world or type new to create one: ')
if getWorld == 'new':
    name = input('enter a name for the new world: ')
    difficulty = input('enter a difficulty for the world: ')
    seed = random.randint(1000000,9999999)
    newWorld = WORLD(worldName=name, seed = seed, difficultyLevel = difficulty)
    db.saveRecord(newWorld)
    getWorld = str(db.manualSQLCommand('SELECT MAX(worldid) FROM WORLD')[0][0])

print(db.manualSQLCommand(f'SELECT * FROM CHARACTER WHERE characterid = {getCharcter}'))#get all the data for the character
print(db.manualSQLCommand(f'SELECT * FROM WORLD WHERE worldid = {getWorld}'))#get all the data for the character in the world
print(db.manualSQLCommand(f'SELECT * FROM CHARACTERPOSITIONS WHERE characterid = {getCharcter} AND worldid = {getWorld}'))    



