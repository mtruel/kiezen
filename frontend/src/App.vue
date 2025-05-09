<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import SongList from './components/SongList.vue'
import AddSongForm from './components/AddSongForm.vue'
import MusicPlayer from './components/MusicPlayer.vue'
import { api, type Song } from './api'
import { usePlayerStore } from './stores/playerStore'
import { useSongStore } from './stores/songStore'

const activeTab = ref('songs')
const songListRef = ref<InstanceType<typeof SongList> | null>(null)
const showDebug = ref(false)
const consoleMessages = ref<Array<{ type: string; message: string; timestamp: string; source?: string }>>([])

const playerStore = usePlayerStore()
const songStore = useSongStore()

// Override console methods to capture messages
const originalConsole = {
  log: console.log,
  error: console.error,
  warn: console.warn,
  info: console.info,
  debug: console.debug
}

// Store messages in localStorage to persist across page reloads
const STORAGE_KEY = 'kiezen_console_messages'
const MAX_MESSAGES = 1000

// Add global error handler
window.addEventListener('error', (event) => {
  addMessage('error', event.message, 'window.onerror')
})

// Add unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
  addMessage('error', event.reason?.message || String(event.reason), 'unhandledrejection')
})

function addMessage(type: string, message: string, source?: string) {
  consoleMessages.value.push({
    type,
    message,
    timestamp: new Date().toISOString(),
    source
  })

  // Keep only the last MAX_MESSAGES messages
  if (consoleMessages.value.length > MAX_MESSAGES) {
    consoleMessages.value = consoleMessages.value.slice(-MAX_MESSAGES)
  }

  // Save to localStorage
  saveMessages()
}

function loadStoredMessages() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      consoleMessages.value = JSON.parse(stored)
    }
  } catch (e) {
    console.error('Failed to load stored console messages:', e)
  }
}

function saveMessages() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(consoleMessages.value))
  } catch (e) {
    console.error('Failed to save console messages:', e)
  }
}

function captureConsole(type: string) {
  return (...args: any[]) => {
    // Call original console method
    originalConsole[type as keyof typeof originalConsole](...args)
    
    // Format the message
    const message = args.map(arg => {
      if (typeof arg === 'object') {
        try {
          return JSON.stringify(arg, null, 2)
        } catch (e) {
          return String(arg)
        }
      }
      return String(arg)
    }).join(' ')

    addMessage(type, message)
  }
}

// Override console methods
console.log = captureConsole('log')
console.error = captureConsole('error')
console.warn = captureConsole('warn')
console.info = captureConsole('info')
console.debug = captureConsole('debug')

// Load stored messages on mount
loadStoredMessages()

// Clear console messages when debug panel is closed
watch(showDebug, (newValue) => {
  if (!newValue) {
    // Don't clear messages anymore, just hide the panel
  }
})

// Add a clear button
const clearConsole = () => {
  consoleMessages.value = []
  localStorage.removeItem(STORAGE_KEY)
}

// Debug information
const debugInfo = computed(() => ({
  currentSong: playerStore.currentSong,
  totalSongs: songStore.songs.length,
  activeTab: activeTab.value,
  timestamp: new Date().toISOString()
}))

const fetchSongs = async () => {
  await songStore.fetchSongs()
  playerStore.setQueue(songStore.songs)
}

const handleSongAdded = () => {
  fetchSongs()
}

const handleSongDeleted = (songId: string) => {
  playerStore.handleSongDeleted(songId)
}

const playSong = (song: Song) => {
  if (playerStore.currentSongId === song.id) {
    playerStore.togglePlay()
  } else {
    playerStore.playSong(song)
  }
}

// Initial fetch
fetchSongs()
</script>

<template>
  <div class="max-w-[1400px] mx-auto p-8 font-normal">
    <div v-if="showDebug" class="fixed bottom-4 right-4 w-96 h-96 bg-gray-800 text-white rounded-lg shadow-lg overflow-hidden">
      <div class="flex justify-between items-center p-2 bg-gray-700">
        <button @click="clearConsole" class="px-2 py-1 text-sm bg-red-600 hover:bg-red-700 rounded">Clear Console</button>
        <button @click="showDebug = false" class="text-xl hover:text-gray-300">×</button>
      </div>
      <div class="h-[calc(100%-2.5rem)] overflow-y-auto p-2 font-mono text-sm">
        <div v-for="(msg, index) in consoleMessages" :key="index" :class="['mb-1', {
          'text-red-400': msg.type === 'error',
          'text-yellow-400': msg.type === 'warn',
          'text-blue-400': msg.type === 'info',
          'text-gray-400': msg.type === 'debug'
        }]">
          <span class="text-gray-500">{{ new Date(msg.timestamp).toLocaleTimeString() }}</span>
          <span v-if="msg.source" class="text-gray-400 ml-1">[{{ msg.source }}]</span>
          <span class="ml-1">{{ msg.message }}</span>
        </div>
      </div>
    </div>
    <button v-else @click="showDebug = true" class="fixed bottom-4 right-4 px-3 py-1 bg-gray-800 text-white rounded hover:bg-gray-700">Debug</button>
    
    <header class="mb-8">
      <h1 class="text-3xl font-bold">Kiezen - DJ Song Manager</h1>
    </header>

    <main>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="form-column lg:col-span-1">
          <AddSongForm @song-added="handleSongAdded" />
        </div>
        <div class="content-column lg:col-span-2">
          <SongList 
            ref="songListRef" 
            :current-song="playerStore.currentSong"
            :is-playing="playerStore.isPlaying"
            @play-song="playSong"
            @song-deleted="handleSongDeleted"
          />
        </div>
      </div>
    </main>

    <MusicPlayer 
      :song="playerStore.currentSong" 
      v-model:is-playing="playerStore.isPlaying"
      @next="playerStore.playNext"
      @previous="playerStore.playPrevious"
    />
  </div>
</template>

<style>
/* Remove all custom CSS as we're using Tailwind now */
</style>
