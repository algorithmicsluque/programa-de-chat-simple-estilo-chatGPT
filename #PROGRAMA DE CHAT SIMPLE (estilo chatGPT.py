#PROGRAMA DE CHAT SIMPLE (estilo chatGPT)
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
#navegar por la pantalla
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition 

#Colores (rojo, verde, azul, transparencia)
FONDO = (0.13, 0.13, 0.13, 1) # gris oscuro
BARRA = (0.09, 0.09, 0.09, 1) # casi negro
VERDE = (0.06, 0.64, 0.5, 1)  # verde ChatGPT
GRIS = (0.25, 0.25, 0.25, 1)  # burBuja del bot
CAJA = (0.2, 0.2, 0.2, 1)     # caja de texto

ANCHO_MAX = 260 # ancho maximo de una burbuj

Window.clearcolor = FONDO
Window.size = (400, 650) # tamaño tipo celular


# ------BURBUJA DE MENSAJE------
class Burbuja(Label):
    def __init__(self, texto, color_fondo, **Kwargs):
        super().__init__(text=texto, size_hint=(None, None), padding=(14, 10), **Kwargs)

        # Dibujar un rectangulo rondeaddo detras del texto
        with self.canvas.before:
            Color(*color_fondo)
            self.fondo = RoundedRectangle(radius=[18])
        self.bind(pos=self.dibujar, size=self.dibujar)

        # Si el texto es muy largo, hacer salto de linea
        self.texture_update()
        if self.texture_size[0] > ANCHO_MAX:
            self.text_size = (ANCHO_MAX, None)
            self.texture_update()
        self.size = self.texture_size

    def dibujar(self, *args):
        self.fondo.pos = self.pos
        self.fondo.size = self.size



class PantallaInicio(Screen):
    def __init__(self, **Kwargs):
        super().__init__(**Kwargs)
        caja = BoxLayout(orientation="vertical", padding=40, spacing=20)
        caja.add_widget(Label(text="Mi ChatGPT", font_size=36, bold=True))
        caja.add_widget(Label(text="Tu asistente personal", font_size=18, color=(0.7, 0.7, 0.7, 1)))
        
        boton = Button(text="Empezar a chatear", size_hint_y=None, height=55,
                       background_normal="", background_color=VERDE, bold=True)
        boton.bind(on_press=lambda b: App.get_running_app().ir_a("chat"))
        caja.add_widget(boton)
        self.add_widget(caja)


#------PANTALLA DE CHAT------
class PantallaChat(Screen):
    def __init__(self, **Kwargs):
        super().__init__(**Kwargs)
        caja = BoxLayout(orientation="vertical")

        #Lista de mensajes (con scroll)
        self.scroll = ScrollView()
        self.lista = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.lista.bind(minimum_height=self.lista.setter("height"))
        self.scroll.add_widget(self.lista)
        caja.add_widget(self.scroll)

        # Fila d abajo: caja de texto + boton
        fila = BoxLayout(size_hint_y=None, height=60, padding=8, spacing=8)
        self.entrada = TextInput(multiline=False, hint_text="Escribe un mensaje...",
                                 background_normal="", background_active="",
                                 background_color=CAJA, foreground_color=(1, 1, 1, 1),
                                 cursor_color=(1, 1, 1, 1), padding=(12, 12))
        self.entrada.bind(on_text_validate=self.enviar) # enviar con Enter
        boton = Button(text="Enviar", size_hint_x=0.3, background_normal="",
                       background_color=VERDE, bold=True)
        boton.bind(on_press=self.enviar)
        fila.add_widget(self.entrada)
        fila.add_widget(boton)
        caja.add_widget(fila)

        self.add_widget(caja)

    def enviar(self, *args):
        texto = self.entrada.text.strip()
        if texto == "":
            return # no enviar mensajes vacios
        
        self.agregar_mensaje(texto, es_usuario=True)
        self.entrada.text = ""
        self.entrada.focus = True

        # El bot responde despues de medio segundo(SIEMPRE lo mismo
        lambda dt: self.agregar_mensaje("hola no más", es_usuario=False)

    def agregar_mensaje(self, texto, es_usuario):
        if es_usuario:
            burbuja = Burbuja(texto, VERDE)
        else:
            burbuja = Burbuja(texto, GRIS)

        fila = BoxLayout(size_hint_y=None, height=burbuja.height)
        if es_usuario:
            fila.add_widget(Widget()) # espacio vacio -> burbuja a la derecha
            fila.add_widget(burbuja)
        else:
            fila.add_widget(burbuja)
            fila.add_widget(Widget()) # ESPACIO VACIO -> BURBUJA A LA IZQUIERDA
        self.lista.add_widget(fila)

        #Bajar el scroll hasta el ultimo mensaje
        Clock.schedule_once(lambda dt: setattr(self.scroll, "croll_y", 0), 0.1)


#----PANTALLA: ACERCA DE----
class PantallaAcerca(Screen):
    def __init__(self, **Kwargs):
        super().__init__(**Kwargs)
        self.add_widget(Label(
            text="Mi ChatGPT\n\nHecho con Python y Kivy\nVersion 1.0",
        halign="center", font_size=18))


#----APP PRINCIPAL----
class ChatApp(App):
    def build(self):
        self.title = "Mi ChatGPT"
        raiz = BoxLayout(orientation="vertical")

        # Menu de navegacion (arriba)
        menu = BoxLayout(size_hint_y=None, height=50)
        self.botones = {}
        for nombre, texto in [("inicio", "Inicio"), ("chat", "Chat"), ("acerca", "Acerca de")]:
            boton = Button(text=texto, background_normal="", background_color=BARRA)
            # n=nombre guarda a que pantalla va cada boton
            boton.bind(on_press=lambda b, n=nombre: self.ir_a(n))
            self.botones[nombre] = boton
            menu.add_widget(boton)
        raiz.add_widget(menu)

        # Pantallas
        self.pantallas = ScreenManager (transition=FadeTransition())
        self.pantallas.add_widget(PantallaInicio(name="inicio"))
        self.pantallas.add_widget(PantallaChat(name="chat"))
        self.pantallas.add_widget(PantallaAcerca(name="acerca"))
        raiz.add_widget(self.pantallas)

        self.ir_a("inicio")
        return raiz

    def ir_a(self, nombre):
        self.pantallas.current = nombre
        # Pintar de verde el boton de la pantalla actual
        for n, boton in self.botones.items():
            if n == nombre:
                boton.background_color = VERDE
            else:
                boton.background_color = BARRA


ChatApp().run()
