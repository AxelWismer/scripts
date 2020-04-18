import matplotlib.pyplot as plt
import math
import estadistica

class Tabla():
    intervalos = []
    intervalos_reorganizados = []
    c_acum = 0
    valor_minimo = 0
    valor_maximo = 0
    num_intervalos = 0
    datos = []
    v = 0

    class IndivisibleData(Exception):
        pass

    def __init__(self,  datos, num_intervalos=0, valor_minimo=None, valor_maximo=None, decimals=4):
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
        self.generar_intervalos(self.valor_minimo, self.valor_maximo, self.num_intervalos)
        self.conteo_frecuencias()

    def __str__(self):
        r = "Tabla: "
        r += "valor minimo: " + str(self.valor_minimo) + ", valor maximo: " + str(self.valor_maximo) \
            + ", numero de intervalos: " + str(self.num_intervalos) + ", c acumulado: " \
             + str(round(self.c_acum, self.decimals)) + ', v: ' + str(self.v) + '\n'
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
                   ", fe: " + str(round(self.fe, self.decimals)) + ", c:" + str(round(self.c, self.decimals)) + ", c_acum: " + str(round(self.c_acum, self.decimals))

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
        largo_intervalo = (valor_maximo - valor_minimo) / num_intervalos
        self.intervalos = [0] * num_intervalos
        for i in range(num_intervalos):
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

    # Setea el valor fe en todos los intervalos
    def set_fe(self):
        raise Exception("No se puede llamar a este metodo en la clase padre")

    # Devuelve el valor total de fe que deberia ser igual a la cantidad de datos
    def sum_fe(self):
        acum = 0
        for interv in self.intervalos:
            acum += interv.fe
        return acum

    # Calcula el valor de v para ver si se refuta o no la hipotesis
    def set_v(self):
        raise Exception("No se puede llamar a este metodo en la clase padre")

    # Completa la tabla segun el metodo de chi
    def chi(self):
        self.reagrupar_intervalos()
        self.set_c_acum()
        return self.c_acum, self.v

    def reagrupar_intervalos_ascendente(self, intervalos):
        intervalos_new = []
        inicio = 0
        # Se itera por los intervalos
        for i in range(len(intervalos)):
            # Si el elemto actual es mayor que 5 se corta el algoritmo
            if intervalos[inicio].fe >= 5:
                break
            # Acumuladores de las frecuencias esperada y observadas
            fe_acum = fo_acum = 0
            # Si es menor a 5 se itera el resto del vector acumulando la frecuencia
            # esperada hasta que el valor es mayor a 5
            for j in range(inicio, len(intervalos)):
                fe_acum += intervalos[j].fe
                fo_acum += intervalos[j].fo
                if fe_acum >= 5:
                    # Se crea un intervalo que inicia en el primer intervalo y finaliza en el intervalo que cumplio que
                    # fe_acum sea mayor que 5
                    interv = self.Intervalo(intervalos[inicio].inicio, intervalos[j].fin, self.decimals)
                    interv.fe = fe_acum
                    interv.fo = fo_acum
                    intervalos_new.append(interv)
                    # Se setea como inicio el intervalo siguiente al ultimo que incluimos en nuestro
                    # intervalo para repetir el proceso
                    inicio = j + 1
                    # Se termina este ciclo porque ya no se busca mas intervalos para generar este intervalo
                    break
        return intervalos_new, j


    def reagrupar_intervalos_descendente(self, intervalos):
        intervalos_new = []
        inicio = 0
        # Se itera por los intervalos
        for i in range(len(intervalos)):
            # Si el elemto actual es mayor que 5 se corta el algoritmo
            if intervalos[inicio].fe >= 5:
                break
            # Acumuladores de las frecuencias esperada y observadas
            fe_acum = fo_acum = 0
            # Si es menor a 5 se itera el resto del vector acumulando la frecuencia
            # esperada hasta que el valor es mayor a 5
            for j in range(inicio, len(intervalos)):
                fe_acum += intervalos[j].fe
                fo_acum += intervalos[j].fo
                if fe_acum >= 5:
                    # Se crea un intervalo que inicia en el primer intervalo y finaliza en el intervalo que cumplio que
                    # fe_acum sea mayor que 5
                    interv = self.Intervalo(intervalos[j].inicio, intervalos[inicio].fin, self.decimals)
                    interv.fe = fe_acum
                    interv.fo = fo_acum
                    intervalos_new.append(interv)
                    # Se setea como inicio el intervalo siguiente al ultimo que incluimos en nuestro
                    # intervalo para repetir el proceso
                    inicio = j + 1
                    # Se termina este ciclo porque ya no se busca mas intervalos para generar este intervalo
                    break
        return intervalos_new, j

    # Reagrupa los intervalos juntando los intervalos con fe menor a 5 de cada extremo y
    # agrupandolos con los del centro hasta que todos los grupos tengan un fe > 5
    def reagrupar_intervalos(self):
        # Una copia de los intervalos originales
        intervalos = self.intervalos
        # Si el primer valor es menor a 5 recorre la lista en orden
        # ascendente reagrupando los intervalos para que su fe sea mayo a 5
        intervalos_asc = intervalos_desc = []
        inicio_intervalo_original = - 1
        fin_intervalo_original = - 1

        # Calcula los nuevos intervalos de forma ascendente
        if intervalos[0].fe < 5:
            intervalos_asc, inicio_intervalo_original = self.reagrupar_intervalos_ascendente(intervalos)

        # Calcula los nuevos intervalos de forma descendente
        if intervalos[-1].fe < 5:
            # Genera una copia de los intervalos originales y la invierte
            intervalos_reverse = intervalos.copy()
            intervalos_reverse.reverse()
            # Calcula los nuevos intervalos y los invierte dado que la funcion los devuelve en orden inverso
            intervalos_desc, fin_intervalo_original = self.reagrupar_intervalos_descendente(intervalos_reverse)
            intervalos_desc.reverse()

        # Genera la lista uniendo la lista de nuevos intervalos en orden ascendente, los intervalos que no se
        # modeificaron y los nuevos intervalos calculados de forma descendente
        intervalos_asc.extend(intervalos[inicio_intervalo_original + 1: len(self.intervalos) - 1 - fin_intervalo_original])
        intervalos_asc.extend(intervalos_desc)
        self.intervalos_reorganizados = intervalos_asc

    # Genera los datos para simular la frecuencia esperada
    def datos_esperados(self):
        frec_esperada = []
        # genera fe numeros en cada intervalo para simular la frecuencia esperada
        for intervalo in self.intervalos:
            frec_esperada.extend([round(intervalo.x, self.decimals)] * int(estadistica.truncate(intervalo.fe, 0)))
        return frec_esperada

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
            frec_esperada = self.datos_esperados()
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

