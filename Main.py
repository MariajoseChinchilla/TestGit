import matplotlib as mlp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation
from matplotlib.widgets import Button
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from datetime import datetime
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import webbrowser
import numpy as np
import random
import time


class JuegoDeLaVida(Gtk.Window):
    cuenta = 0
    def __init__(self):
        super(JuegoDeLaVida, self).__init__(title='Juego de la vida')
    #Cuestiones basicas para la ventana y los contenedores
        self.set_default_size(800, 600)
        self.set_resizable(False)  # fijar el tamaño de la ventana
        vbox = Gtk.VBox()
        self.add(vbox)
        grid = Gtk.Grid()
        grid.set_row_spacing(2)
        grid.set_column_spacing(2)
        vbox.pack_start(grid, True, True, 0)
        self.pause = True
        self.now = datetime.now()


    #Menu y todos sus items
        menubar = Gtk.MenuBar()  # barra de menu

        # elementos en el menu
        archivo = Gtk.MenuItem('Archivo')
        config = Gtk.MenuItem('Configuración')
        ayuda = Gtk.MenuItem('Ayuda')

        # SUBMENU DE LA OPCION ARCHIVO
        arch_menu = Gtk.Menu()
        config_inicial = Gtk.MenuItem('Cargar configuración inicial')
        arch_menu.append(config_inicial)
        guardar = Gtk.MenuItem('Guardar estado de simulación')
        arch_menu.append(guardar)
        generar = Gtk.MenuItem('Generar configuración aleatoria')
        arch_menu.append(generar)
        archivo.set_submenu(arch_menu)

        # ACCIONES DE LOS ITEMS DE ARCHIVO PARA PANTALLAS CORRESPONDIENTES SEGUN BOTON
        config_inicial.connect('activate', self.cargar_config_inicial)
        guardar.connect('activate', self.guardar_estado)
        generar.connect('activate', self.generar_jugar_aleatorio)

        # SUBMENU DE AYUDA
        ayuda_menu = Gtk.Menu()
        acerca_de = Gtk.MenuItem('Acerca de')
        cod_fuente = Gtk.MenuItem('Código fuente GitHub')
        ayuda_menu.append(acerca_de)
        ayuda_menu.append(cod_fuente)
        ayuda.set_submenu(ayuda_menu)

        # ACCIONES DE MENU DE AYUDA
        acerca_de.connect('activate', self.acerca_de)
        cod_fuente.connect('activate', self.codigo_fuente)

        # agregar las opciones al menu
        menubar.append(archivo)
        menubar.append(ayuda)
        grid.attach(menubar, 0,0, 5, 1)

        #tiempo = Gtk.SpinButton()
        #self.TimeFrame = tiempo.get_value_as_int()
        self.TimeFrame = 0.3

#el submenu de configuracion aparece siempre y no esta en la barra de menu para facilidad de modificacion de
        #las configuraciones

#Radio button para que el usuario deje seleccionado un tipo de frontera

        tipos_de_frontera = Gtk.Label('Tipo de frontera para el juego')
        grid.attach(tipos_de_frontera, 1, 1, 1, 3)
        radio_boton_normales = Gtk.RadioButton.new_with_label_from_widget(None, 'Fronteras normales')
        radio_boton_normales.connect('toggled', self.elegido_normal)
        grid.attach_next_to(radio_boton_normales, tipos_de_frontera, Gtk.PositionType.BOTTOM, 1, 1)

        radio_boton_toroidales = Gtk.RadioButton.new_from_widget(radio_boton_normales)
        radio_boton_toroidales.set_label('Fronteras toroidales')
        radio_boton_toroidales.connect('toggled', self.elegido_toroidal)
        grid.attach_next_to(radio_boton_toroidales, radio_boton_normales, Gtk.PositionType.RIGHT, 1, 1)

        segundos_label = Gtk.Label('Segundos de espera entre turnos')
        grid.attach(segundos_label, 24, 1, 1, 3)
        segundos = Gtk.SpinButton()
        segundos.set_digits(2)
        ajuste = Gtk.Adjustment(lower=0.00001, upper=5, step_increment=0.01, page_increment=0.01)
        segundos.set_adjustment(ajuste)
        grid.attach_next_to(segundos, segundos_label, Gtk.PositionType.BOTTOM, 1, 1)

