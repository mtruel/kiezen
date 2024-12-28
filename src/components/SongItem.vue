<template>
  <div class="border-4 border-cyan-700">
    <button class="play-button" @click="handlePlayClick">
      <i class="fas fa-play" v-if="!isPlaying"></i>
      <i class="fas fa-pause" v-else></i>
    </button>
    <div class="song-info">
      <span class="title">{{ song.title }}</span>
      <span class="artist">{{ song.artist }}</span>
      <div class="meta">
        <span class="bpm">{{ song.bpm }} BPM</span>
        <span class="key">{{ song.key }}</span>
        <span class="genre">{{ song.genre }}</span>
      </div>
      <span class="duration">{{ formatDuration(song.duration) }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'

interface Song {
  title: string
  artist: string
  bpm: number
  key: string
  genre: string
  duration: number // duration in seconds
}

export default defineComponent({
  props: {
    song: {
      type: Object as PropType<Song>,
      required: true,
    },
    isPlaying: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handlePlayClick() {
      // emit event to parent component
      this.$emit('play-click', this.song)
    },
    formatDuration(duration: number) {
      const minutes = Math.floor(duration / 60)
      const seconds = Math.floor(duration % 60)
      return `${minutes}:${seconds.toString().padStart(2, '0')}`
    },
  },
  emits: ['play-click'],
})
</script>

<style scoped>
</style>