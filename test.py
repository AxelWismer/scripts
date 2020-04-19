from generador import Generador
from tabla import Tabla, Uniforme, Exponencial, Normal, Poisson


# Uniforme
def prueba_uniforme(random):
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.uniforme(a=0, b=10, n=1000)
    tabla = Uniforme(num_intervalos=10, datos=datos, decimals=4)
    # tabla.chi_uniforme()
    tabla.chi()
    print(tabla)
    tabla.histogram()

# Exponencial
def prueba_exponencial(random):
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.exponencial(lam=10, n=1000)
    print(datos)

    tabla = Exponencial(num_intervalos=10, datos=datos, decimals=4)
    tabla.chi()
    print(tabla)
    tabla.histogram()

# Normal
def prueba_normal(random, box=True):
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.normal(media=0, desviacion=1, n=1000, box=box)
    tabla = Normal(num_intervalos=10, datos=datos, decimals=4)
    tabla.chi()
    print(tabla)
    tabla.histogram()

# Poisson
def prueba_poisson(random):
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.poisson(lam=1, n=1000)
    print(max(datos))
    tabla = Poisson(datos=datos, decimals=4)
    tabla.chi()
    print(tabla)
    tabla.histogram()

random = True
prueba_uniforme(random)
prueba_exponencial(random)
prueba_normal(random)
prueba_normal(random, box=False)
prueba_poisson(random)