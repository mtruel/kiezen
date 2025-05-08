<script setup lang="ts">
import { ref } from 'vue'
import { api, type Song } from '../../api'
import FormMessage from '../common/FormMessage.vue'

const emit = defineEmits<{
  (e: 'song-added'): void
}>()

const uploadForm = ref<Omit<Song, 'id'>>({
  title: '',
  artist: '',
  isDummy: 0,
  metadata: {}
})

const error = ref<string | null>(null)
const success = ref<string | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return

  const file = input.files[0]
  const fileName = file.name
  const fileNameWithoutExt = fileName.replace(/\.[^/.]+$/, "")
  
  // Create a URL for the file to read duration
  const fileUrl = URL.createObjectURL(file)
  
  // Create an audio element to read duration
  const audio = new Audio(fileUrl)
  
  audio.onloadedmetadata = () => {
    uploadForm.value = {
      title: fileNameWithoutExt,
      artist: 'Unknown Artist',
      isDummy: 0,
      filePath: file.name,
      metadata: {
        duration: audio.duration || 0,
        genre: '',
        year: new Date().getFullYear()
      }
    }
    
    // Clean up
    URL.revokeObjectURL(fileUrl)
  }
}

const submitUploadForm = async () => {
  try {
    error.value = null
    success.value = null
    
    if (!fileInput.value?.files?.length) {
      error.value = 'Please select a file to upload'
      return
    }

    const file = fileInput.value.files[0]
    const uploadedSong = await api.uploadFile(file)
    
    // Reset form
    uploadForm.value = {
      title: '',
      artist: '',
      isDummy: 0,
      metadata: {}
    }
    if (fileInput.value) {
      fileInput.value.value = ''
    }
    success.value = 'Song uploaded successfully!'
    emit('song-added')
  } catch (err: any) {
    if (err.response?.data?.detail) {
      const errorDetail = err.response.data.detail
      switch (errorDetail.error) {
        case 'INVALID_FILE_TYPE':
          error.value = errorDetail.message
          break
        case 'DUPLICATE_FILE':
          error.value = `${errorDetail.message} (${errorDetail.existing_song.title} by ${errorDetail.existing_song.artist})`
          break
        case 'UPLOAD_FAILED':
          error.value = errorDetail.message
          break
        default:
          error.value = 'Failed to upload song. Please try again.'
      }
    } else {
      error.value = 'Failed to upload song. Please try again.'
    }
    console.error('Upload error:', err)
  }
}
</script>

<template>
  <div class="bg-white rounded-lg shadow p-6 max-w-md mx-auto">
    <h2 class="text-2xl font-bold mb-4">Upload Song</h2>
    <form @submit.prevent="submitUploadForm" class="space-y-4">
      <FormMessage 
        :error="error"
        :success="success"
      />

      <div class="space-y-2">
        <label for="file" class="block text-sm font-medium text-gray-700">Upload Song</label>
        <input 
          type="file" 
          id="file" 
          ref="fileInput"
          accept="audio/*"
          @change="handleFileUpload"
          class="block w-full text-sm text-gray-500
                 file:mr-4 file:py-2 file:px-4
                 file:rounded-full file:border-0
                 file:text-sm file:font-semibold
                 file:bg-emerald-50 file:text-emerald-700
                 hover:file:bg-emerald-100"
        >
      </div>

      <div v-if="uploadForm.title" class="bg-gray-50 rounded-lg p-4 space-y-2">
        <p><strong>Title:</strong> {{ uploadForm.title }}</p>
        <p><strong>Artist:</strong> {{ uploadForm.artist }}</p>
        <p v-if="uploadForm.metadata.duration">
          <strong>Duration:</strong> {{ Math.floor(uploadForm.metadata.duration / 60) }}:{{ Math.floor(uploadForm.metadata.duration % 60).toString().padStart(2, '0') }}
        </p>
      </div>

      <button 
        type="submit" 
        :disabled="!uploadForm.title"
        class="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Upload Song
      </button>
    </form>
  </div>
</template>

<script lang="ts">
export default {
  name: 'FileUploadForm'
}
</script> 