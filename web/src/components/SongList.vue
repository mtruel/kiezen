<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type Song } from '../api'

const songs = ref<Song[]>([])
const error = ref<string | null>(null)
const isLoading = ref(false)

const emit = defineEmits<{
  (e: 'play-song', song: Song): void
}>()

const fetchSongs = async () => {
  try {
    isLoading.value = true
    error.value = null
    songs.value = await api.getSongs()
  } catch (err) {
    error.value = 'Failed to load songs. Please check your connection and try again.'
    console.error('Error fetching songs:', err)
  } finally {
    isLoading.value = false
  }
}

const deleteSong = async (songId: string) => {
  try {
    error.value = null
    await api.deleteSong(songId)
    await fetchSongs()
  } catch (err) {
    error.value = 'Failed to delete song. Please try again.'
    console.error('Error deleting song:', err)
  }
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
  <div>
    <h2 class="text-2xl font-bold mb-4">Songs</h2>
    
    <div v-if="error" class="bg-red-50 border border-red-400 rounded-lg p-4 mb-4 flex items-center justify-between">
      <p class="text-red-600">{{ error }}</p>
      <button @click="fetchSongs" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors">Retry</button>
    </div>

    <div v-if="isLoading" class="text-gray-600">
      Loading songs...
    </div>
    
    <table v-else-if="!error" class="w-full border-collapse">
      <thead>
        <tr>
          <th class="p-3 text-left border-b bg-gray-50">Title</th>
          <th class="p-3 text-left border-b bg-gray-50">Artist</th>
          <th class="p-3 text-left border-b bg-gray-50">Type</th>
          <th class="p-3 text-left border-b bg-gray-50">URL</th>
          <th class="p-3 text-left border-b bg-gray-50">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="song in songs" :key="song.id" class="hover:bg-gray-50">
          <td class="p-3 border-b">{{ song.title }}</td>
          <td class="p-3 border-b">{{ song.artist }}</td>
          <td class="p-3 border-b">{{ isDummySong(song) ? 'Dummy' : 'Regular' }}</td>
          <td class="p-3 border-b">
            <a v-if="isDummySong(song) && song.url" 
               :href="song.url" 
               target="_blank" 
               rel="noopener noreferrer"
               class="inline-block px-2 py-1 bg-gray-50 border border-gray-200 rounded font-mono text-sm max-w-[300px] truncate hover:bg-gray-100 hover:border-gray-300 transition-colors"
               :title="song.url">
              🔗 {{ song.url }}
            </a>
            <span v-else>-</span>
          </td>
          <td class="p-3 border-b">
            <div class="flex items-center gap-2">
              <button v-if="!isDummySong(song)" 
                      @click="playSong(song)" 
                      class="px-3 py-1 bg-emerald-600 text-white rounded hover:bg-emerald-700 transition-colors">
                ▶
              </button>
              <button @click="deleteSong(song.id)" 
                      class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition-colors">
                Delete
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
/* Remove all custom CSS as we're using Tailwind now */
</style> 