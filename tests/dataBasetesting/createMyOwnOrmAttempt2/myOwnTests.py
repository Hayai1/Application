

from orm import Database, Column, Table, ForeignKey, PrimaryKey
import os
DB_PATH = 'NeaProject/tests/dataBasetesting/createMyOwnOrmAttempt2/dataBaseConn/dataBase.db'
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
        Name = Column(str)
        HP = Column(int)
        

class WORLD(Table):
        worldid = PrimaryKey()
        seed = Column(int)
        
class CHARACTERPOSITION(Table):
        xPos = Column(float)
        Ypos = Column(float)
        characterid = ForeignKey(CHARACTER)
        worldid = ForeignKey(WORLD)


db.create(CHARACTER)
db.create(WORLD)
db.create(CHARACTERPOSITION)