from benandjerrys import *
import unittest

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

if __name__ == '__main__':
    unittest.main()
