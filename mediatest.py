import unittest
import media
import datetime

class MediaTest(unittest.TestCase):

    def test_first(self):
        b1 = media.Book("Python", 10.0)
        b2 = media.Book("Numpy", 20, datetime.datetime(2020,9,30,16,8),"red",authors = ["Cyril","Toto"],nbPage=90)
        self.assertAlmostEqual(10.55, b1.netPrice(), delta=1e-3)