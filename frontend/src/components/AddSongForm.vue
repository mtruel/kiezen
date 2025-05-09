<script setup lang="ts">
import FileUploadForm from './songs/FileUploadForm.vue'
import DummySongForm from './songs/DummySongForm.vue'

const emit = defineEmits<{
  (e: 'song-added'): void
}>()
</script>

<template>
  <div class="space-y-8 max-w-md mx-auto">
    <FileUploadForm @song-added="emit('song-added')" />
    <DummySongForm @song-added="emit('song-added')" />
  </div>
</template> 