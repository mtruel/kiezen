
## Roadmap

### Version 0.0.1

- Setup dev environment

### Version 0.1

Minimum viable product :

- Frontend :
    - List of songs : playable songs and not playabe songs
    - Basic player
    - Add a non-playable song (via text url−>input/ name,artist...−>form ? )
    - Add a playable song (file select and upload)
- Backend :
    - A subsonic server for playable songs
    - A folder for storing files
    - An sqlite database :
        - A table for all songs with a uuid, a file to a path(file if playable, url if not, a ref to subsonic server)


Empty the list on submit
Submit multiple files
Be able to add a file to the database
tags with mutagen

Docker et deploiement

### Version 0.2
Make a form to add a dummy song

### Version 0.3

Remake a basic web audio player
Wavesurfer load with Blob
analyse de waveform ? 

### Version 0.4
Script de scan des dossiers et de synchronisation avec la DB
page édition d'un seul morceau

### Version 0.5
Authification
Edition de tags

Multi library

Automatic reach for tags, covers and infos online (musibrainz ? )
Etapes : 
- Formulaire d'ajouts de GHOST morceaux
- stokage backend des fichiers


Multi user ??

for tags:
- mutagen 
- musicbrainzngs

for song infos analysis : 
- librosa 
- Essentia

for playlist m3u export : 
- m3u8




### Version 0.3

## Draft
As a DJ I want :
- When I listen to some music, share it to my service to save it for later.
- Listen to songs I need to add i my library and add them.
- Organize my lib into crates or playlists, tag songs with genres

As a DJ I want :

- Listen to my music library
    - Listen at random (with higher proability for new songs (or old))
    - Listen to a label
    - Listen to playlists
    - Listen to a genre
- To add new music easly in my library
    - Add a folder
    - Add a file
    - Add a dummy song before I buy it (with a link to buy it or to listen to it)
- Depretiate old songs (or the one I dont want to see animore)
    - Depretiate a song
    - Delete a song
- Manage multiple libraries (multiple folders for multiple usb keys ? Or be able to export a folder)
- The player
    - See the BPM (based on other software analysis or based on internal analysis)
    - See the musical key (based on other software analysis or based on internal analysis)
    - See the waveform
    - Check audio quality of my files with a spectrogram (see spek)
    - Edit and see the tags of my songs (At least: artist, label, album, title, picture) and then (song NRJ, favorite
      tracks)
- Listen to my DJ library on the Go (Subsonic ?)
    - To depreciate easly
    - To create playlists
    - Mark songs
- Offline ?

- Share futures to social networks/text
- Export my files/library in other DJ softwares
- Have playlist
- Proximity with other songs feature ? Will listen to songs that are close based on every noise at once or spotify
  api ??
- Export my files on my usb key

## Technologies

- A go backend :
    - SQLite database per user ?
    - Gin for the API
    - GORM for the database
    - a subsonic server for the on the go feature
- Vue frontend (and wails v3 when ready) :
  - 
- Offline possible (wails)
- Small desktop app for file sync



