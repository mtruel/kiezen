import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Song } from '../api'

export const usePlayerStore = defineStore('player', () => {
  const currentSongId = ref<string | null>(null)
  const queue = ref<Song[]>([])
  const history = ref<string[]>([])
  const isPlaying = ref(false)
  const repeatMode = ref<'none' | 'one' | 'all'>('none')
  const shuffle = ref(false)
  const playedHistory = ref<Set<string>>(new Set())

  const currentSong = computed(() => {
    if (!currentSongId.value) return null
    return queue.value.find(song => song.id === currentSongId.value)
  })

  function findNextValidSong(currentIndex: number): Song | null {
    let nextIndex = currentIndex + 1
    
    while (nextIndex < queue.value.length) {
      const nextSong = queue.value[nextIndex]
      if (nextSong && queue.value.some(s => s.id === nextSong.id)) {
        return nextSong
      }
      nextIndex++
    }
    
    if (repeatMode.value === 'all' && queue.value.length > 0) {
      return queue.value[0]
    }
    
    return null
  }

  function playSong(song: Song) {
    currentSongId.value = song.id
    isPlaying.value = true
    history.value.push(song.id)
    markAsPlayed(song.id)
  }

  function playNext() {
    const currentIndex = queue.value.findIndex(song => song.id === currentSongId.value)
    const nextSong = findNextValidSong(currentIndex)
    if (nextSong) {
      playSong(nextSong)
    } else {
      isPlaying.value = false
      currentSongId.value = null
    }
  }

  function playPrevious() {
    const currentIndex = queue.value.findIndex(song => song.id === currentSongId.value)
    if (currentIndex > 0) {
      let prevIndex = currentIndex - 1
      while (prevIndex >= 0) {
        const prevSong = queue.value[prevIndex]
        if (prevSong && queue.value.some(s => s.id === prevSong.id)) {
          playSong(prevSong)
          return
        }
        prevIndex--
      }
    }
  }

  function togglePlay() {
    isPlaying.value = !isPlaying.value
  }

  function setQueue(songs: Song[]) {
    queue.value = songs
  }

  function handleSongDeleted(songId: string) {
    if (currentSongId.value === songId) {
      const currentIndex = queue.value.findIndex(song => song.id === songId)
      const nextSong = findNextValidSong(currentIndex)
      if (nextSong) {
        playSong(nextSong)
      } else {
        isPlaying.value = false
        currentSongId.value = null
      }
    }
    queue.value = queue.value.filter(song => song.id !== songId)
  }

  function markAsPlayed(songId: string) {
    playedHistory.value.add(songId)
  }

  function isPlayed(songId: string): boolean {
    return playedHistory.value.has(songId)
  }

  return {
    currentSongId,
    queue,
    history,
    isPlaying,
    repeatMode,
    shuffle,
    currentSong,
    playedHistory,
    playSong,
    playNext,
    playPrevious,
    togglePlay,
    setQueue,
    handleSongDeleted,
    isPlayed
  }
}) 