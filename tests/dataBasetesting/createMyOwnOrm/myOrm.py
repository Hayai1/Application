
import sqlite3
import inspect
import sys

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
CREATE_TABLE_SQL = "CREATE TABLE {name} ({fields});"
INSERT_SQL = 'INSERT INTO {name} ({fields}) VALUES ({placeholders});'
SELECT_ALL_SQL = 'SELECT {fields} FROM {name};'
SELECT_WHERE_SQL = 'SELECT {fields} FROM {name} WHERE {query};'

SQLITE_TYPE_MAP = {
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
    @property
    def tables(self):
        return [x[0] for x in self._execute(SELECT_TABLES_SQL).fetchall()]
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
        cursor = self._execute(table._get_insert_sql())
        self.conn.commit()
    """
    saves a record once the tables class has been instancited
    """
    def getAll(self, table):
        return self._execute(table._get_select_all_sql()).fetchall()
    """
    returns all the records from a table given as an arg
    """
    def getWhere(self, **kwargs):
        tableAndCondition={}
        for key, value in kwargs.items():
            tableAndCondition[key] = value
        table = tableAndCondition['table']
        del tableAndCondition['table']
        Condition = tableAndCondition
        return self._execute(table._get_select_where_sql(Condition)).fetchall()
    """
    returns records from a specified table with a specified condition
    """

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
            elif isinstance(field, ForeignKey):
                fields.append((name, "INTEGER"))
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
        return CREATE_TABLE_SQL.format(name=cls._get_name(), fields=", ".join(fields))
    """
    parameter cls = a class representing a table
    returns the sql for creating a table
    """
    def _get_insert_sql(self):
        cls = self.__class__
        fields = []
        values = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values.append((getattr(self,name)))
            elif isinstance(field, ForeignKey):
                fields.append(name)
                values.append((getattr(self,name)))
        vals = str(values[0])
        for i in range(1,len(values)):
            if type(values[i]) != str:
                vals = vals + ", " + str(values[i])
            else:
                vals = vals + ", " + "'"+values[i]+"'"
        return INSERT_SQL.format(name=cls._get_name(), 
                                fields=", ".join(fields), 
                                placeholders = vals)
    """
    returns the sql for inserting a record into a table
    """
    @classmethod
    def _get_select_all_sql(cls):
        return SELECT_ALL_SQL.format(name=cls._get_name(),fields="*")
    """
    returns sql for selecting all of a specified table
    """
    @classmethod
    def _get_select_where_sql(cls, condition):
        fields = ""
        for key in condition:
            value = condition[key]
            valueType = type(value)
            if key == "le":
                fields =  fields + value + " "
            elif type(value) == int:
                fields = fields + key + " = " + str(value) + " "
            elif valueType == str:
                fields = fields + key + " = '" + value  + "' "
        return SELECT_WHERE_SQL.format(fields="*",name=cls._get_name(),query=fields)
    """
    returns sql for selecting a record from a specified table
    and specified condition
    """
class Column:
    def __init__(self, type):
        self.type =type
    @property
    def sql_type(self):
        return SQLITE_TYPE_MAP[self.type]
    """
    returns the columns type
    """
class ForeignKey:
    def __init__(self, table):
        self.table = table
        
class PrimaryKey:
    def __init__(self, primaryKeyAutomaticIncrement=True):
        self.primaryKeyAutomaticIncrement = primaryKeyAutomaticIncrement

    def get_primaryKeyAutomaticIncrement(self):
        return self.primaryKeyAutomaticIncrement