<script setup lang="ts">
defineProps<{
  error?: string | null
  success?: string | null
}>()
</script>

<template>
  <div v-if="error" class="bg-red-50 border border-red-400 rounded-lg p-4 text-red-600">
    {{ error }}
  </div>
  
  <div v-if="success" class="bg-green-50 border border-green-400 rounded-lg p-4 text-green-600">
    {{ success }}
  </div>
</template>

<script lang="ts">
export default {
  name: 'FormMessage'
}
</script> 