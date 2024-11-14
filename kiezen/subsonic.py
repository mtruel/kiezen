from pathlib import Path

# WEBDAV_URL = "https://cloud.truel.fr/remote.php/dav/files/mtruel/"
# WEBDAV_USER = "mtruel"
# WEBDAV_PASSWORD = "NgpDJ-sFpmc-xxBDi-AYoAC-CFkKY"

WEBDAV_URL = "http://webdav"
WEBDAV_USER = "mtruel"
WEBDAV_PASSWORD = "password"
WEBDAV_PORT = 80


SUBSONIC_URL = "http://navidrome" # https://music2.truel.fr
# SUBSONIC_URL = "https://music2.truel.fr"
SUBSONIC_USER = "mtruel" # mtruel
SUBSONIC_PASSWORD = "password" # Jrfs7Te8P4joB3Pm@BJiR^96s#qgYmb&m&mxjDTYcHenEyj5!w@6SGv
# SUBSONIC_PASSWORD = "Jrfs7Te8P4joB3Pm@BJiR^96s#qgYmb&m&mxjDTYcHenEyj5!w@6SGv"
SUBSONIC_PORT = 4533 # 443
# SUBSONIC_PORT = 443


def with_jellyfin():
    from jellyfin_apiclient_python import JellyfinClient
    client = JellyfinClient()
    client.config.app('your_brilliant_app', '0.0.1', 'machine_name', 'unique_id')
    client.config.data["auth.ssl"] = True



    client.config.data["app.name"] = 'your_brilliant_app'
    client.config.data["app.version"] = '0.0.1'
    client.authenticate({"Servers": [{"AccessToken": "358501172f2e448eb6ae93fe715d0281", "address": "https://music.truel.fr"}]},
                        discover=True)

    client.jellyfin.play_sync_play()
    # client.jellyfin.search_media_items(
    #     term="Bugge", media="Audio")
    # pass


def find_file(client, folder, name):
    folders_found = []
    for item in client.list(folder):
        print(item)
        item: str
        if item == name:
            return item

        if item.endswith("/") and Path(item).name != Path(folder).name:
            folders_found.append(item)
    print(folders_found)

    # If not in the files, search in the folders
    for sub_folder in folders_found:
        return find_file(client, folder + sub_folder, name)
    return None


def with_subsonic():
    from libopensonic.connection import Connection

    conn = Connection(SUBSONIC_URL, SUBSONIC_USER, SUBSONIC_PASSWORD, port=SUBSONIC_PORT)
    songs = conn.getRandomSongs(size=2)
    print(songs[0].to_dict())

    def get_playlist(conn: Connection, name):
        playlists = conn.getPlaylists()
        for playlist in playlists:
            if playlist.name == name:
                break
        return conn.getPlaylist(playlist.id)

    playlist = get_playlist(conn, "Test")
    print(playlist.songs)
    for songs in playlist.songs:
        print(songs.path)
    SONG_TEST_PATH = playlist.songs[0].path
    return SONG_TEST_PATH


# We pass in the base url, the username, password, and port number
# Be sure to use https:// if this is an ssl connection!




def webdav_part(SONG_TEST_PATH):
    from webdav3.client import Client

    WEBDAV_FOLDER = "/"
    options = {
        'webdav_hostname': "{url}:{port}".format(url=WEBDAV_URL,port=WEBDAV_PORT),
        'webdav_login': WEBDAV_USER,
        'webdav_password': WEBDAV_PASSWORD
    }
    print(options)
    client = Client(options)
    # client.session.proxies(...) # To set proxy directly into the session (Optional)
    # client.session.auth(...) # To set proxy auth directly into the session (Optional)
    # reponse = client.info("/Music/Mix library/Titres")
    print(client.list(WEBDAV_FOLDER))

    print("returned ", find_file(client, WEBDAV_FOLDER, SONG_TEST_PATH))
    print("searched ", SONG_TEST_PATH)


def main():
    # song_path = with_jellyfin()
    song_path = with_subsonic()
    webdav_part(song_path)


if __name__ == "__main__":
    main()
