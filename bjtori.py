import sqlite3
import requests
import json
from bs4 import BeautifulSoup

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

class BenandJerrys:
    def __init__(self, name = "No name", ingredients = "No ingredients", desc = "No description", rating = "No rating", review = "No review", recommend = "No recommendation", account = "No account name", url=None):
        self.name = name
        self.ingredients = ingredients
        self.description = desc
        self.rating = rating
        self.review = review
        self.recommend = recommend
        self.accountname = account
        self.url = url
    def __str__(self):
        return "{}\nIngredients: {}\nDescription: {}".format(self.name, self.ingredients, self.description, self.url)

def icecreamflavors():
    # flavor_icecream=flavor_icecream.split()
    # # flavor = "-".join(flavor_icecream)
    list_of_icecreams = []
    url = 'https://www.benjerry.com/'
    # baseurl = url + 'flavors/' + str(flavor) + '-ice-cream'
    baseurl = url + 'flavors/ice-cream-pints'
    page_text = make_request_using_cache(baseurl)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    get_info = page_soup.find_all('div', class_ = 'row-content')
    # print(get_info)
    for x in get_info:
        if x.find('h4') != None:
            name = x.find('h4').text
            # print(name)
        get_next_link = x.find('a')['href']
        add_url = url + get_next_link
    new_requests = make_request_using_cache(add_url)
    new_page_soup = BeautifulSoup(new_requests, 'html.parser')
        # print(new_page_soup)
    get_additional_information = new_page_soup.find('div', class_ = 'mobile-only two-thirds-last grid-right FDMultiImage')
    for info in get_additional_information:
        if get_additional_information != None:
            try:
                ingredients = get_additional_information.find('p', id = 'productDetails-product_desc-mobile').text.strip()
            except:
                ingredients = "Information on ingredients not available"
            try:
                description = get_additional_information.find('p', id="productDetails-product_story").text.strip()
            except:
                description = "Description not available"
            try:
                image=get_additional_information.find('figure')
                pic=image.find('img')['src']
                print(pic)
        #         # image = img.find(img['src'])
        # except:
        #     image = None
            # print(image)
        # get_more_info = new_page_soup.find('div', id = 'expReviews')
        # # print(get_more_info)
        # if get_more_info != None:
        #     r = get_more_info.find('div', class_ = 'accordion-content-style')
        #     print(r)
        #     ra = r.find('div', id = 'BVRRContainer')
            # print(ra)
    #             rat = ra.find('div', class_ = 'bv-cleanslate bv-cv2-cleanslate')
    #             # print(rat)
    #             rating = r.find('span', class_ = 'bv-secondary-rating-summary-rating').text.strip()
    #         except:
    #             rating = "No average rating"
    #         # print(rating)
    #         # for info in get_more_info:
    #         try:
    #             r = get_more_info.find('div', class_ = "bv-content-item-avatar-offset bv-content-item-avatar-offset-on")
    #             # print(r)
    #             rev = r.find('div', class_ = 'bv-content-container')
    #             review = rev.find('div', class_ = '"bv-content-summary"')
    #         except:
    #             review = "No review avaible"
    #         # print(review)
    #         try:
    #             recommend = info.find('span', class_ = 'bv-content-data-label')
    #         except:
    #             recommend = "No recommendation available"
    #         # print(recommend)
    #         try:
    #             account = info.find('h3')
    #         except:
    #             account = "No username available"
    #         # print(account)
            createlist = BenandJerrys(name = name, ingredients=ingredients, desc= description, rating = None, review = None, recommend = None, account = None, url = add_url)
        # print(createlist)
            list_of_icecreams.append(createlist)
            # print("\n")
            # print(list_of_icecreams)
        return list_of_icecreams
icecreamflavors()

# #takes in the one flavor object from the class benandjerry
# def moreinfo(icecreamflavor):
#     icecream=icecreamflavor.split()
#     one_flavor = "-".join(icecream)
#     # icecreamname = icecreamflavor.name
#     info_of_icecream = []
#     url = 'https://www.benjerry.com/'
#     # baseurl = url + 'flavors/' + str(one_flavor) + '-ice-cream'
#     baseurl = url + 'flavors/' + str(one_flavor)
#     # baseurl = url + 'flavors/'
#     page_text = make_request_using_cache(baseurl)
#     page_soup = BeautifulSoup(page_text, 'html.parser')
#     get_info = page_soup.find_all('div', class_ = 'row-content')
#     for x in get_info:
#         get_next_link = x.find('a')['href']
#
#
#         createlist2 = more_info()
#         print(createlist2)
#         info_of_icecream.append(createlist2)
#     return info_of_icecream
# moreinfo('ice cream pints')

#make into a list; create tuple and list through classes

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
            'Ingredients' TEXT NOT NULL
            'Image'
         );
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS 'Ratings';
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'Ratings' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Account' TEXT
            'Rating' REAL,
            'Review' TEXT,
            'FlavorId' INTEGER
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def insert_icecream_data():
    flavors = icecreamflavors('ice cream pints')
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for flavor in flavors:
        insertion = (None, flavor.name, flavor.description, flavor.ingredients)
        statement = 'INSERT OR IGNORE INTO "Flavors" '
        statement += 'VALUES (?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()
    conn.close()
#
# if __name__ == '__main__':
    # init_db()
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
