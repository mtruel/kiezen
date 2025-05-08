<script setup lang="ts">
import { ref, computed, watch, onUnmounted, nextTick } from 'vue'
import { type Song } from '../api'
import { 
  BackwardIcon, 
  ForwardIcon, 
  PlayIcon, 
  PauseIcon, 
  SpeakerWaveIcon, 
  SpeakerXMarkIcon 
} from '@heroicons/vue/24/solid'

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
const volume = ref(1)
const isMuted = ref(false)
const previousVolume = ref(1)

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

watch(volume, (val) => {
  if (audio.value) {
    audio.value.volume = val
    if (val === 0) {
      isMuted.value = true
      audio.value.muted = true
    } else {
      isMuted.value = false
      audio.value.muted = false
    }
  }
})

watch(isMuted, (val) => {
  if (audio.value) {
    audio.value.muted = val
    if (val) {
      audio.value.volume = 0
    } else {
      audio.value.volume = volume.value || 1
    }
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

const setVolume = (val: number) => {
  if (val > 0) {
    previousVolume.value = val
  }
  volume.value = val
  if (audio.value) {
    audio.value.volume = val
    if (val === 0) {
      isMuted.value = true
      audio.value.muted = true
    } else {
      isMuted.value = false
      audio.value.muted = false
    }
  }
}

const toggleMute = () => {
  if (!isMuted.value) {
    // Muting: save current volume if not zero
    if (volume.value > 0) {
      previousVolume.value = volume.value
    }
    isMuted.value = true
    volume.value = 0
    if (audio.value) {
      audio.value.muted = true
      audio.value.volume = 0
    }
  } else {
    // Unmuting: restore previous volume
    isMuted.value = false
    volume.value = previousVolume.value || 1
    if (audio.value) {
      audio.value.muted = false
      audio.value.volume = volume.value
    }
  }
}

const handleVolumeInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  setVolume(parseFloat(target.value))
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
          <BackwardIcon class="h-6 w-6" />
        </button>
        
        <button @click="togglePlay" class="p-3 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
          <PauseIcon v-if="isPlaying" class="h-8 w-8" />
          <PlayIcon v-else class="h-8 w-8" />
        </button>

        <button @click="$emit('next')" class="p-2 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
          <ForwardIcon class="h-6 w-6" />
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
        <!-- Volume control -->
        <div class="flex items-center gap-2 ml-auto">
          <button @click="toggleMute" class="p-2 flex items-center justify-center rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
            <SpeakerXMarkIcon v-if="isMuted || volume === 0" class="h-6 w-6" />
            <SpeakerWaveIcon v-else class="h-6 w-6" />
          </button>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            :value="isMuted ? 0 : volume"
            @input="handleVolumeInput"
            class="h-1 w-24 bg-gray-600 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-white"
          >
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