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

<template>
  <div class="mt-8">
    <h2 class="text-2xl font-bold mb-4">Playlists</h2>

    <div v-if="error" class="bg-red-50 border border-red-400 rounded-lg p-4 text-red-600 mb-4">
      {{ error }}
    </div>
    
    <div v-if="success" class="bg-green-50 border border-green-400 rounded-lg p-4 text-green-600 mb-4">
      {{ success }}
    </div>

    <div class="flex gap-4 mb-8">
      <input 
        type="text" 
        v-model="newPlaylistName" 
        placeholder="New playlist name"
        @keyup.enter="createPlaylist"
        class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
      >
      <button 
        @click="createPlaylist" 
        class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
      >
        Create Playlist
      </button>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div v-for="playlist in playlists" :key="playlist.id" class="bg-gray-50 p-4 rounded-lg relative">
        <h3 class="text-lg font-semibold mb-2">{{ playlist.name }}</h3>
        <p class="text-gray-600">{{ playlist.songs.length }} songs</p>
        <button 
          @click="deletePlaylist(playlist.id)" 
          class="absolute top-2 right-2 px-2 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Remove all custom CSS as we're using Tailwind now */
</style> 