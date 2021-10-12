import unittest
# from typing import List
import mylib
import config
import pandas
import geometry


class MyClass(unittest.TestCase):

    def test1(self):
        self.assertEqual(2, 1+1)

    def test_iseven(self):
        res = mylib.is_even(8)
        self.assertTrue(res)

    def test_isprime(self):
        self.assertTrue(mylib.is_prime(7))
        self.assertFalse(mylib.is_prime(8))

    def test_sum(self):
        mylib.sum1([1,2,3])
        mylib.sum2(1,2,3)
        x = 1
        print(f"totototto {x:.1f} ")

    def test_rectangle(self):
        r1 = geometry.Rectangle(3.0,2.0)
        self.assertEqual(10, r1.perimeter())
        self.assertAlmostEqual(10,r1.perimeter(),delta=1e-2)
        self.assertAlmostEqual(6, r1.area, delta=1e-2)
        # geometry.Rectangle.perimeter(r1)
        self.assertEqual(3, r1.length)
        print(r1.coord)
        del(r1)



