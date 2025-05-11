<script setup lang="ts">
import { ref, computed, watch, onUnmounted, nextTick, onMounted } from 'vue'
import { type Song } from '../api'
import { 
  BackwardIcon, 
  ForwardIcon, 
  PlayIcon, 
  PauseIcon, 
  SpeakerWaveIcon, 
  SpeakerXMarkIcon,
  QueueListIcon,
  XMarkIcon,
  ChevronUpIcon,
  ChevronDownIcon,
  TagIcon
} from '@heroicons/vue/24/solid'
import { usePlayerStore } from '../stores/playerStore'

const props = defineProps<{
  song: Song | null
  isPlaying: boolean
}>()

const emit = defineEmits<{
  (e: 'next'): void
  (e: 'previous'): void
  (e: 'update:isPlaying', value: boolean): void
}>()

const playerStore = usePlayerStore()
const showQueue = ref(false)
const showTagPanel = ref(false)
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
    return `http://localhost:8000/music/music_files/${props.song.filePath}`
  }
  return ''
})

const cleanup = () => {
  if (audio.value) {
    audio.value.pause()
    audio.value.src = ''
    audio.value.load()
    audio.value.currentTime = 0
    duration.value = 0
    currentTime.value = 0
  }
}

watch(() => props.song, (newSong, oldSong) => {
  if (!newSong) {
    cleanup()
    return
  }
  if (oldSong && newSong && oldSong.id !== newSong.id) {
    cleanup()
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

watch(() => props.isPlaying, (newValue) => {
  if (!audio.value) return
  
  if (newValue) {
    audio.value.play()
  } else {
    audio.value.pause()
  }
})

// Load saved volume on component mount
const loadSavedVolume = () => {
  try {
    const savedVolume = localStorage.getItem('musicPlayerVolume')
    const savedMute = localStorage.getItem('musicPlayerMuted')
    
    if (savedVolume !== null) {
      const parsedVolume = parseFloat(savedVolume)
      // Ensure the volume is between 0 and 1
      if (!isNaN(parsedVolume) && parsedVolume >= 0 && parsedVolume <= 1) {
        volume.value = parsedVolume
      }
    }
    
    if (savedMute !== null) {
      isMuted.value = savedMute === 'true'
    }
  } catch (error) {
    console.warn('Failed to load saved volume settings:', error)
  }
}

// Apply volume settings to audio element
const applyVolumeSettings = () => {
  if (audio.value) {
    audio.value.volume = volume.value
    audio.value.muted = isMuted.value
  }
}

// Watch for audio element creation
watch(audio, (newAudio) => {
  if (newAudio) {
    applyVolumeSettings()
  }
})

// Save volume when it changes
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
    try {
      localStorage.setItem('musicPlayerVolume', val.toString())
    } catch (error) {
      console.warn('Failed to save volume setting:', error)
    }
  }
})

// Save mute state when it changes
watch(isMuted, (val) => {
  if (audio.value) {
    audio.value.muted = val
  }
  try {
    localStorage.setItem('musicPlayerMuted', val.toString())
  } catch (error) {
    console.warn('Failed to save mute setting:', error)
  }
})

// Call loadSavedVolume when component is mounted
onMounted(() => {
  loadSavedVolume()
})

