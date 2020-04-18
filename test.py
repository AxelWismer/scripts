from generadores import Generador, Tabla

# Uniforme
def prueba_uniforme(random):
    print("Distribucion uniforme")
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.uniforme(a=0, b=10, n=1000)
    tabla = Tabla(num_intervalos=10, datos=datos, decimals=4)
    tabla.chi_uniforme()
    print(tabla)
    tabla.histogram()

# Exponencial
def prueba_exponencial(random):
    print("Distribucion exponencial")
    gen = Generador(x=12, c=40, k=27, g=2, decimals=4, random=random)
    datos = gen.exponencial(lam=10, n=1000)
    tabla = Tabla(num_intervalos=10, datos=datos, decimals=4)
    tabla.chi_exponencial()
    print(tabla)
    tabla.histogram()

# Normal
def prueba_normal(random, box=True):
    print("Distribucion normal")
    gen = Generador(x=12, c=40, k=27, g=10, decimals=4, random=random)
    datos = gen.normal(media=0, desviacion=1, n=1000, box=box)
    tabla = Tabla(num_intervalos=10, datos=datos, decimals=4)
    tabla.chi_normal()
    print(tabla)
    tabla.histogram()

# Poisson
def prueba_poisson(random):
    print("Distribucion poisson")
    gen = Generador(x=12, c=40, k=27, g=10, decimals=4, random=random)
    datos = gen.poisson(lam=2, n=1000)
    tabla = Tabla(num_intervalos=20, datos=datos, decimals=4, poisson=True)
    tabla.chi_poisson()
    print(tabla)
    tabla.histogram()

random = True
prueba_uniforme(random)
prueba_exponencial(random)
prueba_normal(random)
prueba_normal(random, box=False)
prueba_poisson(random)