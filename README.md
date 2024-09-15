# Dj Library Organizer
Simple DJ software to manage a music library. 

## Roadmap
### Version 0.0.1
- Setup dev environment
### Version 0.1
- GTK window
- Load and play a sound (simple audio, librosa)
- Play, pause
### Version 0.2
- Load a folder (recursive ?)
- Display the list of songs
- Move buttons (To delete, to commercial...)
- Progress in sound
- Package the app (Flatpak, brew, chocolaty, exe)
### Version 0.3
- Think about my workflowSound player in anticipation of the next versions 
### Future improvments Player module 
- Use a segment inside the callback function 
- be able to play multiple tracks at the same time
- Modify the track playback speed during playback
### Version 0.4
- Edit and view song tags (artist, label, album, title, picture)
- Add new music to the library
- Depreciate old songs
- Share feature
### Version 0.5
- BPM and musical key of a track
- Check audio quality with a spectrogram
- See the waveform
### Version 0.6
- Have playlists
### Version 0.7
- Listen to my DJ library on the Go (Subsonic ?)
### Version 0.8
- Export my files on my usb key (Compatible with Rekordbox)
- Compatibility with other DJ softwares
### Version 0.9
- Mark songs
### Version 1.0


## Links
- [GTK4 Docs](https://rafaelmardojai.pages.gitlab.gnome.org/pygobject-guide/gtk4/introduction.html)
- [Pygobject](https://gnome.pages.gitlab.gnome.org/pygobject/guide/api/index.html)
- [GTK Reference](https://amolenaar.pages.gitlab.gnome.org/pygobject-docs/Gtk-4.0/class-FileDialog.html#gi.repository.Gtk.FileDialog)


## Installation
### Dependencies
## Contribute
> sudo dnf install gcc gobject-introspection-devel cairo-gobject-devel pkg-config python3-devel gtk4
> sudo dnf install gtk4-devel






## Draft
As a DJ I want : 
- Edit and see the tags of my songs (At least: artist, label, album, title, picture) and then (song NRJ, favorite tracks)
- To add new music easly in my library
- See the BPM
- See the musical key of a track
- Check audio quality of my files with a spectrogram (see spek)
- Depretiate old songs (or the one I dont want to see animore)
- Export my files on my usb key 
- Export my files/library in other DJ softwares
- Have playlist
- See the waveform
- Listen to my DJ library on the Go (Subsonic ?)
    - To depreciate easly 
    - To create playlists
    - Mark songs 
- Share futures to social networks/text
