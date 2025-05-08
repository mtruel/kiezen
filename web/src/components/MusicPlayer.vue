<script setup lang="ts">
import { ref, computed, watch, onUnmounted, nextTick } from 'vue'
import { type Song } from '../api'

const props = defineProps<{
  song: Song | null
  isPlaying: boolean
}>()

const emit = defineEmits<{
  (e: 'next'): void
  (e: 'previous'): void
  (e: 'update:isPlaying', value: boolean): void
}>()

const audio = ref<HTMLAudioElement | null>(null)
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
    currentTime.value = 0
    duration.value = 0
  }
  if (newSong) {
    nextTick(() => {
      if (audio.value) {
        audio.value.play().then(() => {
          emit('update:isPlaying', true)
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
        emit('update:isPlaying', true)
      }).catch(error => {
        console.error('Error playing audio:', error)
      })
    })
  }
})

watch(() => props.isPlaying, (newValue) => {
  if (!audio.value) return
  
  if (newValue) {
    audio.value.play()
  } else {
    audio.value.pause()
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
  emit('update:isPlaying', !props.isPlaying)
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
  emit('update:isPlaying', false)
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
            <rect x="3" y="5" width="2" height="14" rx="1" fill="currentColor" />
            <polygon points="5,12 19,5 19,19" fill="currentColor" />
          </svg>
        </button>
        
        <button @click="togglePlay" class="p-3 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
          <svg v-if="isPlaying" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <rect x="7" y="5" width="3" height="14" fill="currentColor" />
            <rect x="14" y="5" width="3" height="14" fill="currentColor" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <polygon points="6,4 20,12 6,20" fill="currentColor" />
          </svg>
        </button>

        <button @click="$emit('next')" class="p-2 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <rect x="19" y="5" width="2" height="14" rx="1" fill="currentColor" />
            <polygon points="19,12 5,5 5,19" fill="currentColor" />
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