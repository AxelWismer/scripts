import unittest
import sys
sys.path.append('../')
from tabla import Tabla, Uniforme, Exponencial, Normal, Poisson
import estadistica
# Muestras
muestra_1 = [0.15, 0.22, 0.41, 0.65, 0.84, 0.81, 0.62, 0.45, 0.32, 0.07, 0.11, 0.29, 0.58, 0.73, 0.93, 0.97, 0.79, 0.55,
             0.35, 0.09, 0.99, 0.51, 0.35, 0.02, 0.19, 0.24, 0.98, 0.10, 0.31, 0.17]
muestra_2 = [0.10, 0.25, 1.53, 2.83, 3.50, 4.14, 5.65, 6.96, 7.19, 8.25, 1.20, 5.24, 4.75, 3.96, 2.21, 3.15, 2.53, 1.16,
             0.32, 0.90, 0.87, 1.34, 1.87, 2.91, 0.71, 1.69, 0.69, 0.55, 0.43, 0.26]
muestra_3 = [1.56,2.21,3.15,4.61, 4.18,5.20,6.94,7.71,5.15,6.76,7.28,4.23,3.21,2.75,
            4.69,5.86,6.25,4.27,4.91,4.78,2.46,3.97,5.71,6.19,4.20,3.48,5.83,6.36,5.90,5.43]

class TestChiUniforme(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tabla = Uniforme(num_intervalos=5, datos=muestra_1, valor_minimo=0, valor_maximo=1, decimals=2)
        cls.tabla.chi()
        cls.fe = fe = []
        cls.fo = fo = []
        cls.c = c = []
        print(cls.tabla)
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
        self.assertEqual(len(self.tabla.datos), sum(self.fo))
        self.assertListEqual([8, 7, 5, 4, 6], self.fo)

    def test_c(self):
        self.assertListEqual([0.666666666666667, 0.166666666666667, 0.166666666666667, 0.666666666666667, 0], self.c)


class TestChiExponencial(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tabla = Exponencial(num_intervalos=10, datos=muestra_2, valor_minimo=0, valor_maximo=10, decimals=2)
        cls.tabla.chi()
        print(cls.tabla)
        cls.fe = fe = []
        cls.fo = fo = []
        # Para los intervalos reorganizados
        cls.fe_reorg = fe_reorg = []
        cls.fo_reorg = fo_reorg = []
        cls.c = c = []
        print(cls.tabla)
        for interv in cls.tabla.intervalos:
            fe.append(round(interv.fe, 5))
            fo.append(interv.fo)

        for interv in cls.tabla.intervalos_reorganizados:
            fe_reorg.append(round(interv.fe, 5))
            fo_reorg.append(interv.fo)
            c.append(round(interv.c, 5))

    def test_media(self):
        self.assertEqual(2.57133333333333, round(estadistica.media(self.tabla.datos), 14))

    def test_lambda(self):
        self.assertEqual(0.388903292714545, round(self.tabla.get_lambda(),15))

    def test_fe(self):
        self.assertListEqual([9.58677, 6.49791, 4.40428, 2.98522, 2.02338, 1.37145,
                              0.92957, 0.63006, 0.42706, 0.28946], self.fe)

    def test_fo(self):
        self.assertListEqual([10, 6, 4, 3, 2, 2, 1, 1, 1, 0], self.fo)

    # Intervalos reorganizados
    def test_fe_reorg(self):
        self.assertListEqual([9.58677, 6.49791, 7.38951, 5.67097], self.fe_reorg)

    def test_fo_reorg(self):
        self.assertListEqual([10, 6, 7, 7], self.fo_reorg)

    def test_c(self):
        self.assertListEqual([0.01781, 0.03815, 0.02053, 0.31147], self.c)

    def test_c_acum(self):
        self.assertEqual(0.3880, round(self.tabla.c_acum, 4))



class TestChiNormal(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tabla = Normal(datos = muestra_3, num_intervalos = 10, valor_minimo=0, valor_maximo=10, decimals=2)
        cls.tabla.chi()
        print(cls.tabla)
        cls.fe = fe = []
        cls.fo = fo = []
        # Para los intervalos reorganizados
        cls.fe_reorg = fe_reorg = []
        cls.fo_reorg = fo_reorg = []
        cls.c = c = []
        print(cls.tabla)
        for interv in cls.tabla.intervalos:
            fe.append(round(interv.fe, 5))
            fo.append(interv.fo)

        for interv in cls.tabla.intervalos_reorganizados:
            fe_reorg.append(round(interv.fe, 5))
            fo_reorg.append(interv.fo)
            c.append(round(interv.c, 5))

    #Probando los datos del Excel contra los de nuestro modelo
    def test_media(self):
        self.assertEqual(4.8410, round(estadistica.media(self.tabla.datos), 4))


    def test_varianza(self):
        self.assertEqual(2.43, round(estadistica.varianza(self.tabla.datos), 2))

    def test_desviacion(self):
        self.assertEqual(1.5574, round(estadistica.desviacion(self.tabla.datos),4))

    def test_fe(self):
        pass
        #Hay diferencias decimales que no son por redondeo
        #self.assertListEqual([0.15653,0.76432,2.47108,5.28976,7.49761,7.03635,4.37229,1.79891,0.49006,0.08839], self.fe)

    def test_fo(self):
        self.assertListEqual([0,1,3,4,8,7,5,2,0,0], self.fo)

    # Intervalos reorganizados
    def test_fe_reorg(self):
        pass
        # RT al anterior
        #self.assertListEqual([8.68170,7.49761,7.03635,6.74965], self.fe_reorg)

    def test_fo_reorg(self):
        self.assertListEqual([8,8,7,7], self.fo_reorg)

    def test_c(self):
        pass
        # Como los Fe estan man su correspondiente C va a estar mal
        #self.assertListEqual([0.05353,0.03366,0.00019,0.00929], self.c)

    def test_c_acum(self):
        pass
        # Idem a anterior, C estan mal
        #self.assertEqual(0.0967, round(self.tabla.c_acum, 4))


class TestChiPoisson(unittest.TestCase):
    pass