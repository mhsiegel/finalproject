import sqlite3
import requests
import json
from bs4 import BeautifulSoup
import secrets
from requests_oauthlib import OAuth1

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
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        if 'https' in unique_ident:
            auth = OAuth1(secrets.twitter_api_key, secrets.twitter_api_secret, secrets.twitter_access_token, secrets.twitter_access_token_secret)
            response = requests.get(unique_ident, auth=auth)
            CACHE_DICTION[unique_ident] = response.text
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close()
            return CACHE_DICTION[unique_ident]
        print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

class BenandJerrys:
    def __init__(self, name = "No name", mix_ins = "No mixes", desc = "No description", image = "No image", url=None):
        self.name = name
        self.mix_ins = mix_ins
        self.description = desc
        self.image = image
        self.url = url
    def __str__(self):
        return "{}\nIngredients: {}\nDescription: {}".format(self.name, self.mix_ins, self.description, self.url)

class Tweet:
    def __init__(self, text, username, creation_date, num_retweets, num_favorites, id_tweet):
        self.text = text
        self.username = username
        self.creation_date = creation_date
        self.num_retweets = num_retweets
        self.num_favorites = num_favorites
        self.id = id_tweet

    def __str__(self):
        return "{}: {} \n [retweeted {} times] \n [favorited {} times] \n [popularity {}] \n [tweeted on {}] | [id: {}]".format(self.username, self.text, self.num_retweets, self.num_favorites, self.popularity_score, self.creation_date, self.id)

def icecreamflavors():
    list_of_icecreams = []
    url = 'https://www.benjerry.com/'
    baseurl = url + '/flavors/ice-cream-pints/'
    page_text = make_request_using_cache(baseurl)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    get_info = page_soup.find_all('div', class_ = 'row-content')
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
                mix_ins = get_additional_information.find('p', id = 'productDetails-product_desc-mobile').text.strip()
            except:
                mix_ins = "Information on mix-ins not available"
            try:
                description = get_additional_information.find('p', id="productDetails-product_story").text.strip()
            except:
                description = "Description not available"
            try:
                image = get_additional_information.find('li', class_ = 'photo on-top').find('noscript').find('img')['src']
            except:
                image = "No image available"
    #     createlist = BenandJerrys(name = name, mix_ins = mix_ins, desc = description, image = image)
    #     print(createlist)
    #     list_of_icecreams.append(createlist)
    #     print("\n")
    # return list_of_icecreams
icecreamflavors()

def get_tweets(flavor):
    twitter_api = 'https://api.twitter.com/1.1/search/tweets.json?q={}&count={}'.format(flavor, 10)
    twitter_request = make_request_using_cache(twitter_api)
    print(twitter_request)
    # twitter_data = json.loads(twitter_request)
    # tweet= []
    # for t in twitter_data['statuses']:
    #     if 'retweeted_status' not in t:
    #         if 'RT @' not in t['text']:
    #             num_favorites = t['favorite_count']
    #             num_retweets = t['retweet_count']
    #             text = t['text']
    #             username = "@" + t['user']['screen_name']
    #             creation_date = t['created_at']
    #             id_tweet = t['id_str']
    #     createlist2 = Tweet(text = text, username = username, creation_date = creation_date, num_retweets = num_retweets, num_favorites = num_favorites, id_tweet = id_tweet)
    #     tweet.append(createlist2)
    #     print("\n")
    # return tweet
get_tweets('Vanilla')

#PLOTLY distribution of ratings for all ice creams, ice cream ingredient, 10 most frequent words

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
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'Description' TEXT NOT NULL,
            'Mix-Ins' TEXT NOT NULL,
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
            'Username' TEXT
            'CreationDate' REAL,
            'Text' TEXT,
            'NumFavorites'
            'NumRetweets'
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
    for flavor in flavors:
        insertion = (None, flavor.name, flavor.description, flavor.mix_ins, flavor.image)
        statement = 'INSERT OR IGNORE INTO "Flavors" '
        statement += 'VALUES (?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()
    conn.close()

# def insert_tweet_data():
#     flavor_tweets = tweets()
#     conn = sqlite3.connect(DBNAME)
#     cur = conn.cursor()
#     for tweet in flavor_tweets:
#         insertion = (None, tweet.)

if __name__ == '__main__':
    init_db()
    # insert_icecream_data()
