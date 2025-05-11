<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type Song } from '../api'
import { useErrorHandler } from '../composables/useErrorHandler'
import { useLoadingState } from '../composables/useLoadingState'
import SongsTable from './songs/SongsTable.vue'
import ErrorMessage from './common/ErrorMessage.vue'
import { useSongStore } from '../stores/songStore'

const props = defineProps<{
  currentSong: Song | null
  isPlaying: boolean
}>()

const emit = defineEmits<{
  (e: 'play-song', song: Song): void
  (e: 'song-deleted', songId: string): void
  (e: 'load-song', song: Song): void
}>()

const { error, handleError, clearError } = useErrorHandler()
const { isLoading, withLoading } = useLoadingState()
const songStore = useSongStore()
const songToDelete = ref<string | null>(null)
const deleteTimeout = ref<number | null>(null)

const fetchSongs = async () => {
  try {
    clearError()
    await withLoading(() => songStore.fetchSongs())
  } catch (err) {
    handleError(err, 'Failed to load songs. Please check your connection and try again.')
  }
}

const deleteSong = async (songId: string) => {
  try {
    clearError()
    // First check if the song exists
    const song = songStore.songs.find(s => s.id === songId)
    if (!song) {
      handleError(new Error('Song not found'), 'Song not found. It may have been already deleted.')
      return
    }

    // Always emit the deletion event to update the queue
    emit('song-deleted', songId)

    // Then proceed with the deletion
    await withLoading(() => api.deleteSong(songId))
    await fetchSongs()
    songToDelete.value = null
    if (deleteTimeout.value) {
      clearTimeout(deleteTimeout.value)
      deleteTimeout.value = null
    }
  } catch (err: any) {
    console.error('Delete error:', err)
    if (err.response?.data?.detail) {
      handleError(err, err.response.data.detail)
    } else if (err.response?.status === 404) {
      handleError(err, 'Song not found. It may have been already deleted.')
    } else {
      handleError(err, `Failed to delete song: ${err.message || 'Unknown error'}`)
    }
  }
}

const handleDeleteClick = (songId: string) => {
  if (songToDelete.value === songId) {
    deleteSong(songId)
  } else {
    songToDelete.value = songId
    if (deleteTimeout.value) {
      clearTimeout(deleteTimeout.value)
    }
    deleteTimeout.value = window.setTimeout(() => {
      songToDelete.value = null
      deleteTimeout.value = null
    }, 3000)
  }
}

const playSong = (song: Song) => {
  emit('play-song', song)
}

const isDummySong = (song: Song) => {
  return song.isDummy === 1
}

onMounted(fetchSongs)
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Songs</h2>
    
    <ErrorMessage 
      v-if="error" 
      :message="error" 
      @retry="fetchSongs" 
    />

    <div v-if="isLoading" class="text-gray-600">
      Loading songs...
    </div>
    
    <SongsTable 
      v-else-if="!error"
      :songs="songStore.songs"
      :song-to-delete="songToDelete"
      :current-song="currentSong"
      :is-playing="isPlaying"
      @play-song="$emit('play-song', $event)"
      @delete-song="handleDeleteClick"
      @load-song="$emit('load-song', $event)"
    />
  </div>
</template>

<style scoped>
/* Remove all custom CSS as we're using Tailwind now */
</style> 