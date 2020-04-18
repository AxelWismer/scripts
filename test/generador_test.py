import unittest
from generador import Generador

class TestGenerador(unittest.TestCase):
    def test_truncate(self):
        gen = Generador(decimals=5)
        self.assertEqual(gen.truncate(0.1234567), 0.12345)
        gen.decimals = 2
        self.assertEqual(gen.truncate(0.1234567), 0.12)

    def test_rnd(self):
        gen = Generador(x=10, c=12, k=3, g=10)
        self.assertEqual(0.0224609375, gen.rnd())
        self.assertNotEqual(gen.rnd(), gen.rnd())
