import math
import matplotlib.pyplot as plt
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
        self.x = (self.a + self.x + self.m) % self.m
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


class Tabla():
    intervalos = []
    intervalos_reorganizados = []
    c_acum = 0
    valor_minimo = 0
    valor_maximo = 0
    num_intervalos = 0
    datos = []

    class IndivisibleData(Exception):
        pass

    def __init__(self,  datos, num_intervalos=0, valor_minimo=None, valor_maximo=None, decimals=4, poisson=False):
        if len(datos) % num_intervalos != 0:
            raise self.IndivisibleData('La cantidad de datos debe ser divisible por el numero de intervalos')
        # Completar datos
        # Si no se dan los valores minimos y maximos se obtienen directamente de los datos
        if valor_minimo is not None:
            self.valor_minimo = valor_minimo
        else:
            self.valor_minimo = min(datos)
        if valor_maximo is not None:
            self.valor_maximo = valor_maximo
        else:
            self.valor_maximo = max(datos)

        self.num_intervalos = num_intervalos
        self.datos = datos
        self.decimals = decimals
        # Generar y completar la tabla
        if poisson:
            # Para poisson genera tantos intervalos como valores distintos posibles existan
            self.num_intervalos = num_intervalos
            self.generar_intervalos(self.valor_minimo, self.valor_maximo, max(datos), poisson=True)
        else:
            self.generar_intervalos(self.valor_minimo, self.valor_maximo, self.num_intervalos)
        self.conteo_frecuencias()

    def __str__(self):
        r = "Tabla: "
        r += "valor minimo: " + str(self.valor_minimo) + ", valor maximo: " + str(self.valor_maximo) \
            + ", numero de intervalos: " + str(self.num_intervalos) + ", c acumulado: " + str(self.c_acum) + '\n'
        r += "Intervalos:\n"
        # Muesta todos los intervalos
        for intervalo in self.intervalos:
            r += '\t' + str(intervalo) + '\n'

        # Si existen muestran los intervalos reorganizados
        if len(self.intervalos_reorganizados) > 0:
            r += "Intervalos reorganizados:\n"
            for intervalo in self.intervalos_reorganizados:
                r += '\t' + str(intervalo) + '\n'
        return r

    # Trunca un valor a cierta cantidad de decimales
    def truncate(self, number, digits=False) -> float:
        if not digits:
            digits = self.decimals
        return estadistica.truncate(number, digits)


    # Clase que representa cada fila de la tabla con sus atributos
    class Intervalo():
        inicio = 0
        fin = 0
        fo = 0
        fe = 0
        c_acum = 0
        decimals = 0

        def __init__(self, inicio, fin, decimals=4):
            self.inicio = inicio
            self.fin = fin
            self.decimals = decimals

        def __str__(self):
            return "inicio: " + str(self.inicio) + ", fin: " + str(self.fin) + ", fo: " + str(self.fo) + \
                   ", fe: " + str(self.fe) + ", c:" + str(round(self.c, self.decimals)) + ", c_acum: " + str(round(self.c_acum, self.decimals))

        @property
        def c(self):
            if self.fe == 0:
                return 0
            return (self.fe - self.fo) ** 2 / self.fe

        # Valor que se utiliza en las funciones de densidad y acumulada
        @property
        def x(self):
            return estadistica.media([self.inicio, self.fin])

        def add_number(self, num):
            if self.inicio <= num <= self.fin:
                self.fo += 1
                return True
            return False


    # Genera los intervalos con su rango
    def generar_intervalos(self, valor_minimo, valor_maximo, num_intervalos, poisson=False):
        # Rango de valores que podran tomar los datos
        rango_valores = valor_maximo - valor_minimo
        # Rango de valores de un intervalo
        largo_intervalo = rango_valores / num_intervalos
        self.intervalos = [0] * num_intervalos
        for i in range(num_intervalos):
            # Crea el intervalo
            if poisson:
                # Para el caso de poisson no existe un intervalo al ser numeros enteros por lo que
                # cada intervalo representa un valor empezando desde 0
                self.intervalos[i] = self.Intervalo(inicio=i, fin=i + 1 , decimals=self.decimals)
            else:
                # Calcula y setea el valor de inicio y fin del rango de valores posibles
                inicio = self.truncate(i * largo_intervalo + valor_minimo)
                fin = self.truncate((i + 1) * largo_intervalo + valor_minimo - 1 / (10 ** self.decimals))
                self.intervalos[i] = self.Intervalo(inicio, fin, self.decimals)


    # Realiza el conteo de la frecuencia observada a partir de un conjunto de datos
    def conteo_frecuencias(self):
        for dato in self.datos:
            for intervalo in self.intervalos:
                if intervalo.add_number(dato):
                    break

    # Setea el valor de c acumuliadp de la tabla y de cada intervalo
    def set_c_acum(self):
        c_acum = 0
        # Si existen calcula c acumulado sobre los intervalos reorganizados
        if len(self.intervalos_reorganizados) > 0:
            intervalos = self.intervalos_reorganizados
        else:
            intervalos = self.intervalos
        for i in range(len(intervalos)):
            c_acum = c_acum + intervalos[i].c
            intervalos[i].c_acum = c_acum
        self.c_acum = c_acum

    # Setea la frecuencia esperada para una distribucion uniforme
    def fe_uniforme(self):
        fe = int(len(self.datos) / len(self.intervalos))
        for interv in self.intervalos:
            interv.fe = fe

    def fe_exponencial(self, lam):
        for interv in self.intervalos:
            # Calcula el area dada por la diferencia de las frecuencias acumuladas
            # y lo multiplica por la cantidad de datos
            interv.fe = self.truncate(len(self.datos) * \
                        (estadistica.acumulada_exponencial(interv.fin, lam)
                         - estadistica.acumulada_exponencial(interv.inicio, lam)))

    def fe_normal(self, media, desviacion):
        for interv in self.intervalos:
            # Calcula la densidad normal y lo multiplica por  el largo del intervalo para obtener el area aproximada
            # y lo multiplica por la cantidad de datos para que sea proporcional
            interv.fe = estadistica.densidad_normal(interv.x, media, desviacion) * (interv.fin - interv.inicio) * len(self.datos)

    def fe_poisson(self, lam):
        for interv in self.intervalos:
            # Calcula la densidad de poisson y lo multiplica por  el largo del intervalo
            interv.fe = estadistica.densidad_poisson(int(interv.inicio), lam) * (interv.fin - interv.inicio) * len(self.datos)

    # Devuelve el valor total de fe que deberia ser igual a la cantidad de datos
    def sum_fe(self):
        acum = 0
        for interv in self.intervalos:
            acum += interv.fe
        return acum

    # Completa la tabla segun el metodo de chi para una variable uniforme
    def chi_uniforme(self):
        self.fe_uniforme()
        self.set_c_acum()

    # Completa la tabla segun el metodo de chi para una variable exponencial
    def chi_exponencial(self, lam=None):
        # Se calcula lambda si no se provee
        if lam is None:
            lam = 1 / estadistica.media(self.datos)
        self.fe_exponencial(lam)
        self.reagrupar_intervalos()
        self.set_c_acum()

    # Completa la tabla segun el metodo de chi para una variable normal
    def chi_normal(self, media=None, desviacion=None):
        if media is None:
            media = estadistica.media(self.datos)
        if desviacion is None:
            desviacion = estadistica.desviacion_normal(self.datos)
        self.fe_normal(media, desviacion)
        self.reagrupar_intervalos()
        self.set_c_acum()

    # Completa la tabla segun el metodo de chi para una variable poisson
    def chi_poisson(self, lam=None):
        if lam is None:
            lam = estadistica.media(self.datos)
        self.fe_poisson(lam)
        self.reagrupar_intervalos()
        self.set_c_acum()

    def reagrupar_intervalos_ascendente(self, intervalos):
        intervalos_new = []
        # Acumuladores de las frecuencias esperada y observadas
        fe_acum = fo_acum = 0
        for i in range(len(intervalos)):
            if intervalos[i].fe >= 5:
                break
            for j in range(i, len(intervalos)):
                fe_acum += intervalos[j].fe
                fo_acum += intervalos[j].fo
                if fe_acum >= 5:
                    interv = self.Intervalo(intervalos[i].inicio, intervalos[j].fin, self.decimals)
                    interv.fe = fe_acum
                    interv.fo = fo_acum
                    intervalos_new.append(interv)
                    i = j
                    break
        return intervalos_new, j

    def reagrupar_intervalos_descendente(self, intervalos):
        intervalos_new = []
        # Acumuladores de las frecuencias esperada y observadas
        fe_acum = fo_acum = 0
        for i in range(len(intervalos)):
            if intervalos[i].fe >= 5:
                break
            for j in range(i, len(intervalos)):
                fe_acum += intervalos[j].fe
                fo_acum += intervalos[j].fo
                if fe_acum >= 5:
                    interv = self.Intervalo(intervalos[j].inicio, intervalos[i].fin, self.decimals)
                    interv.fe = fe_acum
                    interv.fo = fo_acum
                    intervalos_new.append(interv)
                    i = j
                    break
        return intervalos_new, j

    # Reagrupa los intervalos juntando los intervalos con fe menor a 5 de cada extremo y
    # agrupandolos con los del centro hasta que todos los grupos tengan un fe > 5
    def reagrupar_intervalos(self):
        # Una copia de los intervalos originales
        intervalos = self.intervalos.copy()
        # Si el primer valor es menor a 5 recorre la lista en orden
        # ascendente reagrupando los intervalos para que su fe sea mayo a 5
        intervalos_asc = intervalos_desc = []
        inicio_intervalo_original = - 1
        fin_intervalo_original = 1
        if intervalos[0].fe < 5:
            intervalos_asc, inicio_intervalo_original = self.reagrupar_intervalos_ascendente(intervalos)
        if intervalos[-1].fe < 5:
            intervalos_reverse = intervalos.copy()
            intervalos_reverse.reverse()
            intervalos_desc, fin_intervalo_original = self.reagrupar_intervalos_descendente(intervalos_reverse)
            intervalos_desc.reverse()

        intervalos_asc.extend(intervalos[inicio_intervalo_original + 1: len(self.intervalos) - 1 - fin_intervalo_original])
        intervalos_asc.extend(intervalos_desc)
        self.intervalos_reorganizados = intervalos_asc

    # Genera el grafico a partir de los datos de la tabla permitiendo mostrar la frecuencia esperada
    def histogram(self, fe=True, reorganizado=False):
        # Defino si mostrar los intervalos originales o reorganizados
        if reorganizado:
            intervalos = self.intervalos_reorganizados
        else:
            intervalos = self.intervalos

        # Genero los vectores con las frecuencias observadas y esperadas de la tabla
        plt.xlabel('rango')
        plt.ylabel('cant. apariciones')
        plt.title('Conteo de frecuecias')

        if fe:
            frec_esperada = []
            # genera fe numeros en cada intervalo para simular la frecuencia esperada
            for intervalo in self.intervalos:
                frec_esperada.extend([round(intervalo.x, self.decimals) ] * int(estadistica.truncate(intervalo.fe, 0)))

            # Genera el grafico pasandole los datos y los intervalos
            plt.hist([self.datos, frec_esperada], bins=len(intervalos), rwidth=0.9,
                     label=['frecuencia observada', 'frecuencia esperada'])
        else:
            plt.hist(self.datos, bins=self.num_intervalos, rwidth=0.9,
                     label='frecuencia observada')
        # Muestra las labels
        plt.legend()
        # Guarda la figura como un archivo png
        # plt.savefig('media/histograma.png')
        # Elimina la figura
        plt.show()
        plt.close()



