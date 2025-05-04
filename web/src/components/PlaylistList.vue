<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type Playlist } from '../api'

const playlists = ref<Playlist[]>([])
const newPlaylistName = ref('')
const error = ref<string | null>(null)
const success = ref<string | null>(null)

const fetchPlaylists = async () => {
  playlists.value = await api.getPlaylists()
}

const createPlaylist = async () => {
  if (!newPlaylistName.value.trim()) return
  
  try {
    error.value = null
    success.value = null
    
    await api.createPlaylist(newPlaylistName.value)
    newPlaylistName.value = ''
    await fetchPlaylists()
    success.value = 'Playlist created successfully!'
  } catch (err) {
    error.value = 'Failed to create playlist. Please try again.'
    console.error(err)
  }
}

const deletePlaylist = async (playlistId: string) => {
  try {
    error.value = null
    success.value = null
    
    await api.deletePlaylist(playlistId)
    await fetchPlaylists()
    success.value = 'Playlist deleted successfully!'
  } catch (err) {
    error.value = 'Failed to delete playlist. Please try again.'
    console.error(err)
  }
}

onMounted(fetchPlaylists)
</script>

<script lang="ts">
export default {
  name: 'PlaylistList'
}
</script>

<template>
  <div class="playlist-list">
    <h2>Playlists</h2>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-if="success" class="success-message">
      {{ success }}
    </div>

    <div class="create-playlist">
      <input 
        type="text" 
        v-model="newPlaylistName" 
        placeholder="New playlist name"
        @keyup.enter="createPlaylist"
      >
      <button @click="createPlaylist" class="create-btn">Create Playlist</button>
    </div>

    <div class="playlists">
      <div v-for="playlist in playlists" :key="playlist.id" class="playlist-item">
        <h3>{{ playlist.name }}</h3>
        <p>{{ playlist.songs.length }} songs</p>
        <button @click="deletePlaylist(playlist.id)" class="delete-btn">Delete</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.playlist-list {
  margin-top: 2rem;
}

.create-playlist {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

input[type="text"] {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.create-btn {
  background-color: #42b983;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.playlists {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.playlist-item {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  position: relative;
}

.playlist-item h3 {
  margin: 0 0 0.5rem 0;
}

.playlist-item p {
  margin: 0;
  color: #666;
}

.delete-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: #ff4444;
  color: white;
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.error-message {
  color: #ff4444;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #ffeeee;
  border-radius: 4px;
}

.success-message {
  color: #42b983;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #f0fff0;
  border-radius: 4px;
}
</style> 