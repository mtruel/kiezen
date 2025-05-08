<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import SongList from './components/SongList.vue'
import AddSongForm from './components/AddSongForm.vue'
import MusicPlayer from './components/MusicPlayer.vue'
import { api, type Song } from './api'

const activeTab = ref('songs')
const songListRef = ref<InstanceType<typeof SongList> | null>(null)
const songs = ref<Song[]>([])
const currentSong = ref<Song | null>(null)
const currentSongIndex = ref(-1)
const showDebug = ref(false)
const consoleMessages = ref<Array<{ type: string; message: string; timestamp: string; source?: string }>>([])

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
  currentSong: currentSong.value,
  totalSongs: songs.value.length,
  activeTab: activeTab.value,
  timestamp: new Date().toISOString()
}))

const fetchSongs = async () => {
  songs.value = await api.getSongs()
}

const handleSongAdded = () => {
  fetchSongs()
  songListRef.value?.fetchSongs()
}

const playSong = (song: Song) => {
  currentSong.value = song
  currentSongIndex.value = songs.value.findIndex(s => s.id === song.id)
}

const playNext = () => {
  let nextIndex = currentSongIndex.value + 1
  while (nextIndex < songs.value.length && songs.value[nextIndex].isDummy === 1) {
    nextIndex++
  }
  if (nextIndex < songs.value.length) {
    currentSongIndex.value = nextIndex
    currentSong.value = songs.value[currentSongIndex.value]
  }
}

const playPrevious = () => {
  let prevIndex = currentSongIndex.value - 1
  while (prevIndex >= 0 && songs.value[prevIndex].isDummy === 1) {
    prevIndex--
  }
  if (prevIndex >= 0) {
    currentSongIndex.value = prevIndex
    currentSong.value = songs.value[currentSongIndex.value]
  }
}

// Initial fetch
fetchSongs()
</script>

<template>
  <div class="app">
    <div v-if="showDebug" class="debug-panel">
      <div class="console-header">
        <button @click="clearConsole" class="clear-btn">Clear Console</button>
        <button @click="showDebug = false" class="debug-close">×</button>
      </div>
      <div class="console-output">
        <div v-for="(msg, index) in consoleMessages" :key="index" :class="['console-line', msg.type]">
          <span class="timestamp">{{ new Date(msg.timestamp).toLocaleTimeString() }}</span>
          <span v-if="msg.source" class="source">[{{ msg.source }}]</span>
          <span class="message">{{ msg.message }}</span>
        </div>
      </div>
    </div>
    <button v-else @click="showDebug = true" class="debug-toggle">Debug</button>
    
    <header>
      <h1>Kiezen - DJ Song Manager</h1>
    </header>

    <main>
      <div class="layout">
        <div class="form-column">
          <AddSongForm @song-added="handleSongAdded" />
        </div>
        <div class="content-column">
          <SongList ref="songListRef" @play-song="playSong" />
        </div>
      </div>
    </main>

    <MusicPlayer 
      :song="currentSong" 
      @next="playNext"
      @previous="playPrevious"
    />
  </div>
</template>

<style>
.app {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  padding-bottom: 6rem; /* Add space for the player */
}

header {
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

main {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

.form-column {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.content-column {
  min-width: 0; /* Prevents overflow in grid */
}

.debug-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.95);
  color: #fff;
  padding: 1rem;
  font-family: monospace;
  z-index: 9999;
  max-height: 300px;
  overflow-y: auto;
}

.console-header {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.clear-btn {
  background: #666;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  font-size: 0.8rem;
}

.clear-btn:hover {
  background: #777;
}

.console-output {
  font-size: 0.9rem;
  line-height: 1.4;
}

.console-line {
  margin: 0.25rem 0;
  padding: 0.25rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  word-break: break-word;
}

.console-line .timestamp {
  color: #888;
  margin-right: 0.5rem;
  font-size: 0.8rem;
}

.console-line.log {
  color: #fff;
}

.console-line.error {
  color: #ff6b6b;
}

.console-line.warn {
  color: #ffd93d;
}

.console-line.info {
  color: #4dabf7;
}

.console-line.debug {
  color: #a0aec0;
}

.console-line .source {
  color: #888;
  margin-right: 0.5rem;
  font-size: 0.8rem;
  font-style: italic;
}

.debug-close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  color: #42b983;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
}

.debug-toggle {
  position: fixed;
  top: 1rem;
  right: 1rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  z-index: 9998;
}

.debug-toggle:hover {
  background: #3aa876;
}
</style>
