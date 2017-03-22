import sqlite3

class DBHelper:
    def __init__(self, dbname="ollie.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def addItem(self, itemText, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (itemText, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def deleteItem(self, itemText, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (itemText, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def getItems(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]
    
