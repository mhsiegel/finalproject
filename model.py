from benandjerrys import *
import sqlite3

DBNAME = 'benandjerrys.db'

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

#displays the top 10 ice creams that are tweeted about with pictures
def tweets():
    statement = '''
    SELECT Image, Flavors.Name
    FROM Tweets
    JOIN Flavors
    ON Flavors.Id = Tweets.FlavorId
    GROUP BY Flavors.Id
    ORDER BY COUNT(*) desc
    LIMIT 10
    '''
    cur.execute(statement)
    for row in cur:
        print(row)
# tweets()

#displays the users with the top followers and a picture of the ice cream they tweeted about
def followers():
    statement = '''
    SELECT ScreenName, FollowerCount, Image
    FROM Tweets
    JOIN Flavors
    ON Tweets.FlavorId = Flavors.Id
    ORDER BY FollowerCount DESC
    LIMIT 10
    '''
    cur.execute(statement)
    for row in cur:
        print(row)
# followers()

#displays the ice cream picture, name, and description
def list_of_flavors():
    statement = '''
    SELECT Name, Description, Image
    FROM Flavors
    '''
    cur.execute(statement)
    for row in cur:
        print(row)
# list_of_flavors()

#displays the ice creams that contain chocolate, vanilla, etc.
def flavor(flavor):
    statement = "SELECT Name, Ingredients FROM Flavors WHERE Ingredients LIKE '" + "%" + flavor.title() + "%" + "'"
    cur.execute(statement)
    for row in cur:
        print(row)
# flavor('caramel')
