<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type Song } from '../api'

const songs = ref<Song[]>([])

const emit = defineEmits<{
  (e: 'play-song', song: Song): void
}>()

const fetchSongs = async () => {
  songs.value = await api.getSongs()
}

const deleteSong = async (songId: string) => {
  await api.deleteSong(songId)
  await fetchSongs()
}

const playSong = (song: Song) => {
  emit('play-song', song)
}

const isDummySong = (song: Song) => {
  return song.isDummy === 1
}

onMounted(fetchSongs)

// Expose the fetchSongs method to parent components
defineExpose({
  fetchSongs
})
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
          <th>URL</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="song in songs" :key="song.id">
          <td>{{ song.title }}</td>
          <td>{{ song.artist }}</td>
          <td>{{ isDummySong(song) ? 'Dummy' : 'Regular' }}</td>
          <td>
            <a v-if="isDummySong(song) && song.url" 
               :href="song.url" 
               target="_blank" 
               rel="noopener noreferrer"
               class="url-link"
               :title="song.url">
              🔗 {{ song.url }}
            </a>
            <span v-else>-</span>
          </td>
          <td class="actions-cell">
            <div class="actions-wrapper">
              <button v-if="!isDummySong(song)" @click="playSong(song)" class="play-btn">▶</button>
              <button @click="deleteSong(song.id)" class="delete-btn">Delete</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.song-list {
  margin-top: 0;
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

.actions-cell {
  /* display: flex; align-items: center; gap: 0.5rem; */
}

.actions-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.play-btn {
  background-color: #42b983;
  color: white;
}

.play-btn:hover {
  background-color: #3aa876;
}

.delete-btn {
  background-color: #ff4444;
  color: white;
}

.delete-btn:hover {
  background-color: #ff3333;
}

.url-link {
  color: #2c3e50;
  text-decoration: none;
  word-break: break-all;
  display: inline-block;
  padding: 4px 8px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9em;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.url-link:hover {
  background-color: #e9ecef;
  text-decoration: none;
  border-color: #dee2e6;
}
</style> 