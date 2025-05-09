<script setup lang="ts">
import { ref, computed } from 'vue'
import { api, type Song } from '../../api'
import FormMessage from '../common/FormMessage.vue'

const emit = defineEmits<{
  (e: 'song-added'): void
}>()

const dummyForm = ref<Omit<Song, 'id'>>({
  title: '',
  artist: '',
  isDummy: 1,
  metadata: {}
})

const error = ref<string | null>(null)
const success = ref<string | null>(null)

// Computed property to check if at least one field is filled
const isDummyFormValid = computed(() => {
  return dummyForm.value.title.trim() !== '' || 
         dummyForm.value.artist.trim() !== '' || 
         dummyForm.value.url?.trim() !== '' ||
         dummyForm.value.metadata.genre?.trim() !== '' ||
         dummyForm.value.metadata.year !== undefined
})

const submitDummyForm = async () => {
  try {
    error.value = null
    success.value = null
    
    // Create the song with the URL mapped to link
    const songData = {
      ...dummyForm.value,
      link: dummyForm.value.url  // Map url to link for the backend
    }
    
    await api.createSong(songData)
    
    // Reset form
    dummyForm.value = {
      title: '',
      artist: '',
      isDummy: 1,
      url: '',  // Reset URL field
      metadata: {}
    }
    success.value = 'Dummy song added successfully!'
    emit('song-added')
  } catch (err) {
    error.value = 'Failed to add dummy song. Please try again.'
    console.error(err)
  }
}
</script>

<template>
  <div class="bg-white rounded-lg shadow p-6 max-w-md mx-auto">
    <h2 class="text-2xl font-bold mb-4">Add Dummy Song</h2>
    <form @submit.prevent="submitDummyForm" class="space-y-4">
      <FormMessage 
        :error="error"
        :success="success"
      />

      <div class="space-y-2">
        <label for="dummy-title" class="block text-sm font-medium text-gray-700">Title</label>
        <input 
          type="text" 
          id="dummy-title" 
          v-model="dummyForm.title"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
        >
      </div>

      <div class="space-y-2">
        <label for="dummy-artist" class="block text-sm font-medium text-gray-700">Artist</label>
        <input 
          type="text" 
          id="dummy-artist" 
          v-model="dummyForm.artist"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
        >
      </div>

      <div class="space-y-2">
        <label for="dummy-url" class="block text-sm font-medium text-gray-700">URL</label>
        <input 
          type="url" 
          id="dummy-url" 
          v-model="dummyForm.url"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
        >
      </div>

      <div class="space-y-2">
        <label for="dummy-genre" class="block text-sm font-medium text-gray-700">Genre</label>
        <input 
          type="text" 
          id="dummy-genre" 
          v-model="dummyForm.metadata.genre"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
        >
      </div>

      <div class="space-y-2">
        <label for="dummy-year" class="block text-sm font-medium text-gray-700">Year</label>
        <input 
          type="number" 
          id="dummy-year" 
          v-model="dummyForm.metadata.year"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
        >
      </div>

      <button 
        type="submit" 
        :disabled="!isDummyFormValid"
        class="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Add Dummy Song
      </button>
    </form>
  </div>
</template>

<script lang="ts">
export default {
  name: 'DummySongForm'
}
</script> 