watch(() => props.isPlaying, (newValue) => {
  if (!audio.value) return
  
  if (newValue) {
    audio.value.play()
  } else {
    audio.value.pause()
  }
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
  playerStore.playNext()
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

const removeFromQueue = (songId: string) => {
  const currentIndex = playerStore.queue.findIndex(song => song.id === songId)
  if (currentIndex !== -1) {
    const newQueue = [...playerStore.queue]
    newQueue.splice(currentIndex, 1)
    playerStore.setQueue(newQueue)
  }
}

const playFromQueue = (song: Song) => {
  playerStore.playSong(song)
}
</script>

<template>
  <div class="fixed bottom-0 left-0 right-0">
    <!-- Tag Edition Panel -->
    <div v-if="showTagPanel" class="bg-slate-900 border-t border-slate-700">
      <div class="max-w-[1400px] mx-auto">
        <div class="p-4 border-b border-slate-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold">Edit Metadata</h3>
          <button @click="showTagPanel = false" class="p-1 hover:bg-slate-700 rounded-full transition-colors">
            <XMarkIcon class="h-5 w-5" />
          </button>
        </div>
        <div class="p-4">
          <div class="grid grid-cols-2 gap-6">
            <!-- Left Column -->
            <div class="space-y-4">
              <!-- Basic Info -->
              <div class="space-y-4">
                <h4 class="text-sm font-medium text-gray-300">Basic Information</h4>
                <div class="space-y-3">
                  <div>
                    <label class="block text-sm font-medium text-gray-400 mb-1">Title</label>
                    <input 
                      type="text" 
                      class="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      :value="song?.title"
                      placeholder="Song title"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-400 mb-1">Artist</label>
                    <input 
                      type="text" 
                      class="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      :value="song?.artist"
                      placeholder="Artist name"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-400 mb-1">Album</label>
                    <input 
                      type="text" 
                      class="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      :value="song?.album"
                      placeholder="Album name"
                    >
                  </div>
                </div>
              </div>

              <!-- Additional Info -->
              <div class="space-y-4">
                <h4 class="text-sm font-medium text-gray-300">Additional Information</h4>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-sm font-medium text-gray-400 mb-1">Year</label>
                    <input 
                      type="number" 
                      class="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      :value="song?.year"
                      placeholder="YYYY"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-400 mb-1">Track Number</label>
                    <input 
                      type="number" 
                      class="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      :value="song?.trackNumber"
                      placeholder="#"
                    >
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-4">
              <!-- Tags Section -->
              <div class="space-y-4">
                <h4 class="text-sm font-medium text-gray-300">Tags</h4>
                <div class="space-y-4">
                  <!-- Genre Tags -->
                  <div>
                    <label class="block text-sm font-medium text-gray-400 mb-2">Genre</label>
                    <div class="flex flex-wrap gap-2">
                      <span class="px-2 py-1 bg-blue-600/20 text-blue-300 rounded-full text-sm">Rock</span>
                      <span class="px-2 py-1 bg-blue-600/20 text-blue-300 rounded-full text-sm">Alternative</span>
                      <button class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded-full text-sm text-gray-300">+ Add</button>
                    </div>
                  </div>

                  <!-- Mood Tags -->
                  <div>
                    <label class="block text-sm font-medium text-gray-400 mb-2">Mood</label>
                    <div class="flex flex-wrap gap-2">
                      <span class="px-2 py-1 bg-purple-600/20 text-purple-300 rounded-full text-sm">Energetic</span>
                      <span class="px-2 py-1 bg-purple-600/20 text-purple-300 rounded-full text-sm">Upbeat</span>
                      <button class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded-full text-sm text-gray-300">+ Add</button>
                    </div>
                  </div>

                  <!-- Custom Tags -->
                  <div>
                    <label class="block text-sm font-medium text-gray-400 mb-2">Custom Tags</label>
                    <div class="flex flex-wrap gap-2">
                      <span class="px-2 py-1 bg-green-600/20 text-green-300 rounded-full text-sm">Favorite</span>
                      <span class="px-2 py-1 bg-green-600/20 text-green-300 rounded-full text-sm">Workout</span>
                      <button class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded-full text-sm text-gray-300">+ Add</button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Comments -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-400">Comments</label>
                <textarea 
                  class="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-24"
                  placeholder="Add your notes about this song..."
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="mt-6 flex justify-end gap-3">
            <button class="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm font-medium transition-colors">
              Cancel
            </button>
            <button class="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium transition-colors">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Player -->
    <div class="bg-slate-800 text-white p-4 shadow-lg">
    <div class="max-w-[1400px] mx-auto flex items-center gap-8">
        <div class="min-w-[200px] flex items-center gap-4">
          <!-- Tag button -->
          <button 
            @click="showTagPanel = !showTagPanel" 
            class="p-2 flex items-center justify-center rounded-full transition-colors"
            :class="{ 
              'opacity-50 cursor-not-allowed': !song,
              'bg-blue-600 hover:bg-blue-500': showTagPanel,
              'bg-slate-700 hover:bg-slate-600': !showTagPanel
            }"
            :disabled="!song">
            <div class="flex items-center gap-1">
              <TagIcon class="h-6 w-6" />
              <ChevronUpIcon v-if="showTagPanel" class="h-4 w-4" />
              <ChevronDownIcon v-else class="h-4 w-4" />
            </div>
          </button>
          <div>
        <h3 class="text-lg font-semibold">{{ song?.title || 'No song loaded' }}</h3>
        <p class="text-gray-300">{{ song?.artist || 'Select a song to play' }}</p>
          </div>
      </div>

      <audio
        ref="audio"
        :src="audioUrl"
        @timeupdate="handleTimeUpdate"
        @loadedmetadata="handleLoadedMetadata"
        @ended="handleEnded"
      ></audio>

      <div class="flex-1 flex items-center gap-4">
        <button 
          @click="handlePrevious" 
          class="p-2 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors"
          :class="{ 'opacity-50 cursor-not-allowed': !song }"
          :disabled="!song">
          <BackwardIcon class="h-6 w-6" />
        </button>
        
        <button 
          @click="togglePlay" 
          class="p-3 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors"
          :class="{ 'opacity-50 cursor-not-allowed': !song }"
          :disabled="!song">
          <PauseIcon v-if="isPlaying" class="h-8 w-8" />
          <PlayIcon v-else class="h-8 w-8" />
        </button>

        <button 
          @click="$emit('next')" 
          class="p-2 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors"
          :class="{ 'opacity-50 cursor-not-allowed': !song }"
          :disabled="!song">
          <ForwardIcon class="h-6 w-6" />
        </button>

        <div class="flex-1 flex items-center gap-2">
          <span class="text-sm text-gray-400">{{ formattedTime(currentTime) }}</span>
          <div class="flex-1 h-8 flex items-center relative">
            <input
              type="range"
              :min="0"
              :max="duration"
              :value="currentTime"
              @input="seek"
              class="absolute inset-0 w-full h-8 opacity-0 cursor-pointer z-10"
              :disabled="!song"
            >
            <div class="w-full h-1 bg-gray-600 rounded-lg relative">
              <div class="h-full bg-white rounded-lg transition-all duration-100" :style="{ width: `${(currentTime / duration) * 100}%` }"></div>
              <div class="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow-lg" :style="{ left: `${(currentTime / duration) * 100}%`, transform: 'translate(-50%, -50%)' }"></div>
            </div>
          </div>
          <span class="text-sm text-gray-400">{{ formattedTime(duration) }}</span>
        </div>

        <!-- Queue button -->
        <button 
          @click="showQueue = !showQueue" 
          class="p-2 flex items-center justify-center rounded-full bg-slate-700 hover:bg-slate-600 transition-colors"
          :class="{ 'opacity-50 cursor-not-allowed': !song }"
          :disabled="!song">
          <QueueListIcon class="h-6 w-6" />
        </button>

        <!-- Volume control -->
        <div class="flex items-center gap-2 ml-auto">
          <button 
            @click="toggleMute" 
            class="p-2 flex items-center justify-center rounded-full bg-slate-700 hover:bg-slate-600 transition-colors">
            <SpeakerXMarkIcon v-if="isMuted || volume === 0" class="h-6 w-6" />
            <SpeakerWaveIcon v-else class="h-6 w-6" />
          </button>
          <div class="h-8 w-24 flex items-center relative">
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              :value="isMuted ? 0 : volume"
              @input="handleVolumeInput"
              class="absolute inset-0 w-full h-8 opacity-0 cursor-pointer z-10"
            >
            <div class="w-full h-1 bg-gray-600 rounded-lg relative">
              <div class="h-full bg-white rounded-lg transition-all duration-100" :style="{ width: `${(isMuted ? 0 : volume) * 100}%` }"></div>
              <div class="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow-lg" :style="{ left: `${(isMuted ? 0 : volume) * 100}%`, transform: 'translate(-50%, -50%)' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Queue panel -->
    <div v-if="showQueue" class="absolute bottom-full right-0 mb-2 w-96 bg-slate-800 rounded-lg shadow-lg overflow-hidden">
      <div class="p-4 border-b border-slate-700 flex justify-between items-center">
        <h3 class="text-lg font-semibold">Queue</h3>
        <button @click="showQueue = false" class="p-1 hover:bg-slate-700 rounded-full transition-colors">
          <XMarkIcon class="h-5 w-5" />
        </button>
      </div>
      <div class="max-h-96 overflow-y-auto">
        <div v-for="(queuedSong, index) in playerStore.queue" :key="queuedSong.id" 
             class="p-3 hover:bg-slate-700 transition-colors flex items-center gap-3"
             :class="{ 
               'bg-slate-700': queuedSong.id === song?.id,
               'bg-slate-600': playerStore.isPlayed(queuedSong.id) && queuedSong.id !== song?.id
             }">
          <span class="text-gray-400 w-6">{{ index + 1 }}</span>
          <div class="flex-1 min-w-0">
            <div class="font-medium truncate">{{ queuedSong.title }}</div>
            <div class="text-sm text-gray-400 truncate">{{ queuedSong.artist }}</div>
          </div>
          <div class="flex items-center gap-2">
            <button v-if="queuedSong.id !== song?.id" 
                    @click="playFromQueue(queuedSong)"
                    class="p-1 hover:bg-slate-600 rounded-full transition-colors">
              <PlayIcon class="h-4 w-4" />
            </button>
            <button @click="removeFromQueue(queuedSong.id)"
                    class="p-1 hover:bg-slate-600 rounded-full transition-colors">
              <XMarkIcon class="h-4 w-4" />
            </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Remove all custom CSS as we're using Tailwind now */
</style> 