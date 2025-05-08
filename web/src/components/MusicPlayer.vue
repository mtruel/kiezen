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
  <div v-if="song" class="fixed bottom-0 left-0 right-0 bg-slate-800 text-white p-4 shadow-lg z-50">
    <div class="max-w-[1400px] mx-auto flex items-center gap-8">
      <div class="min-w-[200px]">
        <h3 class="text-lg font-semibold">{{ song.title }}</h3>
        <p class="text-gray-300">{{ song.artist }}</p>
      </div>

      <audio
        ref="audio"
        :src="audioUrl"
        @timeupdate="handleTimeUpdate"
        @loadedmetadata="handleLoadedMetadata"
        @ended="handleEnded"
      ></audio>

      <div class="flex-1 flex items-center gap-4">
        <button @click="handlePrevious" class="p-2 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          </svg>
        </button>
        
        <button @click="togglePlay" class="p-3 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
          <svg v-if="isPlaying" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>

        <button @click="$emit('next')" class="p-2 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
          </svg>
        </button>

        <div class="flex-1 flex items-center gap-2">
          <span class="text-sm text-gray-400">{{ formattedTime(currentTime) }}</span>
          <input
            type="range"
            :min="0"
            :max="duration"
            :value="currentTime"
            @input="seek"
            class="flex-1 h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-white"
          >
          <span class="text-sm text-gray-400">{{ formattedTime(duration) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Remove all custom CSS as we're using Tailwind now */
</style>

<script lang="ts">
export default {
  name: 'MusicPlayer'
}
</script> 