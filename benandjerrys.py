import sqlite3
import requests
import json
from bs4 import BeautifulSoup
from secrets import *
import tweepy

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def make_tweepy_request_using_cache(url):
    tweepycache = 'tweepycache.json'
    try:
        cache_file = open(tweepycache, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}



class BenandJerrys:
    def __init__(self, name = "No name", ingredients = "No ingredients", desc = "No description", image = "No image", id = 0, url=None):
        self.name = name
        self.ingredients = ingredients
        self.description = desc
        self.image = image
        self.url = url
        self.id_ = id
    def __str__(self):
        return "{}\nIngredients: {}\nDescription: {}".format(self.name, self.ingredients, self.description, self.url)

def icecreamflavors():
    list_of_icecreams = []
    url = 'https://www.benjerry.com'
    baseurl = url + '/flavors/ice-cream-pints/'
    page_text = make_request_using_cache(baseurl)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    get_info = page_soup.find_all('div', class_ = 'row-content')
    id_num = 1
    for x in get_info:
        if x.find('h4') != None:
            name = x.find('h4').text
        get_next_link = x.find('a')['href']
        add_url = url + get_next_link
        new_requests = make_request_using_cache(add_url)
        new_page_soup = BeautifulSoup(new_requests, 'html.parser')
        get_additional_information = new_page_soup.find('div', class_ = 'mobile-only two-thirds-last grid-right FDMultiImage')
        if get_additional_information != None:
            try:
                ingredients = get_additional_information.find('p', id = 'productDetails-product_desc-mobile').text.strip()
            except:
                ingredients = "Information on mix-ins not available"
            try:
                description = get_additional_information.find('p', id="productDetails-product_story").text.strip()
            except:
                description = "Description not available"
            try:
                image = url + get_additional_information.find('li', class_ = 'photo on-top').find('noscript').find('img')['src']
            except:
                image = "No image available"
        createlist = BenandJerrys(name = name, ingredients = ingredients, desc = description, id = id_num, image = image)
        id_num +=1
        list_of_icecreams.append(createlist)
    return list_of_icecreams

def get_tweets():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    searched_tweets = [status for status in tweepy.Cursor(api.search, q='@benandjerrys').items(1000)]
    return searched_tweets

DBNAME = 'benandjerrys.db'
def init_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error in e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'Flavors';
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'Flavors' (
            'Id' INTEGER PRIMARY KEY,
            'Name' TEXT NOT NULL,
            'Description' TEXT NOT NULL,
            'Ingredients' TEXT NOT NULL,
            'Image' TEXT
         );
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS 'Tweets';
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'Tweets' (
            'TweetId' INTEGER PRIMARY KEY AUTOINCREMENT,
            'UserId' TEXT,
            'ScreenName' TEXT,
            'FollowerCount' INTEGER,
            'TweetText' TEXT,
            'NumRetweets' INTEGER,
            'FlavorId' INTEGER
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def insert_icecream_data():
    flavors = icecreamflavors()
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    tweet_num = 0
    for flavor in flavors:
        insertion = (flavor.id_, flavor.name, flavor.description, flavor.ingredients, flavor.image)
        statement = 'INSERT OR IGNORE INTO "Flavors" '
        statement += 'VALUES (?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()
        tweet_num+=1
    conn.close()

def insert_tweet_data(tweets):
    flavors = icecreamflavors()
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for tweet in tweets:
        for flavor in flavors:
            if flavor.name.lower() in tweet.text.lower():
                insertion = (tweet.id, tweet.user.id, tweet.user.screen_name, tweet.user.followers_count, tweet.text.encode('utf8'), tweet.retweet_count, flavor.id_)
                statement = 'INSERT OR IGNORE INTO "Tweets" '
                statement += 'VALUES (?,?,?,?,?,?,?)'
                cur.execute(statement, insertion)
                conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    insert_icecream_data()
    tweets = get_tweets()
    insert_tweet_data(tweets)
