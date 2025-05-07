<script setup lang="ts">
import { ref, computed, watch, onUnmounted, nextTick } from 'vue'
import { type Song } from '../api'

const props = defineProps<{
  song: Song | null
}>()

const audio = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)

const audioUrl = computed(() => {
  if (!props.song) return ''
  if (props.song.isDummy && props.song.url) {
    return props.song.url
  }
  if (props.song.filePath) {
    return `http://localhost:8000/music/${props.song.filePath}`
  }
  return ''
})

const cleanup = () => {
  if (audio.value) {
    audio.value.pause()
    audio.value.src = ''
    audio.value.load()
  }
}

watch(() => props.song, (newSong, oldSong) => {
  if (oldSong && newSong && oldSong.id !== newSong.id) {
    cleanup()
    isPlaying.value = false
    currentTime.value = 0
    duration.value = 0
  }
  if (newSong) {
    nextTick(() => {
      if (audio.value) {
        audio.value.play().then(() => {
          isPlaying.value = true
        }).catch(error => {
          console.error('Error playing audio:', error)
        })
      }
    })
  }
})

watch(() => audioUrl.value, (newUrl) => {
  if (newUrl && audio.value) {
    nextTick(() => {
      audio.value.play().then(() => {
        isPlaying.value = true
      }).catch(error => {
        console.error('Error playing audio:', error)
      })
    })
  }
})

onUnmounted(() => {
  cleanup()
})

const formattedTime = (time: number) => {
  const minutes = Math.floor(time / 60)
  const seconds = Math.floor(time % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

const togglePlay = () => {
  if (!audio.value) return
  
  if (isPlaying.value) {
    audio.value.pause()
  } else {
    audio.value.play()
  }
  isPlaying.value = !isPlaying.value
}

const handleTimeUpdate = () => {
  if (!audio.value) return
  currentTime.value = audio.value.currentTime
}

const handleLoadedMetadata = () => {
  if (!audio.value) return
  duration.value = audio.value.duration
}

const handleEnded = () => {
  isPlaying.value = false
  currentTime.value = 0
}

const seek = (event: Event) => {
  if (!audio.value) return
  const target = event.target as HTMLInputElement
  const time = parseFloat(target.value)
  audio.value.currentTime = time
  currentTime.value = time
}

const restart = () => {
  if (!audio.value) return
  audio.value.currentTime = 0
  currentTime.value = 0
}

const emit = defineEmits<{
  (e: 'next'): void
  (e: 'previous'): void
}>()

const handlePrevious = () => {
  if (currentTime.value > 3) {
    restart()
  } else {
    emit('previous')
  }
}
</script>

<template>
  <div class="music-player" v-if="song">
    <div class="player-content">
      <div class="player-info">
        <h3>{{ song.title }}</h3>
        <p>{{ song.artist }}</p>
      </div>

      <audio
        ref="audio"
        :src="audioUrl"
        @timeupdate="handleTimeUpdate"
        @loadedmetadata="handleLoadedMetadata"
        @ended="handleEnded"
      ></audio>

      <div class="player-controls">
        <button @click="handlePrevious" class="control-btn">
          ⏮
        </button>
        
        <button @click="togglePlay" class="play-btn">
          {{ isPlaying ? '⏸' : '▶' }}
        </button>

        <button @click="$emit('next')" class="control-btn">
          ⏭
        </button>

        <div class="progress-container">
          <span class="time">{{ formattedTime(currentTime) }}</span>
          <input
            type="range"
            :min="0"
            :max="duration"
            :value="currentTime"
            @input="seek"
            class="progress-bar"
          >
          <span class="time">{{ formattedTime(duration) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.music-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #2c3e50;
  color: white;
  padding: 1rem;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.player-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.player-info {
  min-width: 200px;
}

.player-info h3 {
  margin: 0;
  font-size: 1.1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-info p {
  margin: 0.25rem 0 0;
  color: #a0aec0;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-controls {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.control-btn {
  background: transparent;
  color: white;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.play-btn {
  background: #42b983;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.play-btn:hover {
  background: #3aa876;
}

.progress-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-bar {
  flex: 1;
  height: 4px;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  outline: none;
}

.progress-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 12px;
  height: 12px;
  background: #42b983;
  border-radius: 50%;
  cursor: pointer;
}

.time {
  font-size: 0.8rem;
  color: #a0aec0;
  min-width: 40px;
}
</style>

<script lang="ts">
export default {
  name: 'MusicPlayer'
}
</script> 