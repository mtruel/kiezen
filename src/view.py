import gi

from enum import Enum

from setproctitle import setproctitle, setthreadtitle, getproctitle, getthreadtitle
from model import Model

setproctitle("dj-audio-player")
setthreadtitle("dj-audio-player")
print("Proc ", getproctitle())
print("Thread ", getthreadtitle())
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


@Gtk.Template(resource_path="./dj-audio-player/player.ui")
class View(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title="DJ Audio Player")
        self.model = Model()

        # self.selected_file = None
        # self.player = AudioPlayer()

        header_bar = Gtk.HeaderBar()
        self.set_titlebar(header_bar)

        box = Gtk.Box(spacing=6)
        player_box = PlayerBox()
        self.set_child(player_box)
        # self.set_child(box)

        open_button = Gtk.Button(label="Open File")
        open_button.connect("clicked", self.on_button_open_file_clicked)
        header_bar.pack_start(open_button)

        icon_button = Gtk.Button(icon_name="open-menu-symbolic")
        header_bar.pack_end(icon_button)

        # play_button = Gtk.Button(label="Play")
        # play_button.props.hexpand = True
        # play_button.connect("clicked", self.on_button_play_clicked)
        # box.append(play_button)

        # pause_button = Gtk.Button(label="Pause")
        # pause_button.props.hexpand = True
        # pause_button.connect("clicked", self.on_button_pause_clicked)
        # box.append(pause_button)

        # track_info = Gtk.Label(label="Track info")
        # box.append(track_info)

    def on_button_open_file_clicked(self, _widget):
        dialog = Gtk.FileDialog()
        filter = Gtk.FileFilter()
        filter.set_name("Audio files")
        supported_formats = ["mp3", "wav", "ogg", "flac", "m4a", "wma", "aac"]
        for fmt in supported_formats:  # format is a reserved word
            filter.add_pattern(f"*.{fmt}")

        dialog.set_default_filter(filter)
        dialog.open(self, None, self.on_file_selected)

    def on_file_selected(self, dialog, response):
        file = dialog.open_finish(response)
        filepath = file.get_path()
        print("File selected", filepath)
        self.selected_file = filepath
        self.player.open_file(self.selected_file)

    # def on_button_play_clicked(self, _widget):
    #     print("Play")
    #     if self.play_state == PlayState.STOPPED:
    #         self.player.play()
    #     elif self.play_state == PlayState.PAUSED:
    #         self.player.resume()
    #     self.play_state = PlayState.PLAYING

    # def on_button_pause_clicked(self, _widget):
    #     print("Pause")
    #     self.player.pause()
    #     self.play_state = PlayState.PAUSED


class PlayerBox(Gtk.CenterBox):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        play_button = Gtk.Button(label="Play")
        play_button.connect("clicked", self.on_button_play_clicked)
        self.(play_button)

        pause_button = Gtk.Button(label="Pause")
        pause_button.connect("clicked", self.on_button_pause_clicked)
        self.append(pause_button)

    def on_button_play_clicked(self, _widget):
        print("Play")

    def on_button_pause_clicked(self, _widget):
        print("Pause")


def on_activate(app):
    view = View(application=app)
    view.present()


if __name__ == "__main__":
    app = Gtk.Application(application_id="com.dj-lib-organizer.App")
    app.connect("activate", on_activate)
    app.run(None)
