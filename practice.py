import sqlite3

DBNAME = 'benandjerrys.db'

def flavor(flavor):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = "SELECT Name, Ingredients "
    statement += "FROM Flavors "
    statement += "WHERE Ingredients LIKE "
    statement += "'% " + flavor.title() + "%'"
    print(statement)
flavor('Chocolate')
