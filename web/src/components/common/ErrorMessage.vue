<script setup lang="ts">
defineProps<{
  message: string
}>()

const emit = defineEmits<{
  (e: 'retry'): void
}>()
</script>

<template>
  <div class="bg-red-50 border border-red-400 rounded-lg p-4 mb-4 flex items-center justify-between">
    <p class="text-red-600">{{ message }}</p>
    <button @click="emit('retry')" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors">
      Retry
    </button>
  </div>
</template>

<script lang="ts">
export default {
  name: 'ErrorMessage'
}
</script> 