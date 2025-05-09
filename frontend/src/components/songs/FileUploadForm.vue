<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { api } from '../../api'
import { useSongStore } from '../../stores/songStore'
import FormMessage from '../common/FormMessage.vue'

const emit = defineEmits<{
  (e: 'song-added'): void
}>()

const songStore = useSongStore()
const error = ref<string | null>(null)
const success = ref<string | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFiles = ref<File[]>([])
const uploadProgress = ref<{ [key: string]: { progress: number, status: 'uploading' | 'success' | 'error', message?: string } }>({})
const isUploading = ref(false)
let notificationTimeout: number | null = null
const showSuccessAccordion = ref(false)
const showErrorAccordion = ref(true)

type UploadResult = {
  filename: string
  progress: number
  status: 'success' | 'error'
  message?: string
}

const getUploadResults = computed(() => {
  const results = {
    success: [] as UploadResult[],
    error: [] as UploadResult[]
  }
  
  Object.entries(uploadProgress.value).forEach(([filename, data]) => {
    if (data.status === 'success') {
      results.success.push({
        filename,
        progress: data.progress,
        status: 'success'
      })
    } else if (data.status === 'error') {
      results.error.push({
        filename,
        progress: data.progress,
        status: 'error',
        message: data.message
      })
    }
  })
  
  return results
})

const uploadingFiles = computed(() => {
  return Object.entries(uploadProgress.value)
    .filter(([_, data]) => data.status === 'uploading')
    .map(([filename, data]) => ({
      filename,
      progress: data.progress
    }))
})

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files) {
    selectedFiles.value = Array.from(input.files)
    // Initialize progress for each file
    selectedFiles.value.forEach(file => {
      uploadProgress.value[file.name] = {
        progress: 0,
        status: 'uploading'
      }
    })
  }
}

const handleUploadProgress = (event: CustomEvent) => {
  // Update progress for all files being uploaded
  Object.keys(uploadProgress.value).forEach(filename => {
    if (uploadProgress.value[filename].status === 'uploading') {
      uploadProgress.value[filename].progress = event.detail.progress
    }
  })
}

const clearNotifications = () => {
  error.value = null
  success.value = null
  if (notificationTimeout) {
    clearTimeout(notificationTimeout)
    notificationTimeout = null
  }
}

const showNotification = (type: 'success' | 'error', message: string) => {
  clearNotifications()
  if (type === 'success') {
    success.value = message
  } else {
    error.value = message
  }
  notificationTimeout = window.setTimeout(() => {
    clearNotifications()
  }, 5000)
}

const submitUploadForm = async () => {
  if (!selectedFiles.value.length) return

  isUploading.value = true
  try {
    clearNotifications()

    const result = await api.uploadFiles(selectedFiles.value)
    
    // Update progress for each file by original filename
    result.uploaded_songs.forEach(song => {
      // Find the original file by matching filePath to file.name (assuming backend returns original filename in filePath)
      const originalFile = selectedFiles.value.find(f => f.name === song.filePath || f.name === song.title || song.filePath?.endsWith(f.name))
      const key = originalFile ? originalFile.name : song.filePath || ''
      if (uploadProgress.value[key]) {
        uploadProgress.value[key] = {
          progress: 100,
          status: 'success'
        }
      }
    })

    // Handle errors
    result.errors.forEach(error => {
      if (uploadProgress.value[error.filename]) {
        uploadProgress.value[error.filename] = {
          progress: 100,
          status: 'error',
          message: error.message
        }
      }
    })

    // Refresh the song list
    await songStore.fetchSongs()
    
    // Clear the form
    if (fileInput.value) {
      fileInput.value.value = ''
    }
    selectedFiles.value = []
    
    // Show success message if any files were uploaded
    if (result.uploaded_songs.length > 0) {
      showNotification('success', `Successfully uploaded ${result.uploaded_songs.length} song${result.uploaded_songs.length > 1 ? 's' : ''}`)
      emit('song-added')
    }

    // Show error message if any files failed
    if (result.errors.length > 0) {
      showNotification('error', `Failed to upload ${result.errors.length} file${result.errors.length > 1 ? 's' : ''}`)
    }

    // Ensure all completed uploads are marked as success
    Object.entries(uploadProgress.value).forEach(([filename, data]) => {
      if (data.status === 'uploading' && data.progress === 100) {
        uploadProgress.value[filename].status = 'success'
      }
    })
  } catch (err: any) {
    showNotification('error', 'Failed to upload songs. Please try again.')
    console.error('Upload error:', err)
    // Mark all files as failed
    Object.keys(uploadProgress.value).forEach(filename => {
      uploadProgress.value[filename] = {
        progress: 100,
        status: 'error',
        message: 'Upload failed'
      }
    })
  } finally {
    isUploading.value = false
  }
}

