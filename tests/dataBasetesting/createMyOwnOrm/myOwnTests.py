
from myOrm import Database, Column, Table, ForeignKey, PrimaryKey, QueryTools
import os
DB_PATH = 'tests/dataBasetesting/createMyOwnOrm/dataBaseConn/dataBase.db'

if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
db = Database(DB_PATH)

"""
class ClassName(Table):
        field1 = Column(type)
        field2 = Column(type)
        field3 = Column(type)
        field4 = ForeignKey(table)
        PrimaryKey(column)
"""

class CHARACTER(Table):
        characterid = PrimaryKey()
        name = Column(str)
        HP = Column(int)
        
class WORLD(Table):
        worldid = PrimaryKey()
        seed = Column(int)
        
class CHARACTERPOSITION(Table):
        xPos = Column(float)
        yPos = Column(float)
        characterid = ForeignKey(CHARACTER)
        worldid = ForeignKey(WORLD)

"""to create these tables and insert them into to the 
 Database simple you do db.create(table)"""
db.create(CHARACTER)
db.create(WORLD)
db.create(CHARACTERPOSITION)
"""
creating records will be done by creating an 
instance of said table you want to insert a record too
"""
player1 = CHARACTER(name = "kenshi", HP = 100)
player2 = CHARACTER(name = "zeldora", HP = 100)
player3 = CHARACTER(name = "strings", HP = 100)
player4 = CHARACTER(name = "lizzy", HP = 100)
player5 = CHARACTER(name = "eren", HP = 100)
world1  = WORLD(seed = 38529523087)
world2  = WORLD(seed = 38529523087)

characterSaveData1 = CHARACTERPOSITION(characterid = 1, 
                                       worldid = 1, 
                                       xPos = 45.5, 
                                       yPos=32.1)
characterSaveData2 = CHARACTERPOSITION(characterid = 4, 
                                       worldid = 2, 
                                       xPos = 45.5, 
                                       yPos=32.1)
characterSaveData2 = CHARACTERPOSITION(characterid = 1, 
                                       worldid = 3, 
                                       xPos = 45.5, 
                                       yPos=32.1)

db.saveRecord(player1)
db.saveRecord(player2)
db.saveRecord(player3)
db.saveRecord(player4)
db.saveRecord(player5)
db.saveRecord(world1)
db.saveRecord(world2)
db.saveRecord(characterSaveData1)
db.saveRecord(characterSaveData2)
db.saveRecord(characterSaveData2)

db.getAll(CHARACTER)
db.getAll(WORLD)
db.getAll(CHARACTERPOSITION)


print(db.getWhere({Table : CHARACTER, QueryTools.Where : 'name = kenshi and hp = 100'}))


#print(db.getWhere(table = CHARACTER, name = "kenshi", logicExpression = 'and', HP = 100))
#db.remove(table = CHARACTER, name = "kenshi", logicExpression = 'and', HP = 100)
#db.update(table = CHARACTER, setname='kenshiUpdated', logicalExpression = 'and', setHP = 50, name = "kenshi", logicalExpression = 'and', HP = 100)