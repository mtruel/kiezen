import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api, type Song } from '../api'

export const useSongStore = defineStore('song', () => {
  const songs = ref<Song[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchSongs = async () => {
    try {
      isLoading.value = true
      error.value = null
      songs.value = await api.getSongs()
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch songs'
      console.error('Error fetching songs:', err)
    } finally {
      isLoading.value = false
    }
  }

  return {
    songs,
    isLoading,
    error,
    fetchSongs
  }
}) 