<script setup lang="ts">
import { ref, computed } from 'vue'
import { api, type Song } from '../api'

const dummyForm = ref<Omit<Song, 'id'>>({
  title: '',
  artist: '',
  isDummy: true,
  metadata: {}
})

const uploadForm = ref<Omit<Song, 'id'>>({
  title: '',
  artist: '',
  isDummy: false,
  metadata: {}
})

const error = ref<string | null>(null)
const success = ref<string | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

// Computed property to check if at least one field is filled
const isDummyFormValid = computed(() => {
  return dummyForm.value.title.trim() !== '' || 
         dummyForm.value.artist.trim() !== '' || 
         dummyForm.value.url?.trim() !== '' ||
         dummyForm.value.metadata.genre?.trim() !== '' ||
         dummyForm.value.metadata.year !== undefined
})

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
    // For now, use filename as title and unknown artist
    // In a real application, you would use a library like music-metadata
    // to properly read ID3 tags and other metadata
    uploadForm.value = {
      title: fileNameWithoutExt,
      artist: 'Unknown Artist',
      isDummy: false,
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

const submitDummyForm = async () => {
  try {
    error.value = null
    success.value = null
    
    await api.createSong(dummyForm.value)
    
    // Reset form
    dummyForm.value = {
      title: '',
      artist: '',
      isDummy: true,
      metadata: {}
    }
    success.value = 'Dummy song added successfully!'
  } catch (err) {
    error.value = 'Failed to add dummy song. Please try again.'
    console.error(err)
  }
}

const submitUploadForm = async () => {
  try {
    error.value = null
    success.value = null
    
    await api.createSong(uploadForm.value)
    
    // Reset form
    uploadForm.value = {
      title: '',
      artist: '',
      isDummy: false,
      metadata: {}
    }
    if (fileInput.value) {
      fileInput.value.value = ''
    }
    success.value = 'Song uploaded successfully!'
  } catch (err) {
    error.value = 'Failed to upload song. Please try again.'
    console.error(err)
  }
}
</script>

<script lang="ts">
export default {
  name: 'AddSongForm'
}
</script>

<template>
  <div class="add-song-form">
    <div class="form-section">
      <h2>Upload Song</h2>
      <form @submit.prevent="submitUploadForm">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div v-if="success" class="success-message">
          {{ success }}
        </div>

        <div class="form-group">
          <label for="file">Upload Song</label>
          <input 
            type="file" 
            id="file" 
            ref="fileInput"
            accept="audio/*"
            @change="handleFileUpload"
          >
        </div>

        <div v-if="uploadForm.title" class="preview-info">
          <p><strong>Title:</strong> {{ uploadForm.title }}</p>
          <p><strong>Artist:</strong> {{ uploadForm.artist }}</p>
          <p v-if="uploadForm.metadata.duration">
            <strong>Duration:</strong> {{ Math.floor(uploadForm.metadata.duration / 60) }}:{{ Math.floor(uploadForm.metadata.duration % 60).toString().padStart(2, '0') }}
          </p>
        </div>

        <button type="submit" class="submit-btn" :disabled="!uploadForm.title">Upload Song</button>
      </form>
    </div>

    <div class="form-section">
      <h2>Add Dummy Song</h2>
      <form @submit.prevent="submitDummyForm">
        <div class="form-group">
          <label for="dummy-title">Title</label>
          <input 
            type="text" 
            id="dummy-title" 
            v-model="dummyForm.title" 
          >
        </div>

        <div class="form-group">
          <label for="dummy-artist">Artist</label>
          <input 
            type="text" 
            id="dummy-artist" 
            v-model="dummyForm.artist" 
          >
        </div>

        <div class="form-group">
          <label for="dummy-url">URL</label>
          <input 
            type="url" 
            id="dummy-url" 
            v-model="dummyForm.url"
          >
        </div>

        <div class="form-group">
          <label for="dummy-genre">Genre</label>
          <input 
            type="text" 
            id="dummy-genre" 
            v-model="dummyForm.metadata.genre"
          >
        </div>

        <div class="form-group">
          <label for="dummy-year">Year</label>
          <input 
            type="number" 
            id="dummy-year" 
            v-model="dummyForm.metadata.year"
          >
        </div>

        <button type="submit" class="submit-btn" :disabled="!isDummyFormValid">Add Dummy Song</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.add-song-form {
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.form-section {
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-section:last-child {
  margin-bottom: 0;
}

h2 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input[type="text"],
input[type="url"],
input[type="number"],
input[type="file"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

input::placeholder {
  color: #999;
  font-style: italic;
}

.preview-info {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.preview-info p {
  margin: 0.5rem 0;
}

.submit-btn {
  background-color: #42b983;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
}

.submit-btn:hover {
  background-color: #3aa876;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
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