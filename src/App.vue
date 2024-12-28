<script setup lang="ts">
import MusicPlayer from "./components/MusicPlayer.vue";
import SongItem from "./components/SongItem.vue";


</script>

<template>
  <div>
    <SongItem
        :song="{ title: 'Song Title', artist: 'Artist Name', bpm: 120, key: 'C Major', genre: 'Electronic', duration: 240 }"
        :isPlaying="true"
        @play-click="handlePlayClick"
    />
    <h1 class="text-3xl font  -bold underline text-center">
      Hello world!
    </h1>
    <MusicPlayer></MusicPlayer>
  </div>

</template>

