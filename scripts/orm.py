
import sqlite3
import inspect
import sys

SELECTTABLES = "SELECT name FROM sqlite_master WHERE type = 'table';"
CREATETABLE = "CREATE TABLE {name} ({fields});"
INSERT = 'INSERT INTO {name} ({fields}) VALUES ({placeholders});'
SELECTALL = 'SELECT {fields} FROM {name};'

PYTHONTYPETOSQLITETYPE = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bytes: "BLOB",
    bool: "INTEGER",
}


class Database:
    def __init__(self, path):
        self.conn = sqlite3.Connection(path)
    """
    constructor to establish connection to a sqlite3 database
    """
    """
    returns tables in the database
    """
    def _execute(self,sql):
        return self.conn.execute(sql)
    """
    executes a sql command given as a param
    """
    def create(self, table):
        self._execute(table._get_create_sql())
    """
    creates a table using the class as a param
    """
    def saveRecord(self, table):
        self._execute(table._get_insert_sql())
        self.conn.commit()
    
    def manualSQLCommand(self,sql):
        data = self._execute(sql).fetchall()
        self.conn.commit()
        return data

class Table:
    def __init__(self, **kwargs):
        self._data={}
        for key, value in kwargs.items():
            self._data[key] = value
    """
    constructor for holding table fields
    """
    def __getattribute__(self, key):
        _data = object.__getattribute__(self, '_data')
        if key in _data:
            return _data[key]
        return object.__getattribute__(self,key)
    """ 
    __gtattribute__ will run anytime you get an attribute
    object.__getattr__ is needed as stack overflow will occur
    due to accessing a variable inside the class over and over
    """
    @classmethod
    def _get_name(cls):
        return cls.__name__.lower()
    """
    returns the name of the class stored as a param (cls)
    """
    @classmethod
    def _get_create_sql(cls):
        keyChosen = False
        fields = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append((name, field.sql_type))
            elif isinstance(field, PrimaryKey):
                if keyChosen:
                    print("Error: Cannot have two Primary Keys compisiteKey class should be made for this functionality")
                    sys.exit()
                keyChosen = True
                if field.get_primaryKeyAutomaticIncrement():
                    fields.append((name, "INTEGER PRIMARY KEY AUTOINCREMENT"))
                else:
                    fields.append((name, "INTEGER"))
        fields = [" ".join(x) for x in fields]
        return CREATETABLE.format(name=cls._get_name(), fields=", ".join(fields))
    """
    parameter cls = a class representing a table
    returns the sql for creating a table
    """
    def _get_insert_sql(self):
        cls = self.__class__
        fields = []
        values = []
        x = cls._get_name()
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values.append((getattr(self,name)))
        vals = str(values[0])
        for i in range(1,len(values)):
            if type(values[i]) != str:
                vals = vals + ", " + str(values[i])
            else:
                vals = vals + ", " + "'"+values[i]+"'"
        name=cls._get_name().upper()
        fields=", ".join(fields)
        placeholders = vals
        return INSERT.format(name=name.upper(), 
                                fields=fields, 
                                placeholders =placeholders)
    """
    returns the sql for inserting a record into a table
    """
    @classmethod
    def _get_select_all_sql(cls):
        return SELECTALL.format(name=cls._get_name(),fields="*")
    """
    returns sql for selecting all of a specified table
    """


class Column:
    def __init__(self, type):
        self.type =type
    @property
    def sql_type(self):
        return PYTHONTYPETOSQLITETYPE[self.type]
    """
    returns the columns type
    """
        
class PrimaryKey:
    def __init__(self, primaryKeyAutomaticIncrement=True):
        self.primaryKeyAutomaticIncrement = primaryKeyAutomaticIncrement

    def get_primaryKeyAutomaticIncrement(self):
        return self.primaryKeyAutomaticIncrement

