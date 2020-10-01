from swampy.TurtleWorld import *
import turtle
t = turtle.Turtle ()
import math 
world = TurtleWorld()
bob = Turtle()
bob.delay = 0
# EJERCICIO 4.1
# Inciso a
def polygon(bob, n , l):
    '''Dibuja un poligono regular de n lados para una longitud l dada. \
     Toma de parametros a bob, n, l. '''
    print(bob)
    angle = float(360/n)
    for i in range(0,n):
        fd(bob, l)
        lt(bob, angle)
def arc(bob, theta , radio):
    '''Dibuja un arco para un radio r y angulo theta dados.  \
    Toma de parametros a bob, theta , radio. '''
    print(bob)
    longitud_de_arco = 2 * math.pi * radio * theta / 360
    n = int(longitud_de_arco / 3) + 1
    longitud_de_lado = float ( longitud_de_arco / n )
    angulo = float ( theta / n)
    for i in range(0,n):
        fd (bob, longitud_de_lado)
        lt(bob, angulo)

def circle(bob, radio):
    '''Dibuja un circulo de un radio r dado con una aproximacion de un poligono \
     de 50 lados. '''
    print(bob)
    n = 50
    longitud = float(2 * math.pi * radio / n)
    for i in range(0,n):
        fd (bob, longitud)
        lt(bob, float(360/n))
# Inciso b. Dibujar un diagrama
# EJERCICIO 4.2. Funciones que dibujan flores.
def petalo(bob, theta , radio):
# Dibujar un petalo con dos arcos, angulo es la separacion en grados entre los arcos.
    print(bob)
    for i in range(0,2):
        arc(bob, theta , radio )
        lt(bob, 180 - theta) #para el angulo subtendido por los arcos
def dibujo_de_flor(bob, theta, radio, petalos):
# Dibuja una flor con petalos dados por theta y radio.
    for i in range(0,petalos) :
        petalo(bob, theta, radio)
        lt(bob, float(360/petalos)) #para empezar a formar el otro petalo

#Ejecutar una por una desactivando el comentario
#Para flor 1
#dibujo_de_flor(bob, 60, 60 , 7)
#Para flor 2
#dibujo_de_flor(bob, 120, 60, 10)
# Para flor 3
#dibujo_de_flor(bob, 20 , 140 , 20)

#EJERCICIO 4.3
def dibujar_pie(bob, n , l):
    angulo_lateral = float(90 - 180/n) #angulo de los angulos iguales
    angulo_central = float(360/n) #angulo diferente del triangulo isosceles
    semi_angulo = angulo_central / 2 #angulo que forma con la altura
    lateral = float(( l / 2)  * (1/math.sin(math.radians(semi_angulo)))) #medida del lateral del triangulo
    polygon(bob, n, l)
    for i in range(0,n):
        lt(bob, angulo_lateral)
        fd(bob, lateral )
        rt(bob, 180 - angulo_central)
        fd(bob, lateral)
        lt(bob, 180 - angulo_lateral)

#dibujar_pie(bob, 5, 100)
#dibujar_pie(bob, 6, 100)
#dibujar_pie(bob, 7, 100)

#EJERCICIO 4.4
# Diseño de una fuente
def dibujar_a(bob, n):
    lt(bob, 90)
    circle(bob, n)
    fd(bob, n )
    lt(bob, 180)
    fd(bob, 2 * n)
#dibujar_a(bob, 80)
def dibujar_b(bob, n):
    rt(bob, 90)
    circle(bob, n)
    bk(bob, n)
    fd(bob, 180)
    bk(bob, 3 * n)
#dibujar_b(bob, 80)
def dibujar_c(bob, n):
    lt(bob, 115)
    arc(bob, 300, n)
#dibujar_c(bob, 80)
def dibujar_d(bob, n):
    lt(bob, 90)
    circle(bob, n)
    fd(bob, 2 * n)
    lt(bob, 180)
    fd(bob, 3 * n)
#dibujar_d(bob, 80)
def dibujar_e(bob, n):
    fd(bob, 2 * n)
    lt(bob, 90)
    arc(bob, 320, n)
#dibujar_e(bob, 80)
def dibujar_f(bob, n):
    lt(bob, 90)
    arc(bob, 180, n)
    fd(bob, 3 * n)
    lt(bob, 180)
    fd(bob, n)
    rt(bob, 90)
    fd(bob, n)
#dibujar_f(bob, 40)
def dibujar_g(bob, n):
    rt(bob, 90)
    arc(bob, 180, n)
    fd(bob, 4 * n)
    lt(bob, 180)
    fd(bob, n)
    lt(bob, 180)
    circle(bob, n)
