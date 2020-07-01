import datetime
from typing import *
import abc

class Publisher:

    def __init__(self, name):
        self.name = name


class Item(metaclass=abc.ABCMeta):

    def __init__(self, id, price):
        self.id = id
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Negative price")
        else:
            self._price = value

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __lt__(self, other):
        return self.price - other.price

class Media(Item, metaclass=abc.ABCMeta):

    def __init__(self, id, title, price, author=None, date=datetime.datetime.now(), publisher = Publisher(None) ):
        super().__init__(id,price)
        self.title = title
        self.author = author
        self.date = date
        self.publisher = publisher

    @abc.abstractmethod
    def netPrice(self):...

class Book(Media):

    nbBook = 0
    vat = 0.055

    def __init__(self, id, title, price, author=None, date=datetime.datetime.now(), publisher = Publisher(None), nbPage = 0):
        super().__init__(id,title,price,author,date,publisher)
        self.nbPage = nbPage
        Book.nbBook += 1

    @property
    def netPrice(self):
        return self.price * (1 + Book.vat) * 0.95 + 0.01

    def __del__(self):
        Book.nbBook -= 1

class Cd(Media):

    def __init__(self, id, title, price, author=None, date=datetime.datetime.now(), publisher = Publisher(None), nbTrack = 0):
        super().__init__(id,title,price,author,date,publisher)
        self.nbTrack = nbTrack

    def netPrice(self):
        return self.price * 1.2

class Cart:

    def __init__(self):
        self.items:List[Media]=[]

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

    @property
    def totalNetPrice(self):
        return sum([i.netPrice for i in self.items])

    @property
    def nbItem(self):
        return len(self.items)

class AbstractRepository(metaclass=abc.ABCMeta):

    def __init__(self, path):
        self.path = path
        self.medias:List[Media] = []

    @abc.abstractmethod
    def load(self):... #Lit la source de données et charge medias

    def getMediaByPrice(self, price: float) -> List[Media]:
        return [m for m in self.medias if m.price <= price]

    def getMediaByTitle(self, title: float) -> List[Media]:
        return [m for m in self.medias if title.upper() in m.title.upper()]

import csv
class CsvRepository(AbstractRepository):

    def load(self):
        with open(self.path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                book = Book(int(row["id"]), row["title"], float(row["price"]))
                self.medias.append(book)

import pickle
class PickleRepository(AbstractRepository):

    def load(self):
        with open(self.path, "rb") as f:
            l = pickle.load(f)
            for dico in l:
                b = Book(0,"",0)
                b.__dict__ = dico
                b._price = float(dico["price"])
                self.medias.append(b)

import json
class JsonRepository(AbstractRepository):

    def load(self):
        with open(self.path) as f:
            l = json.load(f)
            for dico in l:
                b = Book(int(dico["id"]),dico["title"],float(dico["price"]))
                self.medias.append(b)

import sqlite3 as db
class DbRepository(AbstractRepository):

    def load(self):
        with db.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("select id,title,price from book")
            for row in cursor:
                b = Book(row[0],row[1],row[2])
                self.medias.append(b)

import unittest
class MediaTest(unittest.TestCase):

    def testBook(self):
        b = Book(0,None,10)
        self.assertAlmostEqual(10.0325, b.netPrice, delta = 1e-4)

    def testNbBook(self):
        b = Book(0,None,0)
        self.assertEqual(1, Book.nbBook)
        del(b)
        self.assertEqual(0, Book.nbBook)

    def testNegativePrice(self):
        b = Book(0,None,0)
        with self.assertRaises(ValueError):
            b.price = -10

    def testPublisher(self):
        p = Publisher("O'Reilly")
        b = Book(0,None,0,publisher=p)
        self.assertEqual("O'Reilly", b.publisher.name)

    def testCart(self):
        cart = Cart() #Liste de Book
        b = Book(0,"Python",10)
        cart.add(b)
        self.assertEqual(1, cart.nbItem)
        b2 = Book(1,"Numpy",20)
        dict = b2.__dict__
        dict["_price"] = -99
        dict["toto"] = "titi"
        b2.__dict__ = dict
        cart.add(b2)
        self.assertEqual(2, cart.nbItem)
        #self.assertAlmostEqual(30.0875, cart.totalNetPrice, delta=1e-4)
        cart.remove(b2)
        self.assertEqual(1, cart.nbItem)

    # Gérer des Book(nbPage), Cd(nbTrack), Dvd(zone)
    # Media
    # Gérer la TVA 20%
    # Bonus : Créer les classes Stylo, MachineALaver => Créer Item
    # Bonus : Book hérite de Media et Media hérite de Item
    # Bonus : stylo hérite de Item
    # MAJ Cart

    #        Item
    #     |        |
    #   Media     Stylo
    #   |  |  |
    # Book Cd Dvd

        # Passer Media en abstract
        # Passe Media.netPrice en abstract
        # Corriger les erreurs et tester le cart.netPrice

    def testEquality(self):
        b1 = Book(1,"",0)
        b2 = Book(1,"",0)
        self.assertEqual(b1, b2)

    def testRepository(self):
        #repo:AbstractRepository = CsvRepository("data/media/books.csv")
        #repo: AbstractRepository = JsonRepository("data/media/books.json")
        #repo: AbstractRepository = PickleRepository("data/media/books.pickle")
        repo: AbstractRepository = DbRepository("data/media/books.db3")
        repo.load()
        medias = repo.medias
        self.assertEqual(6, len(medias))
        medias = repo.getMediaByPrice(10)
        self.assertEqual(2, len(medias))
        medias = repo.getMediaByTitle("py")
        self.assertEqual(2, len(medias))


