from dataclasses import dataclass
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from enum import Enum



from view import View
from player import AudioPlayer

from setproctitle import setproctitle, setthreadtitle, getproctitle, getthreadtitle
setproctitle("dj-audio-player")
setthreadtitle("dj-audio-player")
print("Proc ", getproctitle())
print("Thread ", getthreadtitle())


class Controler:
    def __init__(self) -> None:
        # self._init_view(app)
        self._init_player()

    def on_app_activate(self, app: Gtk.Application):
        self.view = View(application=app)
        self.view.present()

    def _init_player(self):
        self.player = AudioPlayer()


# def on_activate(app):
#     # Create window


if __name__ == "__main__":
    controler = Controler()
    app = Gtk.Application(application_id="com.dj-lib-organizer.App")
    app.connect("activate", controler.on_app_activate)
    app.run()