#botones de pausar/jugar y el de tomar captura de pantalla
        pausa_jugar_boton = Gtk.Button('Jugar/Pausar')
        pausa_jugar_boton.connect('clicked', self.play_pause)
        grid.attach(pausa_jugar_boton, 24, 200, 1, 1)
        captura_boton = Gtk.Button('Captura de pantalla')
        captura_boton.connect('clicked', self.captura_de_pantalla)
        grid.attach_next_to(captura_boton, pausa_jugar_boton, Gtk.PositionType.BOTTOM, 2, 2)

    #metodos para cada boton

    def cargar_config_inicial(self, widget):        #abre el dialogo para elegir un archivo a cargar
        dialogo = Gtk.FileChooserDialog('Select a File', None, Gtk.FileChooserAction.OPEN,
                                       ('Cancelar', Gtk.ResponseType.CANCEL, 'Seleccionar', Gtk.ResponseType.OK))
        respuesta = dialogo.run()
        if respuesta == Gtk.ResponseType.OK:
            # Lectura del archivo .pm2
            file = open(dialogo.get_filename(), 'r')
            global N
            N = int(file.readline())
            linea = [line.split() for line in file]
            global tablero
            tablero = np.zeros((N, N))
            for j in range(len(linea)):
                for i in range(len(linea)):
                    tablero[j, i] = eval(linea[j][i])
            dialogo.close()
            self.normales_cargado(tablero)
        elif respuesta == Gtk.ResponseType.CANCEL:
            pass
        dialogo.destroy()

    def guardar_estado(self, widget):
        pass

    def generar_jugar_aleatorio(self, widget):  #genera aleatoriamente un tablero con juego
        global N
        N = random.randint(3, 250)      #elige al azar una dimension para la cuadricula del juego
        global tablero
        tablero = np.zeros((N, N))

        for y in range(N):
            for x in range(N):
                tablero[y, x] = random.randint(0, 1)

# funciones para cargar un archivo inicial y poner pausa y demas

    def play_pause(self, widget):
        self.pause ^= True      #esto va a servir como un interruptor para normal_cargado funcion

    def captura_de_pantalla(click):
        print('captura boton')

