<script setup lang="ts">
import type { Song } from '../../api'
import { PlayIcon, PauseIcon, TrashIcon } from '@heroicons/vue/24/solid'

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
        <th class="p-3 text-left border-b bg-gray-50">Title</th>
        <th class="p-3 text-left border-b bg-gray-50">Artist</th>
        <th class="p-3 text-left border-b bg-gray-50">Type</th>
        <th class="p-3 text-left border-b bg-gray-50">URL</th>
        <th class="p-3 text-left border-b bg-gray-50">Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="song in songs" :key="song.id" class="hover:bg-gray-50">
        <td class="p-3 border-b">{{ song.title }}</td>
        <td class="p-3 border-b">{{ song.artist }}</td>
        <td class="p-3 border-b">{{ isDummySong(song) ? 'Dummy' : 'Regular' }}</td>
        <td class="p-3 border-b">
          <a v-if="isDummySong(song) && song.url" 
             :href="song.url" 
             target="_blank" 
             rel="noopener noreferrer"
             class="inline-block px-2 py-1 bg-gray-50 border border-gray-200 rounded font-mono text-sm max-w-[300px] truncate hover:bg-gray-100 hover:border-gray-300 transition-colors"
             :title="song.url">
            🔗 {{ song.url }}
          </a>
          <span v-else>-</span>
        </td>
        <td class="p-3 border-b">
          <div class="flex items-center gap-2">
            <button v-if="!isDummySong(song)" 
                    @click="emit('play-song', song)" 
                    class="px-3 py-1 bg-emerald-600 text-white rounded hover:bg-emerald-700 transition-colors flex items-center justify-center">
              <PauseIcon v-if="isCurrentSong(song) && isPlaying" class="h-5 w-5" />
              <PlayIcon v-else class="h-5 w-5" />
            </button>
            <button @click="emit('delete-song', song.id)" 
                    class="w-20 px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition-colors flex items-center justify-center">
              <TrashIcon v-if="songToDelete === song.id" class="h-5 w-5" />
              <span v-else>Delete</span>
            </button>
          </div>
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