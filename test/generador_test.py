import unittest
from generador import Generador
import estadistica

class TestGenerador(unittest.TestCase):
    def test_truncate(self):
        gen = Generador(decimals=5)
        self.assertEqual(gen.truncate(0.1234567), 0.12345)
        gen.decimals = 2
        self.assertEqual(gen.truncate(0.1234567), 0.12)

    def test_rnd(self):
        gen = Generador(x=6, c=7, k=3, g=3)
        self.assertEqual(13, gen.a)
        self.assertEqual(8, gen.m)

        self.assertEqual(0.625, estadistica.truncate(gen.rnd(), 4))
        self.assertEqual(5, gen.x)
        self.assertNotEqual(gen.rnd(), gen.rnd())

