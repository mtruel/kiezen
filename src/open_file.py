import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class OpenAudioFile:
    def __init__(self, window) -> None:
        self.window = window

        self.setup()

    def setup(self):
        self.window = Gtk.Window(title="Open Audio File")
        self.window.set_default_size(200, 100)

        box = Gtk.Box(spacing=6)
        self.window.add(box)

        self.button = Gtk.Button(label="Open")
        self.button.connect("clicked", self.on_button_clicked)
        box.append(self.button)
