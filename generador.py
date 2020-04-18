import math
import estadistica
import random


class Generador():
    box_muller_rnd = False
    x = 0
    c = 0
    a = 0
    k = 0
    m = 0
    g = 0

    def __init__(self, x=0, c=0, a=0, k=0, m=0, g=0, decimals=4, random=False):
        self.x = x
        self.c = c
        self.k = k
        self.g = g
        self.random = random
        self.decimals = decimals
        # Se define o calcula el valor de a con k
        if a:
            self.a = a
        elif k:
            # Metodo multiplicativo
            if c == 0:
                # Se verifica que k sea impar
                if k % 2 == 0:
                    k += 1
                self.a = 3 + 8 * k
            # Metodo mixto
            else:
                self.a = 1 + 4 * k
        else:
            self.a = 0
        # Se define o calcula el valor de m
        if m:
            self.m = m
        elif g:
            self.m = 2 ** g
        else:
            self.m = 0

    def __str__(self):
        return "x: " + str(self.x) + " c: " + str(self.c) + " a: " + str(self.a) + " m: " + str(self.m) + " k: " + str(
            self.k) + " g: " + str(self.g)

    # Trunca un valor a cierta cantidad de decimales
    def truncate(self, number, digits=False) -> float:
        if not digits:
            digits = self.decimals
        return estadistica.truncate(number, digits)

    # Devuelve un valor aleatorio entre 0 y 1
    def rnd(self) -> float:
        if self.random:
            return random.random()
        # Se calcula y guarda el proximo valor de x
        self.x = (self.a * self.x + self.c) % self.m
        # Se calcula el numero aleatoreo y se lo trunca
        return self.x / self.m

    def uniforme_next(self, a=0, b=1) -> float:
        return self.truncate(a + self.rnd() * (b - a))

    # La distribucion es por defecto uniforme 0, 1
    def uniforme(self, a=0, b=1, n = 1) -> float or list[float]:
        # Si se pide un solo elemento se devuelve el valor como float
        if n == 1:
            return self.uniforme_next(a, b)
        # Para mas de un numero se devuelve una lista de valores
        v = [0] * n
        for i in range(n):
            v[i] = self.uniforme_next(a, b)
        return v

    def exponencial_next(self, lam=0, media=0) -> float:
        return self.truncate((-1 / lam) * math.log(1 - self.rnd()))

    # "lam" es la variable lambda y "u la media"
    def exponencial(self, lam=0, media=0, n=1) -> float or list[float]:
        # Si no se provee un valor de lambda se lo calcula con la media
        if lam == 0:
            if media != 0:
                lam = 1 / media
            else:
                lam = 1
        # Si se pide un solo elemento se devuelve el valor como float
        if n == 1:
            return self.exponencial_next(lam, media)
        # Para mas de un numero se devuelve una lista de valores
        v = [0] * n
        for i in range(n):
            v[i] = self.exponencial_next(lam, media)
        return v

    def box_muller_next(self, media=0.0, desviacion=1.0):
        # Identifica si existe un valor de una llamada anterior
        if self.box_muller_rnd:
            # Si existe lo devuelve y setea el valor como vacio (false)
            rnd = self.box_muller_rnd
            self.box_muller_rnd = False
            return rnd
        else:
            # Si no existe el valor calcula los 2 valores del metodo guardando el segundo
            # genera 2 numeros aleatoreos entre a 0 y menores a 1 excluyendo al 0 para
            # evitar errores en la funcion logarimo
            # Calcula el valor minimo segun la cantidad de decimales
            a = 1 / self.decimals
            # calcula el intervalo con la funcion uniforme para poder cambiar el valor minimo
            rnd1, rnd2 = self.rnd(), self.rnd()
            if rnd1 == 0: rnd1 += a
            if rnd2 == 0: rnd2 += a


            # calcula los 2 valores del metodo
            n1 = self.truncate((math.sqrt(-2 * math.log(rnd1)) * math.cos(2 * math.pi * rnd2)) * desviacion + media)
            n2 = self.truncate((math.sqrt(-2 * math.log(rnd1)) * math.sin(2 * math.pi * rnd2)) * desviacion + media)
            # Guarda el valor que no se pidio para esta vuelta para un proximo uso
            self.box_muller_rnd = n2
            # Devuelve el valor pedido
            return n1

    def box_muller(self, media=0.0, desviacion=1.0, n=1):
        # Si se pide un solo elemento se devuelve el valor como float
        if n == 1:
            return self.box_muller_next(media, desviacion)
        # Para mas de un numero se devuelve una lista de valores
        v = [0] * n
        for i in range(n):
            v[i] = self.box_muller_next(media, desviacion)
        return v

    def convolucion_next(self, media, desviacion):
        rnds = self.uniforme(n = 12)
        return self.truncate((sum(rnds) - 6) * desviacion + media)

    def convolucion(self, media=0.0, desviacion=1.0, n=1):
        # Si se pide un solo elemento se devuelve el valor como float
        if n == 1:
            return self.convolucion_next(media, desviacion)
        # Para mas de un numero se devuelve una lista de valores
        v = [0] * n
        for i in range(n):
            v[i] = self.convolucion_next(media, desviacion)
        return v

    # Genera una distribucion normal permitiendo elegir el metodo
    def normal(self, media=0.0, desviacion=1.0, n=1, box=True):
        if box:
            return self.box_muller(media, desviacion, n)
        else:
            return self.convolucion(media, desviacion, n)

    def poisson_next(self, lam):
        p = 1
        x = -1
        a = math.exp(-lam)
        u = self.rnd()
        p = p * u
        x = x + 1
        while (p >= a):
            u = self.rnd()
            p = p * u
            x = x + 1
        return x

    def poisson(self, lam, n=1):
        # Si se pide un solo elemento se devuelve el valor como float
        if n == 1:
            return self.poisson_next(lam)
        # Para mas de un numero se devuelve una lista de valores
        v = [0] * n
        for i in range(n):
            v[i] = self.poisson_next(lam)
        return v