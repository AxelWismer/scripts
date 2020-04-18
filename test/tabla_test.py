import unittest
from tabla import Tabla, Uniforme, Exponencial, Normal, Poisson

# Muestras
muestra_1 = [0.15, 0.22, 0.41, 0.65, 0.84, 0.81, 0.62, 0.45, 0.32, 0.07, 0.11, 0.29, 0.58, 0.73, 0.93, 0.97, 0.79, 0.55,
             0.35, 0.09, 0.99, 0.51, 0.35, 0.02, 0.19, 0.24, 0.98, 0.10, 0.31, 0.17]
muestra_2 = [0.10, 0.25, 1.53, 2.83, 3.50, 4.14, 5.65, 6.96, 7.19, 8.25, 1.20, 5.24, 4.75, 3.96, 2.21, 3.15, 2.53, 1.16,
             0.32, 0.90, 0.87, 1.34, 1.87, 2.91, 0.71, 1.69, 0.69, 0.55, 0.43, 0.26]

class TestChiUniforme(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tabla = Uniforme(num_intervalos=5, datos=muestra_1, valor_minimo=0, valor_maximo=1, decimals=2)
        cls.tabla.chi()
        cls.fe = fe = []
        cls.fo = fo = []
        cls.c = c = []
        for interv in cls.tabla.intervalos:
            fe.append(interv.fe)
            fo.append(interv.fo)
            c.append(round(interv.c, 15))

    def test_c_acum(self):
        self.assertEqual(1.66666666666667, round(self.tabla.c_acum, 14))

    def test_fe(self):
        self.assertEqual(len(self.tabla.datos), sum(self.fe))
        self.assertListEqual([6, 6, 6, 6, 6], self.fe)

    def test_fo(self):
        self.assertListEqual([8, 7, 5, 4, 6], self.fo)

    def test_c(self):
        self.assertListEqual([0.666666666666667, 0.166666666666667, 0.166666666666667, 0.666666666666667, 0], self.c)


# class TestChiNormal(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.tabla = Tabla(num_intervalos=10, datos=muestra_2, valor_minimo=0, valor_maximo=1, decimals=2)
#         cls.fe = fe = []
#         cls.fo = fo = []
#         cls.c = c = []
#         for interv in cls.tabla.intervalos:
#             fe.append(round(interv.fe, 15))
#             fo.append(interv.fo)
#             c.append(round(interv.c, 15))
#
#     def test_c_acum(self):
#         self.assertEqual(1.66666666666667, round(self.tabla.c_acum, 14))
#
#     def test_fe(self):
#         self.assertListEqual([9.58677200422917, 6.4979122911512, 4.40428374898948, 2.98522271038169, 2.02338340090446,
#                               1.37144889485724, 0.929567807250166, 0.630060887807147, 0.427055153210029,
#                               0.289457903851135], self.fe)
#
#     def test_fo(self):
#         self.assertListEqual([10, 6, 4, 3, 2, 2, 1, 1, 1, 0], self.fo)

    # def test_c(self):
    #     self.assertListEqual([0.666666666666667, 0.166666666666667, 0.166666666666667, 0.666666666666667, 0],
    #                          self.c)

    # def test_chi_normal(self):
    #     tabla = Tabla(num_intervalos=10, datos=muestra_1, valor_minimo=0, valor_maximo=1, decimals=2)
    #     tabla.chi_uniforme()
    #     self.assertEqual(1.66666666666667, round(tabla.c_acum, 14))
    #     fo = []
    #     fe = []
    #     print(tabla)
    #     for interv in tabla.intervalos:
    #         fo.append(interv.fo)
    #         fe.append(interv.fe)
    #     print(fo)
    #     self.assertEqual([8, 7, 5, 4, 6], fo)
    #     self.assertEqual([6, 6, 6, 6, 6], fe)