# para evaluar que debe pasar con una celula, evaluar a sus 8 vecinas
#considerar "mover" las celulas en las 8 direcciones. Por cada movimiento, sumar el
#valor de la celula en esa posicion. El valor final que tome cada celula luego de los 8
#movimientos es el numero de celulas vecinas vivas.
    def normales_cargado(self, tablero):

        def conteo_normales(tablero):
            global vecindario
            vecindario = np.zeros((len(tablero), len(tablero)), dtype = int)
            for j in range(1, len(tablero) - 1):
                for i in range(1, len(tablero) - 1):
                    vecindario[j, i] = (
                            tablero[j + 1, i - 1] +  # Abajo - Izquierda
                            tablero[j + 1, i] +  # Abajo
                            tablero[j + 1, i + 1] +  # Abajo - Derecha
                            tablero[j, i + 1] +  # Derecha
                            tablero[j - 1, i + 1] +  # Arriba - Derecha
                            tablero[j - 1, i] +  # Arriba
                            tablero[j - 1, i - 1] +  # Arriba - Izquierda
                            tablero[j, i - 1]  # Izquierda
                    )
            for i in range(1, len(tablero) - 1):
                    vecindario[0, i] = (
                            tablero[0, i - 1] +  # Izquierda
                            tablero[1, i - 1] +  # Abajo - Izquierda
                            tablero[1, i] +  # Abajo
                            tablero[1, i + 1] +  # Abajo - Derecha
                            tablero[0, i + 1]  # Derecha
                    )
            for i in range(1, len(tablero) - 1):
                    vecindario[N - 1, i] = (
                            tablero[N - 1, i - 1] +  # Izquierda
                            tablero[N - 2, i - 1] +  # Arriba - Izquierda
                            tablero[N - 2, i] +  # Arriba
                            tablero[N - 2, i + 1] +  # Arriba - Derecha
                            tablero[N - 1, i + 1]  # Derecha
                    )
            for j in range(1, len(tablero) - 1):
                    vecindario[j, 0] = (
                            tablero[j - 1, 0] +  # Arriba
                            tablero[j - 1, 1] +  # Arriba - Derecha
                            tablero[j, 1] +  # Derecha
                            tablero[j + 1, 1] +  # Abajo - Derecha
                            tablero[j + 1, 0]  # Abajo
                    )
            for j in range(1, len(tablero) - 1):
                    vecindario[j, 0] = (
                            tablero[j - 1, N - 1] +  # Arriba
                            tablero[j - 1, N - 2] +  # Arriba - Izquierda
                            tablero[j, N - 2] +  # Izquierda
                            tablero[j + 1, N - 2] +  # Abajo - Izquierda
                            tablero[j + 1, N - 1]  # Abajo
                    )
            vecindario[0, 0] = (
                    tablero[0, 1] +  # Derecha
                    tablero[1, 1] +  # Abajo - Derecha
                    tablero[1, 0]  # Abajo
            )
            vecindario[0, N - 1] = (
                    tablero[0, N - 2] +  # Izquierda
                    tablero[1, N - 2] +  # Abajo - Izquierda
                    tablero[1, N - 1]  # Abajo
            )
            vecindario[N - 1, 0] = (
                    tablero[N - 2, 0] +  # Arriba
                    tablero[N - 2, 1] +  # Arriba - Derecha
                    tablero[N - 1, 1]  # Derecha
            )
            vecindario[N - 1, N - 1] = (
                    tablero[N - 2, N - 1] +  # Arriba
                    tablero[N - 2, N - 2] +  # Arriba - Izquierda
                    tablero[N - 1, N - 2]  # Izquierda
            )
            return vecindario

        def paso(tablero):
        # evaluacion de que pasara con la celula dependiendo de las reglas del juego
            v = conteo_normales(tablero)
            nuevo_tablero = tablero.copy()
            clase = JuegoDeLaVida
            contador = clase.cuenta
            for i in range(nuevo_tablero.shape[0]):
                for j in range(nuevo_tablero.shape[1]):
                    if v[i, j] == 3 or (v[i, j] == 2 and tablero[i, j]):
                        nuevo_tablero[i, j] = 1
                        contador = contador + 1
                    else:
                        nuevo_tablero[i, j] = 0
                        contador = contador + 1
            return nuevo_tablero

#creacion de figura en matplotlib

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        titulo = f'Turno: {self.cuenta}'  # poner el numero de turno como titulo de la figura de matplotlib
        ax.set_title(titulo)  # agrega lo anterior como titulo de la figura
        imagen = ax.imshow(tablero, interpolation="none", aspect="equal", cmap=cm.bwr)
        plt.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False)

        def animacion(i):
            global tablero
            if self.pause == False:
                tablero = paso(tablero)
                imagen.set_data(tablero)

            return imagen,

        anim = animation.FuncAnimation(fig, animacion,
                                       frames=100, blit=True, interval=(self.TimeFrame * 1000),
                                       repeat=True)
        plt.show()

#sospecho que se esta agregando al scrolled window pero este no esta agregado en la ventana principal

        #mostrar figura
    def fronteras_toroidales(self, widget):
        def vecindad(tablero):
