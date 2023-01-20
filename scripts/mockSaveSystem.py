import os,random

from orm import Database, Column, Table, PrimaryKey

DB_PATH = 'data/testScripts/dataBasetesting/createMyOwnOrm/dataBase.db'
def createTables(db, table):
    db.create(table)
createTheTables = False
if not os.path.exists(DB_PATH):
    createTheTables = True

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

if createTheTables:
    for i in [CHARACTER,CHARACTERPOSITIONS,WORLD,DIFFICULTY,APPLICATIONSETTINGS]:
        createTables(db, i)




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



