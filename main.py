from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

import threading

from plyer import filechooser

from splitter import split_zip


class MangaSplitter(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 20

        self.estado = Label(
            text="Selecciona un ZIP",
            font_size=20
        )

        self.add_widget(self.estado)

        boton = Button(
            text="Seleccionar ZIP",
            font_size=22,
            size_hint=(1, .2)
        )

        boton.bind(on_press=self.abrir)

        self.add_widget(boton)

    def abrir(self, instance):

        filechooser.open_file(
            filters=[("ZIP", "*.zip")],
            on_selection=self.seleccionado
        )

    def seleccionado(self, archivos):

        if not archivos:
            return

        ruta = archivos[0]

        self.estado.text = "Procesando..."

        threading.Thread(
            target=self.procesar,
            args=(ruta,),
            daemon=True
        ).start()

    def procesar(self, ruta):

        try:

            salida = split_zip(ruta)

            Clock.schedule_once(
                lambda dt:
                setattr(
                    self.estado,
                    "text",
                    f"Listo\n{salida}"
                )
            )

        except Exception as e:

            Clock.schedule_once(
                lambda dt:
                setattr(
                    self.estado,
                    "text",
                    str(e)
                )
            )


class MangaSplitterApp(App):

    def build(self):

        self.title = "Manga Splitter"

        return MangaSplitter()


if __name__ == "__main__":

    MangaSplitterApp().run()
