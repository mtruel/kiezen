<script lang="ts">
import { defineComponent } from 'vue'
import { ref, onMounted } from 'vue'
import { api, type Song } from '../api'
import { useErrorHandler } from '../composables/useErrorHandler'
import { useLoadingState } from '../composables/useLoadingState'
import SongTable from './songs/SongTable.vue'
import ErrorMessage from './common/ErrorMessage.vue'

export default defineComponent({
  name: 'SongList',
  components: {
    SongTable,
    ErrorMessage
  },
  setup() {
    const { error, handleError, clearError } = useErrorHandler()
    const { isLoading, withLoading } = useLoadingState()
    const songs = ref<Song[]>([])
    const songToDelete = ref<string | null>(null)
    const deleteTimeout = ref<number | null>(null)

    const emit = defineEmits<{
      (e: 'play-song', song: Song): void
    }>()

    const fetchSongs = async () => {
      try {
        clearError()
        songs.value = await withLoading(() => api.getSongs())
      } catch (err) {
        handleError(err, 'Failed to load songs. Please check your connection and try again.')
      }
    }

    const deleteSong = async (songId: string) => {
      try {
        clearError()
        await withLoading(() => api.deleteSong(songId))
        await fetchSongs()
        songToDelete.value = null
        if (deleteTimeout.value) {
          clearTimeout(deleteTimeout.value)
          deleteTimeout.value = null
        }
      } catch (err) {
        handleError(err, 'Failed to delete song. Please try again.')
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

    return {
      error,
      isLoading,
      songs,
      songToDelete,
      fetchSongs,
      handleDeleteClick,
      playSong,
      isDummySong
    }
  }
})
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
    
    <SongTable 
      v-else-if="!error"
      :songs="songs"
      :song-to-delete="songToDelete"
      @play-song="$emit('play-song', $event)"
      @delete-song="handleDeleteClick"
    />
  </div>
</template>

<style scoped>
/* Remove all custom CSS as we're using Tailwind now */
</style> 