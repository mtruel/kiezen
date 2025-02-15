<script lang="ts" setup>
defineProps({
  song: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="flex items-center gap-4 p-4 border-b border-gray-200 w-11/12">
    <!-- Cover Image -->
    <div v-if="song?.cover" class="w-16 h-16 flex-shrink-0">
      <img :src="song.cover" alt="Cover Image" class="w-16 h-16 object-cover rounded-lg"/>
    </div>
    <div v-else class="w  -16 h-16 bg-gray-300 flex items-center justify-center text-gray-600 rounded-lg">
      <span class="text-sm">No<br/>Image</span>
    </div>

    <!-- Song Details -->
    <div class="w-40">
      <h3 class="text-lg font-medium text-gray-800">{{ song?.title }}</h3>
      <p class="text-sm text-gray-600">{{ song?.artists }}</p>
      <p v-if="song?.album" class="text-xs text-gray-500">{{ song?.album }}</p>
    </div>

    <audio :src="song?.url" controls type="audio/mpeg"></audio>
    <!--    <Waveform :url="song?.url" :id="song?.id" />-->

    <!-- Actions -->
  </div>
</template>
