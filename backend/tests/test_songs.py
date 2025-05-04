from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.conftest import client, test_song

def test_create_song(client):
    response = client.post(
        "/api/songs/",
        json={
            "title": "Test Song",
            "artist": "Test Artist",
            "file_path": "test.mp3",
            "is_dummy": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Song"
    assert data["artist"] == "Test Artist"
    assert data["file_path"] == "test.mp3"

def test_get_songs(client, test_song):
    response = client.get("/api/songs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Find our test song in the list
    test_song_in_list = next(
        (song for song in data if song["id"] == test_song["id"]),
        None
    )
    assert test_song_in_list is not None
    assert test_song_in_list["title"] == test_song["title"]
    assert test_song_in_list["artist"] == test_song["artist"]
    assert test_song_in_list["file_path"] == test_song["file_path"]

def test_get_song(client, test_song):
    response = client.get(f"/api/songs/{test_song['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_song["title"]
    assert data["artist"] == test_song["artist"]
    assert data["file_path"] == test_song["file_path"]

def test_update_song(client, test_song):
    response = client.put(
        f"/api/songs/{test_song['id']}",
        json={
            "title": "Updated Song",
            "artist": "Updated Artist",
            "file_path": "updated.mp3",
            "is_dummy": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Song"
    assert data["artist"] == "Updated Artist"
    assert data["file_path"] == "updated.mp3"

def test_delete_song(client, test_song):
    response = client.delete(f"/api/songs/{test_song['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Song deleted successfully"
    
    # Verify song is deleted
    response = client.get(f"/api/songs/{test_song['id']}")
    assert response.status_code == 404 