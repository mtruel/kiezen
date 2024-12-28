<!-- HTML Template -->
<template>
  <div class="music-player">
    <div class="player-controls">
      <button @click="play" v-if="!isPlaying">Play</button>
      <button @click="pause" v-else>Pause</button>
      <button @click="stop">Stop</button>
    </div>
    <div class="song-info">
      <p>{{ currentSong.title }}</p>
      <p>{{ currentSong.artist }}</p>
    </div>
    <div class="seek-bar">
      <input
          type="range"
          min="0"
          max="100"
          v-model="currentTime"
          @input="seek"
      />
      <p>{{ currentTime }}%</p>
    </div>
    <div class="volume-control">
      <input
          type="range"
          min="0"
          max="100"
          v-model="volume"
          @input="setVolume"
      />
      <p>Volume: {{ volume }}%</p>
    </div>
  </div>
</template>

<!-- TypeScript Script -->
<script lang="ts">
interface Song {
  title: string;
  artist: string;
  src: string;
}

export default {
  data() {
    return {
      isPlaying: false,
      currentSong: {
        title: "Example Song",
        artist: "Example Artist",
        src: "https://example.com/song.mp3",
      } as Song,
      currentTime: 0,
      volume: 50,
      audio: new Audio() as HTMLAudioElement,
    };
  },
  mounted() {
    this.audio.src = this.currentSong.src;
    this.audio.ontimeupdate = () => {
      this.currentTime = (this.audio.currentTime / this.audio.duration) * 100;
    };
  },
  methods: {
    play() {
      this.audio.play();
      this.isPlaying = true;
    },
    pause() {
      this.audio.pause();
      this.isPlaying = false;
    },
    stop() {
      this.audio.pause();
      this.audio.currentTime = 0;
      this.isPlaying = false;
    },
    seek() {
      this.audio.currentTime = (this.currentTime / 100) * this.audio.duration;
    },
    setVolume() {
      this.audio.volume = this.volume / 100;
    },
  },
};
</script>

<!-- CSS Styles -->
<style scoped>
</style>