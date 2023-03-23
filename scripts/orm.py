
import sqlite3#https://docs.python.org/3/library/sqlite3.html
import inspect#https://docs.python.org/3/library/inspect.html
import sys#https://docs.python.org/3/library/sys.html

SELECTTABLES = "SELECT name FROM sqlite_master WHERE type = 'table';"#sql command to select all tables
CREATETABLE = "CREATE TABLE {name} ({fields});"#sql command to create a table
INSERT = 'INSERT INTO {name} ({fields}) VALUES ({placeholders});'#sql command to insert a record
SELECTALL = 'SELECT {fields} FROM {name};'#sql command to select all records

PYTHONTYPETOSQLITETYPE = {#dictionary to convert python types to sqlite types
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bytes: "BLOB",
    bool: "INTEGER",
}


class Database:#class to represent a database
    def __init__(self, path):#constructor to establish connection to a sqlite3 database
        self.conn = sqlite3.Connection(path)#create a connection to the database
    
    def _execute(self,sql):#function to execute sql commands
        return self.conn.execute(sql)#execute the sql command
    
    def create(self, table):#function to create a table
        self._execute(table._get_create_sql())#execute the sql command to create the table
    
    def saveRecord(self, table):#function to save a record
        self._execute(table._get_insert_sql())#execute the sql command to insert the record
        self.conn.commit()#commit the changes
    
    def manualSQLCommand(self,sql):#function to execute a manual sql command
        data = self._execute(sql).fetchall()#execute the sql command and fetch the data
        self.conn.commit()#commit the changes
        return data#return the data

class Table:#class to represent a table
    def __init__(self, **kwargs):#constructor to create a table object
        self._data={}#dictionary to hold the table fields
        for key, value in kwargs.items():#for each key value pair in the kwargs
            self._data[key] = value#add the key value pair to the dictionary
    
    def __getattribute__(self, key):#__gtattribute__ will run anytime you get an attribute object.__getattr__ is needed as stack overflow will occudue to accessing a variable inside the class over and over
        _data = object.__getattribute__(self, '_data')#get the dictionary
        if key in _data:#if the key is in the dictionary
            return _data[key]#return the value
        return object.__getattribute__(self,key)#return the attribute
    @classmethod#https://docs.python.org/3/library/functions.html#classmethod
    def _get_name(cls):#returns the name of the class stored as a param (cls)
        return cls.__name__.lower()#return the name of the table

    @classmethod
    def _get_create_sql(cls):#returns the sql for creating a table
        keyChosen = False#is a primary key chosen
        fields = []#list of fields
        for name, field in inspect.getmembers(cls):#for each field in the class
            if isinstance(field, Column):#if the field is a column
                fields.append((name, field.sql_type))#add the field to the list of fields
            elif isinstance(field, PrimaryKey):#if the field is a primary key
                if keyChosen:#if a primary key has already been chosen
                    print("Error: Cannot have two Primary Keys compisiteKey class should be made for this functionality")#print an error
                    sys.exit()#exit the program
                keyChosen = True#set the keyChosen variable to true
                if field.get_primaryKeyAutomaticIncrement():#if the primary key is set to auto increment
                    fields.append((name, "INTEGER PRIMARY KEY AUTOINCREMENT"))#add the field to the list of fields
                else:#if the primary key is not set to auto increment
                    fields.append((name, "INTEGER"))#add the field to the list of fields
        fields = [" ".join(x) for x in fields]#join the fields together
        return CREATETABLE.format(name=cls._get_name(), fields=", ".join(fields))#return the sql for creating a table
    
    def _get_insert_sql(self):#returns the sql for inserting a record into a table
        cls = self.__class__#get the class
        fields = []#list of fields
        values = []#list of values
        x = cls._get_name()#get the name of the table
        for name, field in inspect.getmembers(cls):#for each field in the class
            if isinstance(field, Column):#if the field is a column
                fields.append(name)#add the field to the list of fields
                values.append((getattr(self,name)))#add the value to the list of values
        vals = str(values[0])#set the first value to vals
        for i in range(1,len(values)):#for each value in the list of values
            if type(values[i]) != str:#if the value is not a string
                vals = vals + ", " + str(values[i])#add the value to vals
            else:#if the value is a string
                vals = vals + ", " + "'"+values[i]+"'"#add the value to vals
        name=cls._get_name().upper()#get the name of the table
        fields=", ".join(fields)#join the fields together
        placeholders = vals#set the placeholders to vals
        return INSERT.format(name=name.upper(), #return the sql for inserting a record into a table
                                fields=fields, 
                                placeholders =placeholders)
  
    @classmethod
    def _get_select_all_sql(cls):#rreturns sql for selecting all of a specified table
        return SELECTALL.format(name=cls._get_name(),fields="*")



class Column:
    def __init__(self, type):#constructor to create a column object
        self.type =type#set the type of the column
    @property
    def sql_type(self):#returns the columns type
        return PYTHONTYPETOSQLITETYPE[self.type]#return the columns type
    
        
class PrimaryKey:#class to represent a primary key
    def __init__(self, primaryKeyAutomaticIncrement=True):#constructor to create a primary key object
        self.primaryKeyAutomaticIncrement = primaryKeyAutomaticIncrement#set the primary key to auto increment

    def get_primaryKeyAutomaticIncrement(self):#returns if the primary key is set to auto increment
        return self.primaryKeyAutomaticIncrement#return if the primary key is set to auto increment