#     ben_and_jerrys_pint_list = ["Caramel Chocolate Cheesecake", "Chillin' the Roast", "Chocolate Shake It", "Gimme S’more", "Glampfire Trail Mix", "One Sweet World", "Pecan Sticky Buns", "Americone Dream", "Banana Split", "Blondie Ambition", "Boom Chocolatta Cookie Core", "Bourbon Pecan Pie", "Brewed to Matter", "Brownie Batter Core", "Cheesecake Brownie", "Cherry Garcia", "Chocolate Chip Cookie Dough", "Chocolate Fudge Brownie", "Chocolate Therapy", "Chubby Hubby", "Chunky Monkey", "Cinnamon Buns", "Coconuts for Caramel Core", "Coffee Toffee Bar Crunch", "Coffee, Coffee BuzzBuzzBuzz", "Cookies & Cream Cheesecake Core", "Everything But The...", "Half Baked", "Karamel Sutra Core", "Keep Caramel & Cookie On", "Milk & Cookies", "Mint Chocolate Cookie", "New York Super Fudge Chunk", "Oat of This Swirled", "Peanut Buttah Cookie Core", "Peanut Butter Cup", "Peanut Butter Fudge Core", "Peanut Butter World", "Phish Food", "Pistachio Pistachio", "Pumpkin Cheesecake", "Red Velvet Cake", "S'mores", "Salted Caramel Almond", "Salted Caramel Core", "Spectacular Speculoos™ Cookie Core", "Strawberry Cheesecake", "The Tonight Dough", "Triple Caramel Chunk", "Truffle Kerfuffle", "Urban Bourbon", "Vanilla", "Vanilla Caramel Fudge", "Vanilla Toffee Bar Crunch"]
#     help_commands = """
#         list flavors
#            available anytime
#            lists all Ice Cream Flavors in the regular pint section
#            valid inputs: list flavors
#         moreinfo <result_number>
#            available only if there is an active result set
#            lists all Places nearby a given result
#            valid inputs: an integer 1-len(result_set_size)
#         tweets <result_number>
#             available only if there is an active results set
#             lists up to 5 most "popular" tweets that mention the selected ice cream
#         exit
#            exits the program
#         help
#            lists available commands (these instructions)
#        """
#     ben_jerry =[0]
#     userinput = input ('Enter command (or "help" for options): ')
#     while userinput != 'exit':
#         if userinput.lower() == "help":
#             print(help_commands)
#         elif userinput.strip().lower().split()[0] == 'list':
#             while userinput.strip().lower().split()[1] != 'list flavors':
#                 userinput = input("Please enter 'list flavors' to see a list of flavors")
#             ben_jerry = icecreamflavors(userinput.strip().lower().split()[1])
#             count = 1
#             count_dict = {}
#             print("Ben and Jerry's Ice Cream Pint Flavors: " + userinput.strip().upper().split()[1])
#             print(' ')
#             for s in ben_jerry:
#                 print(str(count), s)
#                 count_dict[count] = s
#                 count += 1
#
#         elif userinput.strip().lower().split()[0] == 'moreinfo' and isinstance(ben_jerry[0], moreinfo):
#             while int(userinput.strip().split()[1]) not in count_dict or (userinput.strip().split()[1].isdigit()) == False:
#                 userinput = input ("Enter 'moreinfo' with a number following that corresponds with the ice cream you want more information on ")
#             icecream_data = moreinfo(count_dict[int(userinput.strip().split()[1])])
#             icecream_count = 1
#             print('Information for ' + count_dict[int(userinput.strip().split()[1])].name + " " +  count_dict[int(userinput.strip().split()[1])].type_)
#             for icecream in icecream_data:
#                 print(str(icecream_count), icecream)
#                 icecream_count += 1
#
#         elif userinput.strip().lower().split()[0] == 'tweets' and isinstance(ben_jerry[0], BenandJerrys):
#             while int(userinput.strip().lower().split()[1]) not in count_dict or (userinput.strip().split()[1].isdigit()) == False:
#                 userinput = input("Enter the word 'tweets' followed by a number that corresponds with the national site you want to see tweets from: ")
#             twitter_d = get_tweets_for_site(count_dict[int(userinput.strip().split()[1])])
#             for t in twitter_d:
#                 print(t)
#                 print('-' * 20)
#         else:
#             print("Please make sure your input is one of the commands: ")
#
#         userinput = input ('Enter command (or "help" for options): ')
#     print("Goodbye!")