class Uniforme(Tabla):
    def __init__(self, datos, num_intervalos, valor_minimo=None, valor_maximo=None, decimals=4):
        super(Uniforme, self).__init__(datos, num_intervalos, valor_minimo, valor_maximo, decimals)
        # Setea los valores de la fe en la subclase donde se re define el metodo set_fe()
        self.set_fe()
        # Setea el valor v para el calculo de chi
        self.v = self.num_intervalos

    def __str__(self):
        return "Distribucion Uniforme\n" + super(Uniforme, self).__str__()

    def set_fe(self):
        fe = int(len(self.datos) / len(self.intervalos))
        for interv in self.intervalos:
            interv.fe = fe

    def chi(self):
        self.set_c_acum()
        return self.c_acum, self.v

class Exponencial(Tabla):
    def __init__(self, datos, num_intervalos, valor_minimo=None, valor_maximo=None, decimals=4):
        super(Exponencial, self).__init__(datos, num_intervalos, valor_minimo, valor_maximo, decimals)
        # Setea los valores de la fe en la subclase donde se re define el metodo set_fe()
        self.set_fe()
        # Setea el valor v para el calculo de chi
        self.v = self.num_intervalos - 1

    def __str__(self):
        return "Distribucion Exponencial\n" + super(Exponencial, self).__str__()

    def set_fe(self):
        lam = self.get_lambda()
        for interv in self.intervalos:
            # Calcula el area dada por la diferencia de las frecuencias acumuladas
            # y lo multiplica por la cantidad de datos
            interv.fe = len(self.datos) * \
                        (estadistica.acumulada_exponencial(interv.fin, lam)
                         - estadistica.acumulada_exponencial(interv.inicio, lam))

    def get_lambda(self):
        return 1 / estadistica.media(self.datos)

class Normal(Tabla):
    def __init__(self, datos, num_intervalos, valor_minimo=None, valor_maximo=None, decimals=4):
        super(Normal, self).__init__(datos, num_intervalos, valor_minimo, valor_maximo, decimals)
        # Setea los valores de la fe en la subclase donde se re define el metodo set_fe()
        self.set_fe()
        # Setea el valor v para el calculo de chi
        self.v = self.num_intervalos - 2

    def __str__(self):
        return "Distribucion Normal\n" + super(Normal, self).__str__()

    def set_fe(self):
        for interv in self.intervalos:
            # Calcula la densidad normal y lo multiplica por  el largo del intervalo para obtener el area aproximada
            # y lo multiplica por la cantidad de datos para que sea proporcional
            interv.fe = estadistica.densidad_normal(interv.x, media=self.get_media(), desviacion=self.get_desviacion()) \
                        * (interv.fin - interv.inicio) * len(self.datos)

    def get_media(self):
        return estadistica.media(self.datos)

    def get_desviacion(self):
        return estadistica.desviacion(self.datos)


class Poisson(Tabla):
    def __init__(self, datos, decimals=4):
        self.datos = datos
        self.num_intervalos = max(datos) + 1
        self.decimals = decimals
        self.generar_intervalos()
        self.conteo_frecuencias()
        # Setea los valores de la fe en la subclase donde se re define el metodo set_fe()
        self.set_fe()
        # Setea el valor v para el calculo de chi
        self.v = self.num_intervalos - 1

    def __str__(self):
        r = "Distribucion Poisson\n"
        r += "Tabla: "
        r +=  ", numero de intervalos: " + str(self.num_intervalos) + ", c acumulado: " \
              + str(round(self.c_acum, self.decimals)) + '\n'
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

    def set_fe(self):
        for interv in self.intervalos:
            # Calcula la densidad de poisson y lo multiplica por la cantidad de datos
            interv.fe = estadistica.densidad_poisson(int(interv.inicio), lam=self.get_lambda()) * len(self.datos)

    def get_lambda(self):
        return estadistica.media(self.datos)

    def generar_intervalos(self):
        # Para poisson genera tantos intervalos como valores distintos posibles existan
        self.intervalos = [0] * self.num_intervalos
        for i in range(self.num_intervalos):
            self.intervalos[i] = self.Intervalo(inicio=i, fin=i+1, decimals=self.decimals)

    def datos_esperados(self):
        frec_esperada = []
        # genera fe numeros en cada intervalo para simular la frecuencia esperada
        for intervalo in self.intervalos:
            frec_esperada.extend([intervalo.inicio] * int(round(intervalo.fe, 0)))
        return frec_esperada