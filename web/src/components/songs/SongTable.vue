<script setup lang="ts">
import type { Song } from '../../api'
import { PlayIcon, PauseIcon } from '@heroicons/vue/24/solid'
import { TrashIcon } from '@heroicons/vue/24/outline'
import { usePlayerStore } from '../../stores/playerStore'

const props = defineProps<{
  songs: Song[]
  songToDelete: string | null
  currentSong: Song | null
  isPlaying: boolean
}>()

const emit = defineEmits<{
  (e: 'play-song', song: Song): void
  (e: 'delete-song', songId: string): void
}>()

const playerStore = usePlayerStore()

const isDummySong = (song: Song) => {
  return song.isDummy === 1
}

const isCurrentSong = (song: Song) => {
  return props.currentSong?.id === song.id
}
</script>

<template>
  <table class="w-full border-collapse">
    <thead>
      <tr>
        <th class="p-3 text-left border-b bg-gray-50 w-16"></th>
        <th class="p-3 text-left border-b bg-gray-50">Song</th>
        <th class="p-3 text-left border-b bg-gray-50">Details</th>
        <th class="p-3 text-left border-b bg-gray-50 w-24">Duration</th>
        <th class="p-3 text-left border-b bg-gray-50 w-16"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="song in songs" :key="song.id" 
          class="hover:bg-gray-50"
          :class="{
            'bg-emerald-50': isCurrentSong(song),
            'bg-gray-50': playerStore.isPlayed(song.id) && !isCurrentSong(song)
          }">
        <td class="p-3 border-b">
          <button v-if="!isDummySong(song)" 
                  @click="emit('play-song', song)" 
                  class="p-2 bg-emerald-600 text-white rounded-full hover:bg-emerald-700 transition-colors flex items-center justify-center">
            <PauseIcon v-if="isCurrentSong(song) && isPlaying" class="h-5 w-5" />
            <PlayIcon v-else class="h-5 w-5" />
          </button>
        </td>
        <td class="p-3 border-b">
          <div class="flex flex-col">
            <span class="font-medium">{{ song.title }}</span>
            <span class="text-sm text-gray-600">{{ song.artist }}</span>
          </div>
        </td>
        <td class="p-3 border-b">
          <div class="flex flex-col">
            <span class="text-sm">{{ song.metadata?.genre || 'Unknown Label' }}</span>
            <span class="text-sm text-gray-600">{{ song.album || 'Unknown Album' }}</span>
          </div>
        </td>
        <td class="p-3 border-b text-sm text-gray-600">
          {{ song.metadata?.duration ? `${Math.floor(song.metadata.duration / 60)}:${Math.floor(song.metadata.duration % 60).toString().padStart(2, '0')}` : '-' }}
        </td>
        <td class="p-3 border-b">
          <button @click="emit('delete-song', song.id)" 
                  :class="[
                    'px-3 py-2 rounded flex items-center justify-center transition-colors',
                    songToDelete === song.id 
                      ? 'bg-red-600 text-white hover:bg-red-700' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  ]">
            <TrashIcon class="h-5 w-5" />
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts">
export default {
  name: 'SongTable'
}
</script> 