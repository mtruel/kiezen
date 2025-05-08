<script setup lang="ts">
defineProps<{
  msg: string
}>()
</script>

<template>
  <div>
    <h1 class="text-4xl font-medium -mt-2.5 text-emerald-600 text-center lg:text-left">{{ msg }}</h1>
    <h3 class="text-xl text-center lg:text-left">
      You've successfully created a project with
      <a href="https://vite.dev/" target="_blank" rel="noopener" class="text-emerald-600 hover:text-emerald-700">Vite</a> +
      <a href="https://vuejs.org/" target="_blank" rel="noopener" class="text-emerald-600 hover:text-emerald-700">Vue 3</a>.
    </h3>
  </div>
</template>

<style scoped>
/* Remove all custom CSS as we're using Tailwind now */
</style>
