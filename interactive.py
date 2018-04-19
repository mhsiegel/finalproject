from flask import Flask, render_template, request
from benandjerrys import *
import sqlite3
import tweepy

DBNAME = 'benandjerrys.db'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tweets')
def toptweets():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
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
    my_list = []
    for row in cur:
        my_list.append(row)
    return render_template('tweets.html', tweets = my_list)

@app.route('/followers')
def followers():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
    SELECT ScreenName, FollowerCount, Image
    FROM Tweets
    JOIN Flavors
    ON Tweets.FlavorId = Flavors.Id
    ORDER BY FollowerCount DESC
    LIMIT 10
    '''
    cur.execute(statement)
    follower_list = []
    for row in cur:
        follower_list.append(row)
    return render_template('followers.html', followers = follower_list)

@app.route('/icecream')
def list_of_flavors():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
    SELECT Name, Description, Image
    FROM Flavors
    '''
    cur.execute(statement)
    icecream = []
    for row in cur:
        icecream.append(row)
    return render_template('icecream.html', icecream = icecream)

@app.route('/add')
def enter_input():
    return render_template('add.html')

@app.route('/postflavor', methods=["POST"])
def postflavor():
    flavor = request.form.get('flavor', None).title()
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = "SELECT Name, Ingredients, Image "
    statement += "FROM Flavors "
    statement += "WHERE Ingredients LIKE "
    statement += "'%" + str(flavor).title()+ "%'"
    cur.execute(statement)
    contain_flavor = []
    for row in cur:
        contain_flavor.append(row)
    return render_template('containsflavor.html', contain_flavor = contain_flavor, flavor = flavor)

if __name__ == '__main__':
    app.run(debug=True)
