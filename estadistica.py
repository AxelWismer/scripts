import math

# Trunca un numero a cierta cantidad de decimales
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

# Funciones estadisticas basicas
def media(v):
    if len(v) == 0:
        return 0
    return sum(v) / len(v)

def varianza(v, med=None):
    if med is None:
        med = media(v)
    if len(v) == 0:
        return 0
    acum = 0
    for num in v:
        acum += (num - med) ** 2
    return acum / len(v)

def desviacion(v, media=None):
    return math.sqrt(varianza(v, media))

def varianza_normal(v):
    med = media(v)
    if len(v) == 0:
        return 0
    acum = 0
    for num in v:
        acum += (num - med) ** 2
    return acum / (len(v) - 1)

def desviacion_normal(v):
    print(varianza_normal(v))
    return math.sqrt(varianza_normal(v))

# Funciones de densidad
def densidad_uniforme(a, b):
    return 1 / b - a

def densidad_exponencial(x, lam):
    return lam * math.exp(-lam * x)

def densidad_normal(x, media, desviacion):
    return (1 / (desviacion * math.sqrt(2 * math.pi))) * math.exp(-0.5 * (((x - media) / desviacion) ** 2))

def densidad_poisson(x, lam):
    return (lam ** x * math.exp(-lam)) / math.factorial(x)

# Funciones acumuladas
def acumulada_uniforme(x, a, b):
    return (x - a) / (b - a)

def acumulada_exponencial(x, lam):
    return 1 - math.exp(-lam * x)