#conteo de las vivas para ver si una celula tiene sobrepoblacion o esta en soledad
#np.roll podria hacerse la analogia que es como mover el tablero en las direcciones indicadas y a partir de eso, contar
            total = (
                np.roll(np.roll(tablero, 1, 1), 1, 0) +  # Abajo-derecha
                np.roll(tablero, 1, 0) +  # Abajo
                np.roll(tablero(tablero, -1, 1), 1, 0) +  # Abajo-izquierda
                np.roll(tablero, -1, 1) +  # Izquierda
                np.roll(np.roll(tablero, -1, 1), -1, 0) +  # Arriba-izquierda
                np.roll(tablero, -1, 0) +  # Arriba
                np.roll(np.roll(tablero, 1, 1), -1, 0) +  # Arriba-derecha
                np.roll(tablero, 1, 1)  # Derecha
            )
            return total


        def paso(tablero):
#Aplicar las reglas del juego
            v = vecindad(tablero)
            nuevo_tablero = tablero.copy()  # Copia de la matriz para no sobreescribir
            for i in range(nuevo_tablero.shape[0]):
                for j in range(nuevo_tablero.shape[1]):
                    if v[i, j] == 3 or (v[i, j] == 2 and nuevo_tablero[i, j]):
                        nuevo_tablero[i, j] = 1
                    else:
                        nuevo_tablero[i, j] = 0
            return nuevo_tablero

        def animacion(i):
            global tablero
            if self.pause == False:
                tablero = paso(tablero)
                imagen.set_data(tablero)

            return imagen,

#parte grafica del tablero,esto luego se agrega usado un scrolled window y FigCanvas
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        titulo = f'Turno: {contador}'  # poner el numero de turno como titulo de la figura de matplotlib
        ax.set_title(titulo)  # agrega lo anterior como titulo de la figura
        global imagen
        imagen = ax.imshow(tablero, interpolation="none", aspect="equal", cmap=cm.bwr)
        plt.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelleft=False,
            labelbottom=False)

        anim = animation.FuncAnimation(fig, animacion, frames=100, blit=True, interval=(self.TimeFrame * 1000),
                                       save_count=1, repeat=True)
        plt.show()

        # botones de play/pause y de generar captura de pantalla
        boton_jugar = Gtk.Button('Jugar/Pausa')
        boton_jugar.connect('clicked', )
        grid.attach_next_to(boton_jugar, scrolled, Gtk.PositionType.RIGHT, 5, 5)

        boton_captura = Gtk.Button('Captura de pantalla')
        boton_captura.connect('clicked', self.captura_de_pantalla)
        grid.attach_next_to(boton_captura, boton_jugar, Gtk.PositionType.RIGHT, 5, 5)

        t = FigureCanvas(fig)
        scrolled.add(t)

    def segundos_espera(self,widget):
        pass

    def acerca_de(self, widget):
        #acerca de dialogo
        vbox = Gtk.VBox()
        acerca_de_dialogo = Gtk.AboutDialog()
        acerca_de_dialogo.set_program_name('El juego de la vida')
        acerca_de_dialogo.set_version('PM 1')
        acerca_de_dialogo.set_authors('MCM')
        acerca_de_dialogo.set_copyright('Desarrollo de interfaz gráfica en Gtk 3.0')
        acerca_de_dialogo.set_comments('Uso de Gtk 3.0, Numpy, MatplotLib')
        acerca_de_dialogo.set_website('https://github.com/MariajoseChinchilla/TestGit/blob/master/Main.py')
        vbox.pack_start(acerca_de_dialogo, False, False, 0)
        self.add(vbox)
        acerca_de_dialogo.run()
        acerca_de_dialogo.destroy()

    def codigo_fuente(self, widget):
        webbrowser.open_new_tab('https://github.com/MariajoseChinchilla/TestGit/blob/master/Main.py')


#Acciones de los radio botones
    def elegido_normal(self, widget):
        pass
    def elegido_toroidal(self, widget):
        pass

win = JuegoDeLaVida()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()