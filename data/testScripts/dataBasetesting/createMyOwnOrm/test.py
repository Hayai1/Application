# use this for testing python syntax #
class Table:
    def __init__(self,x) -> None:
        self.x = x
class QueryTools:
    class Where():
        pass
    class set():
        pass
def update(param):
    print(param[Table])
    print(param[QueryTools.Where])
table = Table(19)

update({Table : table.x, QueryTools.set : 'name = 10 and hp = 100 and characterID = 1', QueryTools.Where : 'condtion'})