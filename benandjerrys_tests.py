from benandjerrys import *
import unittest
from interactive import *

class TestBenandJerrys(unittest.TestCase):
    def testConstructor(self):
        bj1 = BenandJerrys()
        bj2 = BenandJerrys("Vanilla", "Vanilla Ice Cream", "When you dig into this pint, you’ll find a rich, creamy Vanilla that’s more vanilla-tasting than any Vanilla you’ve ever tasted.")

        self.assertEqual(bj1.name, "No name")
        self.assertEqual(bj1.ingredients, "No ingredients")
        self.assertEqual(bj1.description, "No description")

        self.assertEqual(bj2.name, "Vanilla")
        self.assertEqual(bj2.ingredients, "Vanilla Ice Cream")
        self.assertEqual(bj2.description, "When you dig into this pint, you’ll find a rich, creamy Vanilla that’s more vanilla-tasting than any Vanilla you’ve ever tasted.")

    def testString(self):
        bj1 = BenandJerrys()
        bj2 = BenandJerrys("Red Velvet Cake", "Red Velvet Cake Ice Cream with Red Velvet Cake Pieces & a Cream Cheese Frosting Swirl", "From the velvety-rich ice cream packed with actual cake pieces to the dreamy cream cheese frosting, there's a whole lotta Red Velvet Cake revelry aheadia – & it's best to revel in it before it melts. Enjoy!")

        self.assertEqual(bj1.__str__(), "No name\nIngredients: No ingredients\nDescription: No description")

        self.assertEqual(bj2.__str__(), "Red Velvet Cake\nIngredients: Red Velvet Cake Ice Cream with Red Velvet Cake Pieces & a Cream Cheese Frosting Swirl\nDescription: From the velvety-rich ice cream packed with actual cake pieces to the dreamy cream cheese frosting, there's a whole lotta Red Velvet Cake revelry aheadia – & it's best to revel in it before it melts. Enjoy!")

class TestDataBase(unittest.TestCase):
    def test_flavors_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = "SELECT * FROM Flavors"
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 54)

        sql = '''
            SELECT Flavors.Id, Name, Description, Ingredients
            FROM Flavors
            WHERE Ingredients LIKE "%Coffee%"
            '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 5)
        self.assertEqual(result_list[0][0], 2)
        conn.close()

    def test_tweets_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT ScreenName, FlavorId
            FROM Tweets
            WHERE FollowerCount = 9
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 2)

        sql = '''
            SELECT COUNT(*)
            FROM Tweets
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 33)
        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Image, Flavors.Name
            FROM Tweets
                JOIN Flavors
                ON Flavors.Id = Tweets.FlavorId
            GROUP BY Flavors.Id
            ORDER BY COUNT(*) desc
            LIMIT 10
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()[0][1]
        self.assertEqual((result_list), 'Chocolate Chip Cookie Dough')
        conn.close()

# class TestTweepy(unittest.TestCase):
#     def testtweepy(self):
#         t1 = get_tweets()
#         # print(t1)
#         self.assertEqual(t1.user.id, 973258148105543680)
#         # ex. chunky test has 442 followers

# class TestFlask(unittest.TestCase):
    # def setUp(self):
        # self.

if __name__ == '__main__':
    unittest.main()