#dibujar_g(bob, 20)
def dibujar_h(bob, n):
    lt(bob, 90)
    arc(bob, 180, n)
    lt(bob, 180)
    fd(bob, 4 * n)
#dibujar_h(bob, 30)
def dibujar_i(bob, n):
    lt(bob, 90)
    fd(bob, n)
def dibujar_j(bob, n):
    rt(bob, 90)
    arc(bob, 180, n)
    fd(bob, 3 * n)
#dibujar_j(bob, 50)
def dibujar_k(bob, n):
    rt(bob, 90)
    fd(bob, 3 * n)
    lt(bob, 170)
    fd(bob, 3 * n)
    lt(bob, 180)
    fd(bob,  3 * n / 2)
    lt(bob, 30)
    fd(bob, 3 * n / 2 )
#dibujar_k(bob, 60)
def dibujar_l(bob, n):
    lt(bob, 90)
    fd(bob, n)
#dibujar_l(bob, 80)
def dibujar_m(bob, n):
    lt(bob, 90)
    arc(bob, 180, n)
    lt(bob, 180)
    arc(bob, 180, n)
    lt(bob, 180)
    fd(bob, 5 * n / 4)
#dibujar_m(bob, 40)
def dibujar_n(bob, n):
    lt(bob, 90)
    arc(bob, 180, n)
    lt(bob, 180)
    fd(bob, 5 * n / 4)
#dibujar_n(bob, 50)
def dibujar_o(bob, n):
    circle(bob, n)
#dibujar_o(bob, 40)
def dibujar_p(bob, n):
    rt(bob, 90)
    circle(bob, n)
    lt(bob, 180)
    fd(bob, n)
    lt(bob, 180)
    fd(bob, 3 * n)
#dibujar_p(bob, 40)
def dibujar_q(bob, n):
    lt(bob, 90)
    circle(bob, n)
    lt(bob, 180)
    bk(bob, n / 2)
    lt(bob, 180)
    bk(bob, 3 * n)
#dibujar_q(bob, 50)
def dibujar_r(bob, n):
    lt(bob, 150)
    arc(bob, 120, n)
    fd(bob, n)
    lt(bob, 180)
    fd(bob, 2 * n)
#dibujar_r(bob, 40)
def dibujar_s(bob,n):
    rt(bob, 20)
    arc(bob, 180, n)
    fd(bob, n / 5)
    lt(bob, 180)
    pu(bob)
    arc(bob, 180, n)
    pd(bob)
    arc(bob, 180, n)
#dibujar_s(bob, 50)
def dibujar_t(bob, n):
    fd(bob, n)
    lt(bob, 180)
    fd(bob, n / 2 )
    lt(bob, 90)
    bk(bob, n / 2)
    lt(bob, 180)
    bk(bob, 3 * n / 2)
#dibujar_t(bob, 50)
def dibujar_u(bob, n):
    rt(bob, 90)
    arc(bob, 180, n)
#dibujar_u(bob, 50)
def dibujar_v(bob, n):
    rt(bob, 60)
    fd(bob, n)
    lt(bob, 120)
    fd(bob, n)
#dibujar_v(bob, 80)
def dibujar_w(bob, n):
    rt(bob, 30)
    for i in range(0,2):
        dibujar_v(bob, n)
#dibujar_w(bob, 50)
def dibujar_x(bob, n):
    rt(bob, 50)
    fd(bob, n)
    lt(bob, 180)
    fd(bob, n/2)
    rt(bob, 90)
    fd(bob, n /2)
    lt(bob, 180)
    fd(bob, n)
#dibujar_x(bob, 60)
def dibujar_y(bob, n):
    dibujar_v(bob, n)
    lt(bob, 180)
    fd(bob, n)
    lt(bob, 32)
    fd(bob, 3 * n / 2)
#dibujar_y(bob, 50)
def dibujar_z(bob, n):
    fd(bob, n)
    rt(bob, 135)
    fd(bob, math.sqrt(2) * n)
    lt(bob, 135)
    fd(bob, n)
#dibujar_z(bob, 50)

#EJERCICIO 4.5
#Dibujar un espiral arquimediano
def dibujar_espiral( vueltas, separacion, radio):
    for i in range(0,vueltas):
        for j in range(1, 360, 4):
            radio = radio + separacion * j/360
            j = j * math.pi/180
            y = radio * math.sin(j)
            x = radio * math.cos(j)
            turtle.goto(x,y)
        radio = radio + separacion
dibujar_espiral(10, 3, 5)