const clearHistory = () => {
  uploadProgress.value = {}
  selectedFiles.value = []
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  clearNotifications()
}

// Add event listeners for upload progress
onMounted(() => {
  window.addEventListener('upload-progress', handleUploadProgress as EventListener)
})

onUnmounted(() => {
  window.removeEventListener('upload-progress', handleUploadProgress as EventListener)
  if (notificationTimeout) {
    clearTimeout(notificationTimeout)
  }
})
</script>

<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Upload Songs</h2>
      <button
        v-if="Object.keys(uploadProgress).length > 0"
        @click="clearHistory"
        class="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded hover:bg-gray-200 transition-colors"
      >
        Clear History
      </button>
    </div>
    
    <FormMessage 
      :error="error"
      :success="success"
    />
    
    <!-- File input -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Select Music Files
      </label>
      <input
        type="file"
        ref="fileInput"
        @change="handleFileUpload"
        accept="audio/*"
        multiple
        class="block w-full text-sm text-gray-500
          file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0
          file:text-sm file:font-semibold
          file:bg-violet-50 file:text-violet-700
          hover:file:bg-violet-100"
      />
    </div>

    <!-- Upload progress -->
    <div v-if="Object.keys(uploadProgress).length > 0" class="space-y-4">
      <!-- Files being uploaded -->
      <div v-for="file in uploadingFiles" :key="file.filename" 
           class="bg-gray-50 rounded-lg p-4">
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-medium text-gray-700">{{ file.filename }}</span>
          <span class="text-sm text-gray-500">{{ file.progress }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="h-2 rounded-full transition-all duration-300 bg-blue-600"
            :style="{ width: `${file.progress}%` }"
          ></div>
        </div>
      </div>

      <!-- Failed uploads accordion -->
      <div v-if="getUploadResults.error.length > 0" class="border rounded-lg overflow-hidden">
        <button
          @click="showErrorAccordion = !showErrorAccordion"
          class="w-full px-4 py-2 bg-red-50 text-red-700 flex justify-between items-center hover:bg-red-100 transition-colors"
        >
          <span class="font-medium">Failed Uploads ({{ getUploadResults.error.length }})</span>
          <svg
            class="w-5 h-5 transform transition-transform"
            :class="{ 'rotate-180': showErrorAccordion }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="showErrorAccordion" class="p-4 space-y-4">
          <div v-for="file in getUploadResults.error" :key="file.filename" class="bg-red-50 rounded-lg p-4">
            <div class="flex justify-between items-center mb-2">
              <span class="text-sm font-medium text-red-700">{{ file.filename }}</span>
              <span class="text-sm text-red-500">Failed</span>
            </div>
            <div class="w-full bg-red-200 rounded-full h-2">
              <div class="h-2 rounded-full bg-red-600" style="width: 100%"></div>
            </div>
            <div class="mt-2 text-sm text-red-600">
              {{ file.message }}
            </div>
          </div>
        </div>
      </div>

      <!-- Successful uploads accordion -->
      <div v-if="getUploadResults.success.length > 0" class="border rounded-lg overflow-hidden">
        <button
          @click="showSuccessAccordion = !showSuccessAccordion"
          class="w-full px-4 py-2 bg-green-50 text-green-700 flex justify-between items-center hover:bg-green-100 transition-colors"
        >
          <span class="font-medium">Successful Uploads ({{ getUploadResults.success.length }})</span>
          <svg
            class="w-5 h-5 transform transition-transform"
            :class="{ 'rotate-180': showSuccessAccordion }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="showSuccessAccordion" class="p-4 space-y-4">
          <div v-for="file in getUploadResults.success" :key="file.filename" class="bg-green-50 rounded-lg p-4">
            <div class="flex justify-between items-center mb-2">
              <span class="text-sm font-medium text-green-700">{{ file.filename }}</span>
              <span class="text-sm text-green-500">Success</span>
            </div>
            <div class="w-full bg-green-200 rounded-full h-2">
              <div class="h-2 rounded-full bg-green-600" style="width: 100%"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload button -->
    <button
      @click="submitUploadForm"
      :disabled="!selectedFiles.length || isUploading"
      class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed mt-6"
    >
      {{ isUploading ? 'Uploading...' : 'Upload Songs' }}
    </button>
  </div>
</template>

<script lang="ts">
export default {
  name: 'FileUploadForm'
}
</script> 