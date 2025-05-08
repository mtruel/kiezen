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
        <button @click="handlePrevious" class="text-2xl hover:text-gray-300 transition-colors">
          ⏮
        </button>
        
        <button @click="togglePlay" class="text-3xl hover:text-gray-300 transition-colors">
          {{ isPlaying ? '⏸' : '▶' }}
        </button>

        <button @click="$emit('next')" class="text-2xl hover:text-gray-300 transition-colors">
          ⏭
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