from platform import release
import sqlite3
import os
from turtle import title
from peewee import SqliteDatabase, Model, TextField, DateField, IntegerField
#schema
db = SqliteDatabase("NeaProject/tests/dataBasetesting/ORMTesting/movies.db")

class BaseTable(Model):
    class Meta:
        database = db

class Movie(BaseTable):
    title = TextField(null=False, index=True)
    release_date = DateField(null=False, index = True)

# <--------------------create data----------------------------->
try:
    os.remove('movies.db')
except:
    pass

from datetime import date
db.connect()



#create the table
db.create_tables([Movie])
#add a record
blade_runner = Movie.create(title="Blade Runer", release_date=date(1982,6,25))
#blade runner is spelt wrong so we can edit it:
blade_runner.title = "Blade Runner"
blade_runner.save()# to save it to the database and not in the local copy of the database

