<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type Song } from '../api'

const songs = ref<Song[]>([])

const fetchSongs = async () => {
  songs.value = await api.getSongs()
}

const deleteSong = async (songId: string) => {
  await api.deleteSong(songId)
  await fetchSongs()
}

onMounted(fetchSongs)
</script>

<script lang="ts">
export default {
  name: 'SongList'
}
</script>

<template>
  <div class="song-list">
    <h2>Songs</h2>
    
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Artist</th>
          <th>Type</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="song in songs" :key="song.id">
          <td>{{ song.title }}</td>
          <td>{{ song.artist }}</td>
          <td>{{ song.isDummy ? 'Dummy' : 'Regular' }}</td>
          <td>
            <button @click="deleteSong(song.id)" class="delete-btn">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.song-list {
  margin-top: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.delete-btn {
  background-color: #ff4444;
  color: white;
}
</style> 