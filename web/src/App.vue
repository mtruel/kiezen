<script setup lang="ts">
import { ref, computed } from 'vue'
import SongList from './components/SongList.vue'
import AddSongForm from './components/AddSongForm.vue'
import MusicPlayer from './components/MusicPlayer.vue'
import { api, type Song } from './api'

const activeTab = ref('songs')
const songListRef = ref<InstanceType<typeof SongList> | null>(null)
const songs = ref<Song[]>([])
const currentSong = ref<Song | null>(null)
const currentSongIndex = ref(-1)

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
</style>
