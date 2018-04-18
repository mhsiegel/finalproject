from benandjerrys import *
import sqlite3

DBNAME = 'benandjerrys.db'

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

#displays the ice cream picture, name, and description

# list_of_flavors()

#displays the ice creams that contain chocolate, vanilla, etc.
def flavor(flavor):
    statement = "SELECT Name, Ingredients FROM Flavors WHERE Ingredients LIKE '" + "%" + flavor.title() + "%" + "'"
    cur.execute(statement)
    for row in cur:
        print(row)
flavor('caramel')
